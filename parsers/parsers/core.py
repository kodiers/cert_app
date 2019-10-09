from abc import ABCMeta, abstractmethod

from .client import ParserHttpClient


class BaseParser(metaclass=ABCMeta):
    """

    """
    client_class: type = ParserHttpClient
    parser_id: str = None

    @abstractmethod
    def parse(self):
        """

        :return:
        """
        raise NotImplementedError()
