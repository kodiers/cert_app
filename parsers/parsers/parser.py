from bs4 import BeautifulSoup

from parsers.models import ParserConfig
from .core import BaseParser


class MicrosoftParser(BaseParser):
    """

    """
    parser_id = 'microsoft-parser'

    def __init__(self):
        self.configuration = ParserConfig.objects.get(parser_class_id=self.parser_id)
        self._client = self.client_class()

    def parse(self):
        """
        
        :return:
        """
