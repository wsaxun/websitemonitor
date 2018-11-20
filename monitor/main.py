import os
import sys

SOURCE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SOURCE)


def main():
    from monitor.utils.log import log_init
    from monitor.workdata.workdata import works
    from monitor.collect.collector import Asm
    log = log_init(__name__)
    source = Asm()
    city = source.city
    log.info("当前获取到的城市列表: %s" % city)
    visits = source.visits
    log.info("监测网站可用次数为%d" % visits)
    works()
    #
    # if visits / 10 >= 4:
    #     works()
    #     log.info("监测网站剩余可用次数为%d" % source.visits)
    # else:
    #     log.info("监测网站剩余可用次数为%d" % visits)


if __name__ == '__main__':
    import datetime
    print(datetime.datetime.now())
    main()
    print(datetime.datetime.now())

