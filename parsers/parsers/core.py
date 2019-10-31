import logging
import requests

from abc import ABCMeta, abstractmethod
from typing import Any
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


class BaseParser(metaclass=ABCMeta):
    """
    Base class for parsers
    """
    _version: int = 0
    client_class: type = None
    parser_id: str = None
    parser_class: type = BeautifulSoup
    parser_markup: str = 'html.parser'

    @abstractmethod
    def parse(self) -> dict:
        """
        Abstract method for parse data
        :return: parsed data
        """
        raise NotImplementedError()


class BaseClient(metaclass=ABCMeta):
    """
    Base client class
    """
    timeout_in_seconds: int = 60
    engine: Any = None

    def url_exists(self, url: str) -> bool:
        """
        Check if url exists
        """
        response = requests.head(url)
        if response.status_code == 404:
            logger.warning(f'Requested url: {url} does not exists.')
            return False
        return True
