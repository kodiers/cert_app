import requests
from requests.adapters import HTTPAdapter


class ParserHttpClient:
    """

    """
    engine = requests
    timeout = 3

    def __init__(self):
        self.session = requests.Session()
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
