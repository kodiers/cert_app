import logging
from typing import Optional, Any

from bs4 import BeautifulSoup

from parsers.models import ParserConfig
from .core import BaseParser
from .client import DynamicHttpClient


logger = logging.getLogger(__name__)


class MicrosoftParser(BaseParser):
    """
    Parser for Microsoft exams and certifications.
    """
    _version = 1
    parser_id = 'microsoft-parser'
    client_class = DynamicHttpClient

    def __init__(self):
        self.configuration = ParserConfig.objects.get(parser_class_id=self.parser_id)
        self.client = self.client_class()

    def _get_element_text(self, element: Any, delimiter: str, index: int) -> str:
        """
        Get text information without any words exam/ceritication.
        For example:
        if element.text = "Exam 400: Some exam" and delimiter=':' and index='1' will return 'Some exam'
        :param element: SoupSieve element
        :param delimiter: any symbol to split text
        :param index: index of data in resulting array
        """
        return element.text.split(delimiter)[index].strip()

    def _get_start_links(self) -> set:
        """
        Get unique certification links from main_url and check if certification page exists.
        """
        raw_data = self.client.get(self.configuration.main_url, self.configuration.certifications_link_css_selector)
        data = raw_data if raw_data else ''
        parser = self.parser_class(data, self.parser_markup)
        elements = parser.select(self.configuration.certifications_link_css_selector)
        links = set()
        for element in elements:
            link = element.get('href')
            base_url = self.configuration.base_url
            if base_url:
                if not base_url.endswith('/'):
                    base_url = f'{base_url}/'
                link = f'{base_url}{link}'
            if self.client.url_exists(link):
                links.add(link)
        return links

    def _parse_exams(self, parser: BeautifulSoup) -> list:
        """
        Get needed data from loaded page.
        """
        element_titles = parser.select(self.configuration.exam_title_css_selector)
        element_descriptions = parser.select(self.configuration.exam_description_css_selector)
        exams_data = list()
        for index, element in enumerate(element_titles):
            exam_data = dict()
            exam_data['number'] = self._get_element_text(element, ':', 0)
            exam_data['title'] = self._get_element_text(element, ':', 1)
            try:
                exam_data['description'] = element_descriptions[index].text
            except IndexError:
                logger.error(f'Could not find description for exam: {exam_data["number"]}.')
            exams_data.append(exam_data)
        return exams_data

    def _parse_certification(self, url: str) -> Optional[dict]:
        """
        Request and get needed data from loaded certification page.
        """
        data = self.client.get(url, self.configuration.certification_title_css_selector)
        if data is None:
            return None
        parser = self.parser_class(data, self.parser_markup)
        title_element = parser.select_one(self.configuration.certification_title_css_selector)
        description_element = parser.select_one(self.configuration.certification_description_css_selector)
        certification_data = {'title': title_element.text, 'description': description_element.text}
        exams = self._parse_exams(parser)
        certification_data['exams'] = exams
        return certification_data

    def parse(self) -> list:
        """
        Parse certifications and exams.
        """
        certifications_data = list()
        try:
            base_links = list(self._get_start_links())
            for link in base_links:
                certification_data = self._parse_certification(link)
                if certification_data:
                    certifications_data.append(certification_data)
        finally:
            self.client.close()
            del self.client
        return certifications_data
