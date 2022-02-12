# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     _validators
   Description :   定义proxy验证方法
   Author :        JHao
   date：          2021/5/25
-------------------------------------------------
   Change Activity:
                   2021/5/25:
-------------------------------------------------
"""
__author__ = 'JHao'

from re import findall

import requests

from handler.configHandler import ConfigHandler
from util.singleton import Singleton
from util.six import withMetaclass

conf = ConfigHandler()

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
          'Accept': '*/*',
          'Connection': 'keep-alive',
          'Accept-Language': 'zh-CN,zh;q=0.8'}


class ProxyValidator(withMetaclass(Singleton)):
    pre_validator = []
    http_validator = []
    https_validator = []

    @classmethod
    def addPreValidator(cls, func):
        cls.pre_validator.append(func)
        return func

    @classmethod
    def addHttpValidator(cls, func):
        cls.http_validator.append(func)
        return func

    @classmethod
    def addHttpsValidator(cls, func):
        cls.https_validator.append(func)
        return func


@ProxyValidator.addPreValidator
def formatValidator(proxy):
    """检查代理格式"""
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


@ProxyValidator.addHttpValidator
def httpTimeOutValidator(proxy):
    """ http检测超时 """

    # log = LogHandler("Validator")

    proxies = {"http": "http://{proxy}".format(proxy=proxy), "https": "https://{proxy}".format(proxy=proxy)}

    try:
        r = requests.head(conf.httpUrl, headers=HEADER, proxies=proxies, timeout=conf.verifyTimeout)
        # 修改check算法，只要head请求成功，就算有效
        # resp_headers = r.headers
        if conf.validate_HEADER in resp_headers.keys() and conf.validate_KEYWORD in resp_headers[conf.validate_HEADER]:
            # if r.status_code == 200:
            return True
        else:
            # log.info(resp_headers)
            return False

    except Exception:
        return False


@ProxyValidator.addHttpsValidator
def httpsTimeOutValidator(proxy):
    """https检测超时"""

    proxies = {"http": "http://{proxy}".format(proxy=proxy), "https": "https://{proxy}".format(proxy=proxy)}
    try:
        r = requests.head(conf.httpsUrl, headers=HEADER, proxies=proxies, timeout=conf.verifyTimeout, verify=False)
        return True if r.status_code == 200 else False
    except Exception:
        return False
