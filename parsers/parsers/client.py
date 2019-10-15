import requests
from requests.adapters import HTTPAdapter

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

from django.conf import settings



class StaticHttpClient:
    """

    """
    engine = requests
    timeout = 3

    def __init__(self):
        self.session = self.engine.Session()
        self.adapter = HTTPAdapter(max_retries=5)
        self.session.mount('https://', self.adapter)
        self.session.mount('http://', self.adapter)

    def get(self, url: str, headers: dict = None) -> str:
        """

        :param url:
        :param headers:
        :return:
        """
        data = self.session.get(url, headers=headers)
        return data.text


class DynamicHttpClient:
    """

    """
    timeout_for_page_load = 10

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(settings.CHROME_WEBDRIVER_PATH, options=chrome_options)

    def get(self, url: str, element_class: str) -> str:
        """

        :param url:
        :param element_class:
        :return:
        """
        self.driver.get(url)
        wait = WebDriverWait(self.driver, self.timeout_for_page_load)
        wait.until(expected_conditions.visibility_of_all_elements_located((By.CLASS_NAME, element_class)))
        data = self.driver.page_source
        self.driver.close()
        return data
