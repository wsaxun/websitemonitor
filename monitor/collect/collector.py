import json
import re

import requests
from bs4 import BeautifulSoup


def get_data(url, code):
    resp = requests.get("%s%s" % (url, code))
    if resp.status_code != 200:
        return "ERROR"
    resp = resp.content.decode()
    try:
        content = json.loads(
            resp.replace("update_" + code + "(", "").replace(")",
                                                             "")).get(
            "result")
    except json.decoder.JSONDecodeError:
        return 'ERROR'
    if not content:
        return 'ERROR'
    status = content['message']
    country = content['cp_country']
    city = content['cp_city']
    if status != 'OK':
        print(country + " " + city + ": " + status)
        rtime = 0
        ctime = 0
        dtime = 0
    else:
        rtime = content['rtime']  # 解析时间
        ctime = content['ctime']  # 链接时间
        dtime = content['dtime']  # 下载时间
    print(
        "%s\t%s %s\t%s\t%s\t%s" % (status, country, city, rtime, ctime, dtime))
    return (country, city, rtime, ctime, dtime)


def check_available():
    url = "https://api.asm.ca.com/1.6/acct_credits?&callback=check_avail_credits"
    response = requests.get(url)
    if response.status_code != 200:
        return 0
    # content = json.loads(response.content.replace("check_avail_credits%s(" % (response), "").replace(")", "")).get(
    #     "result")
    try:
        content = json.loads(
            response.content.decode().replace("check_avail_credits(",
                                              "").replace(")", "")).get(
            "result")
        result = eval(
            str(content.get('credits')).replace("[", "").replace("]", "")).get(
            'available')
        # print ast.literal_eval(str(content.get('credits')).replace("[", "").replace("]", "")).get('available')
        return result
    except Exception as e:
        print(e)
        return 0


def get_city():
    citys = []
    url = "https://asm.ca.com/en/checkit.php"
    response = requests.get(url)

    if response.status_code != 200:
        return 0
    soup = BeautifulSoup(response.content, "html5lib")
    datas = soup.find_all('span', attrs={"class": "h7"})

    for data in datas:
        middle = str(data.get_text()).split("-")[1].strip()
        city = re.sub('\(.*\)', "", middle).strip()
        # logging.info("当前城市: %s" % (city))
        citys.append(city)

    return citys
