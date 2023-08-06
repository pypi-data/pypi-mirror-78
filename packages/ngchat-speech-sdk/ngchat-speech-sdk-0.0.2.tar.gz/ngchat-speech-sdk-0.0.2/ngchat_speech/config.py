
"""
Definition the APP Settings in here.

Description:
The Settings will try to find the arguments from os.environ.
If the argument is missing in os.environ, ValidationError
will be raised.

"""

from typing import Dict, Optional
import pathlib
import os
import ujson as json


class Settings():
    """
    Collect arguments from os.environ in this class.

    It try to find the arguments from os.environ.
    If the argument is missing, ValidationError will be raised.
    """

    # logger conf file path
    current_path = pathlib.Path(__file__).parent.absolute()
    file_path = os.path.join(current_path, "logger_conf.json")

    LOGGER_CONF_PATH: Optional[str] = file_path
    LOGGER_CONF: Optional[Dict] = None
    LOGGER_LEVEL: str = "INFO"


# Load confs before to assign to settings
_settings = Settings()
with open(_settings.LOGGER_CONF_PATH, 'r') as f:
    logger_conf = json.load(f)
_settings.LOGGER_CONF = logger_conf
settings = _settings
