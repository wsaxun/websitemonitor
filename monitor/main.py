import os
import sys

SOURCE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SOURCE)


def main():
    from monitor.utils.log import log_init
    from monitor.workdata.workdata import works
    from monitor.collect.collector import get_city, check_available
    log = log_init(__name__)
    city = get_city()
    log.info("当前获取到的城市列表: %s" % city)
    result = int(check_available())
    log.info("监测网站可用次数为%d" % result)
    if result / 10 >= 4:
        works()
        log.info("监测网站剩余可用次数为%d" % int(check_available()))
    else:
        log.info("监测网站剩余可用次数为%d" % result)


if __name__ == '__main__':
    main()
