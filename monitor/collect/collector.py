import json
import re

from bs4 import BeautifulSoup
import eventlet
from eventlet.green.urllib import request

from monitor.utils.config import CONFIG

eventlet.monkey_patch()


class Asm:
    CONFIGS = CONFIG

    def get_data(self, urls):
        pool = eventlet.greenpool.GreenPool(size=500)
        results = []
        for result in pool.imap(self._source, urls):
            resp = result.read().decode()
            url = result.geturl()
            update_code_string = url.split('=')[-1]
            try:
                content = json.loads(
                    resp.replace(update_code_string + "(", "").replace(")",
                                                                       "")).get(
                    "result")
            except json.decoder.JSONDecodeError:
                continue
            if not content:
                continue
            status = content['message']
            country = content['cp_country']
            city = content['cp_city']
            if status != 'OK':
                rtime = ctime = dtime = 0
            else:
                rtime, ctime, dtime = (
                    content['rtime'], content['ctime'], content['dtime'])
            results.append((country, city, rtime, ctime, dtime))
        return results

    @staticmethod
    def _source(url, error_code=None):
        response = request.urlopen(url)
        if response.status != 200:
            if not error_code:
                return 0
            return error_code
        return response

    @staticmethod
    def _not_async_source(url, error_code=None):
        response = request.urlopen(url)
        if response.status != 200:
            if not error_code:
                return 0
            return error_code
        return response.read()

    @property
    def visits(self):
        url = self.CONFIGS.credits_config
        response = self._not_async_source(url)
        if not response:
            return 0
        try:
            content = json.loads(
                response.replace("check_avail_credits(",
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
        response = self._not_async_source(url)
        if not response:
            return 0
        soup = BeautifulSoup(response, "html5lib")
        items = soup.find_all('span', attrs={"class": "h7"})

        for data in items:
            middle = str(data.get_text()).split("-")[1].strip()
            city = re.sub('\(.*\)', "", middle).strip()
            citys.append(city)

        return citys
