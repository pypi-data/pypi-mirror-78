import logging

from logzero import setup_logger

import curia.api.swagger_client as swagger_client
from curia.api.swagger_client import configuration

DEFAULT_LOG_LEVEL = logging.INFO


class Session():
    """Creates a Curia authentication session"""

    def __init__(self, api_token: str = None, debug: bool = False):
        self.api_token = api_token
        self.debug = debug
        self.logger = setup_logger(name='curia', level=DEFAULT_LOG_LEVEL)
        self.api_client = swagger_client

        if debug:
            self.logger.setLevel(logging.DEBUG)

        api_config = configuration.Configuration()
        api_config.debug = self.debug
        api_config.access_token = self.api_token

        self.api_instance = swagger_client.DefaultApi(swagger_client.ApiClient(api_config))
