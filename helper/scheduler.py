# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyScheduler
   Description :
   Author :        JHao
   date：          2019/8/5
-------------------------------------------------
   Change Activity:
                   2019/08/05: proxyScheduler
                   2021/02/23: runProxyCheck时,剩余代理少于POOL_SIZE_MIN时执行抓取
-------------------------------------------------
"""
__author__ = 'JHao'

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler

from handler.configHandler import ConfigHandler
from handler.logHandler import LogHandler
from handler.proxyHandler import ProxyHandler
from helper.check import Checker
from helper.fetch import Fetcher
from util.six import Queue


def __runProxyFetch():
    proxy_queue = Queue()
    proxy_fetcher = Fetcher()

    for proxy in proxy_fetcher.run():
        proxy_queue.put(proxy)

    Checker("raw", proxy_queue)


def __runProxyCheck():
    proxy_handler = ProxyHandler()
    proxy_queue = Queue()

    if proxy_handler.db.getCount().get("total", 0) < proxy_handler.conf.poolSizeMin:
        __runProxyFetch()
    for proxy in proxy_handler.getAll():
        proxy_queue.put(proxy)
    Checker("use", proxy_queue)


def runScheduler(name):
    __runProxyFetch()

    timezone = ConfigHandler().timezone
    scheduler_log = LogHandler("scheduler")
    scheduler = BlockingScheduler(logger=scheduler_log, timezone=timezone)

    if name == 'check':
        scheduler.add_job(__runProxyCheck, 'interval', minutes=ConfigHandler().proxy_check_time, id="proxy_check",
                          name="proxy独立检查")
    elif name == "craw":
        scheduler.add_job(__runProxyFetch, 'interval', minutes=ConfigHandler().proxy_fetch_time, id="proxy_fetch",
                          name="proxy独立采集")

    else:
        scheduler.add_job(__runProxyFetch, 'interval', minutes=ConfigHandler().proxy_fetch_time, id="proxy_fetch",
                          name="proxy采集")
        scheduler.add_job(__runProxyCheck, 'interval', minutes=ConfigHandler().proxy_check_time, id="proxy_check",
                          name="proxy检查")

    executors = {
        'default': {'type': 'threadpool', 'max_workers': 20},
        'processpool': ProcessPoolExecutor(max_workers=5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 10
    }

    scheduler.configure(executors=executors, job_defaults=job_defaults, timezone=timezone)

    scheduler.start()


if __name__ == '__main__':
    runScheduler("test")
