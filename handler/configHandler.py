# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     configHandler
   Description :
   Author :        JHao
   date：          2020/6/22
-------------------------------------------------
   Change Activity:
                   2020/6/22:
-------------------------------------------------
"""
__author__ = 'JHao'

import os

import setting
from util.lazyProperty import LazyProperty
from util.singleton import Singleton
from util.six import reload_six, withMetaclass


class ConfigHandler(withMetaclass(Singleton)):

    def __init__(self):
        pass

    @LazyProperty
    def serverHost(self):
        return os.environ.get("HOST", setting.HOST)

    @LazyProperty
    def serverPort(self):
        return os.environ.get("PORT", setting.PORT)

    @LazyProperty
    def dbConn(self):
        return os.getenv("DB_CONN", setting.DB_CONN)

    @LazyProperty
    def tableName(self):
        return os.getenv("TABLE_NAME", setting.TABLE_NAME)

    @property
    def fetchers(self):
        reload_six(setting)
        # 修改这里 执行特定craw
        # return setting.CRAW1
        # return setting.CRAW2
        # return setting.CRAW3
        # return setting.CRAW4
        return setting.PROXY_FETCHER

    @LazyProperty
    def httpUrl(self):
        return os.getenv("HTTP_URL", setting.HTTP_URL)

    @LazyProperty
    def validate_KEYWORD(self):
        return os.getenv("VALIDATE_KEYWORD", setting.VALIDATE_KEYWORD)

    @LazyProperty
    def validate_HEADER(self):
        return os.getenv("VALIDATE_HEADER", setting.VALIDATE_HEADER)

    @LazyProperty
    def CHECK_THREAD(self):
        return os.getenv("CHECK_THREAD", setting.CHECK_THREAD)

    @LazyProperty
    def httpsUrl(self):
        return os.getenv("HTTPS_URL", setting.HTTPS_URL)

    @LazyProperty
    def verifyTimeout(self):
        return int(os.getenv("VERIFY_TIMEOUT", setting.VERIFY_TIMEOUT))

    # @LazyProperty
    # def proxyCheckCount(self):
    #     return int(os.getenv("PROXY_CHECK_COUNT", setting.PROXY_CHECK_COUNT))

    @LazyProperty
    def maxFailCount(self):
        return int(os.getenv("MAX_FAIL_COUNT", setting.MAX_FAIL_COUNT))

    # @LazyProperty
    # def maxFailRate(self):
    #     return int(os.getenv("MAX_FAIL_RATE", setting.MAX_FAIL_RATE))

    @LazyProperty
    def poolSizeMin(self):
        return int(os.getenv("POOL_SIZE_MIN", setting.POOL_SIZE_MIN))

    @LazyProperty
    def proxy_check_time(self):
        return os.getenv("PROXY_CHECK_TIME", setting.PROXY_CHECK_TIME)

    @LazyProperty
    def proxy_fetch_time(self):
        return os.getenv("PROXY_FETCH_TIME", setting.PROXY_FETCH_TIME)

    @LazyProperty
    def timezone(self):
        return os.getenv("TIMEZONE", setting.TIMEZONE)
