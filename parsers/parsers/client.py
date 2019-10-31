import requests
import logging
from typing import Optional
from requests.adapters import HTTPAdapter

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

from django.conf import settings

from .core import BaseClient


logger = logging.getLogger(__name__)


class StaticHttpClient(BaseClient):
    """
    Use requests to get static pages (not SPA).
    """
    engine = requests
    timeout_in_seconds = 3

    def __init__(self):
        self.session = self.engine.Session()
        self.adapter = HTTPAdapter(max_retries=5)
        self.session.mount('https://', self.adapter)
        self.session.mount('http://', self.adapter)

    def get(self, url: str, headers: dict = None) -> str:
        """
        Send request to url.
        """
        data = self.session.get(url, headers=headers)
        return data.text


class DynamicHttpClient(BaseClient):
    """
    Use requests to get dynamic pages (SPA or JS pages).
    """
    timeout_in_seconds = 60
    engine = webdriver.Chrome

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = self.engine(settings.CHROME_WEBDRIVER_PATH, options=chrome_options)

    def get(self, url: str, css_selector: str) -> Optional[str]:
        """
        Send request to url and wait until element with css_selector will be loaded.
        """
        self.driver.get(url)
        wait = WebDriverWait(self.driver, self.timeout_in_seconds)
        try:
            wait.until(expected_conditions.visibility_of_all_elements_located((By.CSS_SELECTOR, css_selector)))
        except TimeoutException as e:
            logger.error(f'Error on request. {e} . Data: {url} - {css_selector}')
            return None
        data = self.driver.page_source
        return data

    def close(self) -> None:
        """
        Close webdriver connection
        """
        self.driver.close()

    def __del__(self):
        """
        Kill webriver(Chrome) engine process
        :return:
        """
        self.driver.quit()
