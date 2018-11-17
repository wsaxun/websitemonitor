import json
import re

import requests
from bs4 import BeautifulSoup

from monitor.utils.config import CONFIG
from monitor.utils.exception import AsmError


class Asm:
    CONFIGS = CONFIG

    @staticmethod
    def _source(url, error_code=None):
        response = requests.get(url)
        if response.status_code != 200:
            if not error_code:
                return 0
            return error_code
        return response

    def get_data(self, url, code):
        url = url + str(code)
        response = self._source(url, error_code='ERROR')
        assert response != 'ERROR', 'connect error'
        resp = response.content.decode()
        try:
            content = json.loads(
                resp.replace("update_" + code + "(", "").replace(")",
                                                                 "")).get(
                "result")
        except json.decoder.JSONDecodeError:
            raise AsmError('access error')
        assert content, 'access error'
        status = content['message']
        country = content['cp_country']
        city = content['cp_city']
        if status != 'OK':
            rtime = ctime = dtime = 0
        else:
            rtime, ctime, dtime = (
                content['rtime'], content['ctime'], content['dtime'])
        return country, city, rtime, ctime, dtime

    @property
    def visits(self):
        url = self.CONFIGS.credits_config
        response = self._source(url)
        if not response:
            return 0
        try:
            content = json.loads(
                response.content.decode().replace("check_avail_credits(",
                                                  "").replace(")", "")).get(
                "result")
            result = content.get('credits')[0].get('available')
            return int(result)
        except (
                json.decoder.JSONDecodeError, IndexError, TypeError,
                ValueError):
            return 0

    @property
    def city(self):
        citys = []
        url = self.CONFIGS.city_config
        response = self._source(url)
        if not response:
            return 0
        soup = BeautifulSoup(response.content, "html5lib")
        items = soup.find_all('span', attrs={"class": "h7"})

        for data in items:
            middle = str(data.get_text()).split("-")[1].strip()
            city = re.sub('\(.*\)', "", middle).strip()
            citys.append(city)

        return citys
