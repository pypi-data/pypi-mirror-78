"""
Ngchat speech SDK

Descriptions:
How Recognizer to connect the STT server is defined in here.

History:
2020/06/20 Created by Theo
2020/06/29 Change websockets package
2020/07/06 Refactored by Block Chen
"""


from typing import (
    Optional,
    Dict,
    Callable,
    Text
)
import websockets
from ws4py.client.threadedclient import WebSocketClient
import urllib
import asyncio
from ngchat_speech import audio
import threading
import json
import warnings
from ngchat_speech import logger

svc_logger = logger.get_SVCLogger(__name__)

SUPPORTED_AUDIO_FORMAT = {
    'riff-16khz-16bit-mono-pcm': {
        "frame_rate": 16000,
        "sample_width": 2,
        "channels": 1
    }
}


class SpeechConfig():
    """ Setup speech arguments """

    def __init__(
        self,
        host: Text,
        speech_recognition_language: Optional[Text] = 'zh-TW',
        speech_synthesis_language: Optional[Text] = 'zh-TW',
        speech_synthesis_voice_name: Optional[Text] = 'zh-TW-Biaobei',
        speech_synthesis_output_format_id: Text = 'riff-16khz-16bit-mono-pcm',
    ):
        """Init speech arguments"""
        self.__host = host
        self.__speech_recognition_language = speech_recognition_language
        self.__speech_synthesis_language = speech_synthesis_language
        self.__speech_synthesis_voice_name = speech_synthesis_voice_name
        try:
            self.__output_format = SUPPORTED_AUDIO_FORMAT[speech_synthesis_output_format_id]
        except KeyError:
            raise ValueError("Unavailable format id")
        self.__speech_synthesis_output_format_id = speech_synthesis_output_format_id
        self.__speech_synthesis_format_label = 'X-SeasaltAI-OutputFormat'

    @property
    def host(self) -> Text:
        """Retrun host"""
        return self.__host

    @property
    def format_label(self) -> Text:
        """Return format label"""
        return self.__speech_synthesis_format_label

    @property
    def ngchat_format_label(self) -> Text:
        """Return format lable"""
        return self.__speech_synthesis_format_label

    @property
    def output_format(self) -> Dict:
        """Return output format"""
        return self.__output_format

    @property
    def speech_recognition_language(self) -> Optional[Text]:
        """Return recognition language"""
        return self.__speech_recognition_language

    @speech_recognition_language.setter
    def speech_recognition_language(self, language: Text) -> None:
        """Return recognition language"""
        self.__speech_recognition_language = language

    @property
    def speech_synthesis_language(self) -> Optional[Text]:
        """Return synthesis language"""
        return self.__speech_synthesis_language

    @speech_synthesis_language.setter
    def speech_synthesis_language(self, language: Text) -> None:
        """Set synthesis language"""
        self.__speech_synthesis_language = language

    @property
    def speech_synthesis_voice_name(self) -> Optional[Text]:
        """Return voice name"""
        return self.__speech_synthesis_voice_name

    @speech_synthesis_voice_name.setter
    def speech_synthesis_voice_name(self, voice_name: Text) -> None:
        """Set voice name"""
        self.__speech_synthesis_voice_name = voice_name

    @property
    def speech_synthesis_output_format_id(self) -> Text:
        """Return output format id"""
        return self.__speech_synthesis_output_format_id

    @speech_synthesis_output_format_id.setter
    def speech_synthesis_output_format_id(self, format_id: Text) -> None:
        """Set output format id"""
        try:
            self.__output_format = SUPPORTED_AUDIO_FORMAT[format_id]
        except KeyError:
            raise ValueError("Unavailable format id")
        self.__speech_synthesis_output_format_id = format_id

    def enable_audio_logging(self):
        """Enable audio loggin"""
        pass


class Recognizer(WebSocketClient):
    """Base class of recognizer"""

    def __init__(
        self,
        speech_config: SpeechConfig,
        audio_config: Optional[audio.AudioConfig] = None
    ):
        """Initialize speech recognizer"""
        # load speech_config
        self.__speech_config = speech_config
        self.__format_label = speech_config.format_label
        self.__host = speech_config.host
        self.__speech_recognition_language = speech_config.speech_recognition_language
        self.__speech_synthesis_language = speech_config.speech_synthesis_language
        self.__speech_synthesis_voice_name = speech_config.speech_synthesis_voice_name
        self.__output_format = speech_config.output_format
        self.__speech_synthesis_output_format_id = speech_config.speech_synthesis_output_format_id

        # load audio_config
        self.__input_stream = None
        self.__content_type = None
        self.__audio_config = audio_config
        self.__ws_uri = None
        if audio_config is not None:
            self.__input_stream = audio_config.stream
            self.__content_type = urllib.parse.urlencode(
                [
                    ("content-type", self.__input_stream.stream_format.content_type)
                ]
            )
        if self.__content_type is not None:
            self.__ws_uri = f"{self.__host}?{self.__content_type}"
        else:
            self.__ws_uri = f"{self.__host}"
        self.is_running = False

        # create events
        self.__session_started_event = SessionStartedEvent()
        self.__session_stopped_event = SessionStoppedEvent()
        self.__recognizing_event = RecognizingEvent()
        self.__recognized_event = RecognizedEvent()
        self.__canceled_event = CanceledEvent()
        self.session_id = None

        # init websocket client
        super().__init__(url=self.__ws_uri)

    def start_continuous_recognition_async(self):
        """Start speech recognition"""
        self.is_running = True
        self.connect()
        recognition_thread = threading.Thread(
            target=self.send_thread,
        )
        recognition_thread.daemon = True
        recognition_thread.start()

    def thread_start_continuous_recognition_async(self):
        """
        Start a thread to start continuous recognition

        Deprecated: this is used for websockets, but since it has the issue of ws.send(), we changed to use ws4py.
        See coninuous_recognition_async for more info.
        """
        warnings.warn("Deprecated: websockets has the issue of sending data", DeprecationWarning)
        self.ngchat_stt_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.ngchat_stt_loop)
        try:
            self.ngchat_stt_loop.run_until_complete(
                self.await_continuous_recognition_async()
            )
        except Exception as e:
            svc_logger.error(
                f"Exception in thread_start_continuous_recognition_async: {e}"
            )
        finally:
            self.ngchat_stt_loop.close()

    async def await_continuous_recognition_async(self):
        """
        Wait results of continuous recognition

        Deprecated: this is used for websockets, but since it has the issue of ws.send(), we changed to use ws4py.
        See coninuous_recognition_async for more info.
        """
        warnings.warn("Deprecated: websockets has the issue of sending data", DeprecationWarning)
        await self.continuous_recognition_async()

    async def continuous_recognition_async(self):
        """
        Connect ngchat stt server by websocket

        Start a thread to send data to ngchat stt server
        Wait recognized results

        Deprecated: this is used for websockets, but when test, if started a new thread running coninuous_recognition_async
        in on_event_start in twilio_voice.py, from logs of ngchat stt server, ws.send() doesn't send package in real time.
        It sent the first package after about 2 seconds, then sent other packages continuously.
        After changed to use ws4py client, logs of stt server show sending packages is right. So we changed to use ws4py.

        """
        warnings.warn("Deprecated: websockets has the issue of sending data", DeprecationWarning)
        try:
            async with websockets.client.connect(self.__ws_uri) as ws:
                if self.__session_started_event.is_set:
                    # Not sure how to get session id on websocket starting
                    # the handshake response header is set in evt id
                    evt = {"id": f"{ws.response_headers}"}
                    evt_res = EventResults(evt)
                    self.__session_started_event.callback(evt_res)
                if self.__input_stream is not None:
                    thread_send = threading.Thread(target=self.send, args=(ws,))
                    thread_send.start()
                    await self.receive(ws)
            if self.__session_stopped_event.is_set:
                evt = {"session_id": self.session_id}
                evt_res = EventResults(evt)
                self.__session_stopped_event.callback(evt_res)
        except Exception as e:
            svc_logger.error(f"Exception in continuous_recognition_async: {e}")

    def opened(self):
        """Open websocket"""
        svc_logger.info("websocket opened")

    def closed(self, code, reason):
        """Close websocket"""
        svc_logger.info(f"Closed down: {code}, {reason}")

    def send_thread(self):
        """Send data to websocket"""
        while self.is_running:
            try:
                if self.__input_stream is not None:
                    buf = self.__input_stream.read_wait()
                    if buf is not None and len(buf) > 0:
                        self.send(buf, binary=True)
            except KeyboardInterrupt:
                self.stop_continuous_recognition_async()
        else:
            if self.__canceled_event.is_set:
                evt = {"session_id": self.session_id}
                evt_res = EventResults(evt)
                self.__canceled_event.callback(evt_res)
            self.send("EOS")
            self.close()

    def received_message(self, message) -> None:
        """Receive result from websocket"""
        try:
            evt = json.loads(str(message))
            if evt['status'] == 0:
                self.session_id = evt['id']
                if 'result' in evt:
                    if evt['result']['final']:
                        if self.__recognized_event.is_set:
                            evt_res = EventResults(evt)
                            self.__recognized_event.callback(evt_res)
                    else:
                        if self.__recognizing_event.is_set:
                            evt_res = EventResults(evt)
                            self.__recognizing_event.callback(evt_res)
            else:
                errmsg = "Received error from server: "
                if 'message' in evt:
                    errmsg += f"{evt['message']}"
                raise RuntimeError(errmsg)
        except Exception as e:
            svc_logger.error(f"Exception in receive of continuous_recognition_async: {e}")
            self.stop_continuous_recognition_async()

    def stop_continuous_recognition_async(self):
        """Stop recognition"""
        self.is_running = False
        self.ngchat_stt_loop.close()

    @property
    def speech_config(self) -> SpeechConfig:
        """Return speech config"""
        return self.__speech_config

    @property
    def audio_config(self) -> Optional[audio.AudioConfig]:
        """Return audio config"""
        return self.__audio_config

    @property
    def format_label(self) -> Text:
        """Return format lable"""
        return self.__format_label

    @property
    def myhost(self) -> Text:
        """Return host"""
        return self.__host

    @property
    def speech_recognition_language(self) -> Optional[Text]:
        """Return recognition language"""
        return self.__speech_recognition_language

    @property
    def speech_synthesis_language(self) -> Optional[Text]:
        """Return synthesis language"""
        return self.__speech_synthesis_language

    @property
    def speech_synthesis_voice_name(self) -> Optional[Text]:
        """Return voice name"""
        return self.__speech_synthesis_voice_name

    @property
    def output_format(self) -> Dict:
        """Return output format"""
        return self.__output_format

    @property
    def speech_synthesis_output_format_id(self) -> Optional[Text]:
        """Return output format id"""
        return self.__speech_synthesis_output_format_id

    @property
    def session_started(self):
        """Return session started event"""
        return self.__session_started_event

    @property
    def session_stopped(self):
        """Return session stopped event"""
        return self.__session_stopped_event

    @property
    def speech_start_detected(self):
        """Return start detected"""
        raise NotImplementedError

    @property
    def speech_end_detected(self):
        """Return end detected"""
        raise NotImplementedError

    @property
    def recognizing(self):
        """Return Recognizing event"""
        return self.__recognizing_event

    @property
    def recognized(self):
        """Return recognized event"""
        return self.__recognized_event

    @property
    def canceled(self):
        """Return canceled event"""
        return self.__canceled_event


class SpeechRecognizer(Recognizer):
    """Speech recognize"""

    def __init__(
        self,
        speech_config: SpeechConfig,
        audio_config: Optional[audio.AudioConfig] = None
    ):
        """Initialze speech recognizer"""
        super().__init__(
            speech_config=speech_config,
            audio_config=audio_config
        )


class EventBase():
    """Base class for events"""

    def __init__(self):
        """Init event base"""
        self.callback = None
        self.__is_set = False

    def connect(self, callback: Callable):
        """Connnect event"""
        self.callback = callback
        self.__is_set = True

    @property
    def is_set(self):
        """Return is_set"""
        return self.__is_set


class SessionStartedEvent(EventBase):
    """Session started event"""

    def __init__(self):
        """Init sesstion started event"""
        super().__init__()


class SessionStoppedEvent(EventBase):
    """Session stopped event"""

    def __init__(self):
        """Init Session stopped event"""
        super().__init__()


class RecognizingEvent(EventBase):
    """Recognizing event"""

    def __init__(self):
        """Init Recognizing event"""
        super().__init__()


class RecognizedEvent(EventBase):
    """Recognized event"""

    def __init__(self):
        """Return recognized event"""
        super().__init__()


class CanceledEvent(EventBase):
    """Canceled event"""

    def __init__(self):
        """Init canceled event"""
        super().__init__()


class EventResults():
    """Simulate MS SessionEventArgs class"""

    def __init__(self, evt):
        """Init event results"""
        self.status = None
        self.segment = None
        self.result = None
        self.session_id = None

        if "status" in evt:
            self.status = evt.get("status")
        if "segment" in evt:
            self.segment = evt.get("segment")
        if "result" in evt:
            self.result = Results(evt.get("result"))
        if "id" in evt:
            self.session_id = evt.get("id")

    def __str__(self):
        """Return event info"""
        return (
            f"status={self.status}, "
            f"segment={self.segment}, "
            f"result=({self.result}), "
            f"session_id={self.session_id}"
        )


class Results():
    """Simulate MS SpeechRecognitionEventArgs class"""

    def __init__(self, results):
        """Initialize results"""
        self.result_id = None
        self.text = None
        self.reason = None
        self.final = None

        if 'result_id' in results:
            self.result_id = None
        if 'hypotheses' in results:
            self.text = results['hypotheses'][0]['transcript']
        if 'reason' in results:
            self.reason = None
        if 'final' in results:
            self.final = results['final']

    def __str__(self):
        """Return result info"""
        return (
            f"result_id={self.result_id}, "
            f"text={self.text}, "
            f"reason={self.reason}, "
            f"final={self.final}"
        )
