from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup

from .client import StaticHttpClient


class BaseParser(metaclass=ABCMeta):
    """
    Base class for parsers
    """
    client_class: type = StaticHttpClient
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
