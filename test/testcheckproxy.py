# -*- coding: utf-8 -*-
# Created by QQ 253713 on 2022-02-07

import queue
import random
import re
import threading
import time
from os import system as terminal
from sys import argv

import requests
import urllib3
import xlrd
import xlwt
from colorama import Fore, Style
from xlutils.copy import copy


def write_excel_xls(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("xls格式表格写入数据成功！")


def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")


def read_excel_xls(path):
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    for i in range(0, worksheet.nrows):
        for j in range(0, worksheet.ncols):
            print(worksheet.cell_value(i, j), "\t", end="")  # 逐行逐列读取数据
        print()


book_name_xls = 'check_url_file_result.xls'

sheet_name_xls = 'test'

value_title = [["url", "total", "good", "bad", "repeat", "live"], ]

write_excel_xls(book_name_xls, sheet_name_xls, value_title)

URL = "http://httpbin.org"
CMD_CLEAR_TERM = "clear"
TIMEOUT = 10
validate_HEADER = 'Server'
validate_KEYWORD = 'gunicorn'

CRAWL_EXIT = False
PARSE_EXIT = False
GOOD_PROXY = ''
GOODS = 0


def check_proxy(proxy):
    """
        Function for check proxy return ERROR
        if proxy is Bad else
        Function return None
    """
    try:
        ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        ]
        ua = random.choice(ua_list)

        header = {'User-Agent': ua,
                  'Accept': '*/*',
                  'Connection': 'keep-alive',
                  'Accept-Language': 'zh-CN,zh;q=0.8'}

        verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
        _proxy = re.findall(verify_regex, proxy)

        if len(_proxy) == 1 and _proxy[0] in proxy:
            pass
        else:
            return False

        # print(Fore.LIGHTYELLOW_EX + 'Checking ' + proxy)

        r = requests.head(URL, proxies={'http': 'http://' + _proxy[0]}, headers=header, timeout=TIMEOUT)

        resp_headers = r.headers
        if validate_HEADER in resp_headers.keys() and validate_KEYWORD in resp_headers[validate_HEADER]:
            return True
        else:
            return False

    except requests.exceptions.ConnectTimeout:
        print(Fore.LIGHTRED_EX + 'Error,Timeout!')
        return False
    except requests.exceptions.ConnectionError:
        print(Fore.LIGHTRED_EX + 'Error!')
        return False
    except requests.exceptions.HTTPError:
        print(Fore.LIGHTRED_EX + 'HTTP ERROR!')
        return False
    except requests.exceptions.Timeout:
        print(Fore.LIGHTRED_EX + 'Error! Connection Timeout!')
        return False
    except urllib3.exceptions.ProxySchemeUnknown:
        print(Fore.LIGHTRED_EX + 'ERROR unkown Proxy Scheme!')
        return False
    except requests.exceptions.TooManyRedirects:
        print(Fore.LIGHTRED_EX + 'ERROR! Too many redirects!')
        return False


def print_help():
    terminal(CMD_CLEAR_TERM)
    print(Fore.LIGHTCYAN_EX)
    print('Usage -> -f <filename> - Check file with proxies')
    print(' -p <proxy> - check only one proxy')
    print(' -u <url> - check server proxy')
    print(' -t <url> - set thread num')
    print(' --help - show this menu')
    print(' - QQ:253713')


def main():
    if len(argv) > 1:
        commands = ['--help', '-h', '-f', '-u', '-p', '-uf']
        global CRAWL_EXIT
        global GOODS
        if argv[1] in commands:
            start = time.time()
            if argv[1] in ['--help', '-h']:
                print_help()
            elif argv[1] in ['-u', ]:
                try:
                    if len(argv) > 3 and argv[3] in ('-t',):
                        thread_num = int(argv[4])
                    else:
                        thread_num = 10

                    proxies = requests.get(argv[2]).text

                    proxies = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', proxies)

                    proxies_set = set(proxies)
                    repeat = str(len(proxies) - len(proxies_set))
                    pageQueue = queue.Queue()
                    for i in proxies_set:
                        pageQueue.put(i)
                    threadcrawl = []

                    for i in range(thread_num):
                        threadName = "thread-" + str(i)
                        thread = ThreadCrawl(threadName, pageQueue)
                        thread.setDaemon = True
                        thread.start()
                        threadcrawl.append(thread)

                    while pageQueue.qsize() != 0:
                        pass

                    CRAWL_EXIT = True

                    print("pageQueue is numpty")

                    for thread in threadcrawl:
                        thread.join()

                    file_with_goods = open('good.txt', 'w')
                    file_with_goods.write(GOOD_PROXY)
                    file_with_goods.close()
                    rate = GOODS / len(proxies) * 100
                    end = time.time()

                    time_lauch = end - start
                    print(
                        Fore.LIGHTGREEN_EX + ' ,Total: ' + str(len(proxies)) + ', Good: ' + str(
                            GOODS) + ', Bad: ' + str(
                            len(proxies) - GOODS) + ', Repeat: ' + repeat + ',Live: %d' % rate + '%')
                    print(Fore.LIGHTYELLOW_EX + 'Have nice day! time: %.2f' % time_lauch)
                    print()
                except:
                    print(Fore.LIGHTRED_EX + 'Error!\n')

            elif argv[1] in ('-f',):
                try:
                    if len(argv) > 3 and argv[3] in ('-t', '-thread', '--thread'):
                        thread_num = int(argv[4])
                    else:
                        thread_num = 10

                    with open(argv[2], "r") as f:
                        proxies = f.read().splitlines()

                    proxies_set = set(proxies)
                    repeat = str(len(proxies) - len(proxies_set))
                    pageQueue = queue.Queue()
                    for i in proxies_set:
                        pageQueue.put(i)

                    threadcrawl = []

                    for i in range(thread_num):
                        threadName = "thread-" + str(i)
                        thread = ThreadCrawl(threadName, pageQueue)
                        thread.setDaemon = True
                        thread.start()
                        threadcrawl.append(thread)

                    while pageQueue.qsize() != 0:
                        pass

                    CRAWL_EXIT = True

                    print("pageQueue is numpty")

                    for thread in threadcrawl:
                        thread.join()

                    file_with_goods = open('good.txt', 'w')
                    file_with_goods.write(GOOD_PROXY)
                    file_with_goods.close()
                    rate = GOODS / len(proxies) * 100
                    end = time.time()

                    time_lauch = end - start
                    print(
                        Fore.LIGHTGREEN_EX + ' ,Total: ' + str(len(proxies)) + ', Good: ' + str(
                            GOODS) + ', Bad: ' + str(
                            len(proxies) - GOODS) + ', Repeat: ' + repeat + ',Live: %d' % rate + '%')
                    print(Fore.LIGHTYELLOW_EX + 'Have nice day! time: %.2f' % time_lauch)
                    print()
                except FileNotFoundError:
                    print(Fore.LIGHTRED_EX + 'Error!\nFile Not found!')
                except IndexError:
                    print(Fore.LIGHTRED_EX + 'Error!\nMissing filename!')
            elif argv[1] in ('-uf',):
                all_xls_data = []

                try:
                    if len(argv) > 3 and argv[3] in ('-t', '-thread', '--thread'):
                        thread_num = int(argv[4])
                    else:
                        thread_num = 10

                    with open(argv[2], "r") as f:
                        urlfile = f.read().splitlines()

                    rep_all = ""
                    pageQueue = queue.Queue()

                    for u in urlfile:
                        CRAWL_EXIT = False
                        GOODS = 0
                        try:
                            proxies = requests.get(u, timeout=5, allow_redirects=True).text
                        except:
                            one_rep = "[-]" + u
                            rep_all += one_rep + "\n"
                            tmp = [u, '0', '0', '0', '0', '0']

                            all_xls_data.append(tmp)

                            continue

                        proxies = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', proxies)

                        proxies_set = set(proxies)
                        repeat = str(len(proxies) - len(proxies_set))

                        # 容错
                        if len(proxies_set) == 0:
                            one_rep = "[-]" + u
                            rep_all += one_rep + "\n"
                            tmp = [u, '0', '0', '0', '0', '0']

                            all_xls_data.append(tmp)

                            continue

                        for i in proxies_set:
                            pageQueue.put(i)

                        threadcrawl = []

                        for i in range(thread_num):
                            threadName = u + ' -' + str(i)
                            thread = ThreadCrawl(threadName, pageQueue)
                            thread.start()
                            threadcrawl.append(thread)

                        while pageQueue.qsize() != 0:
                            pass

                        CRAWL_EXIT = True

                        print("pageQueue is numpty")

                        for thread in threadcrawl:
                            thread.join()

                        rate = GOODS / len(proxies) * 100

                        one_rep = "[+]" + u + ' ,Total: ' + str(len(proxies)) + ', Good: ' + str(
                            GOODS) + ', Bad: ' + str(
                            len(proxies) - GOODS) + ', Repeat: ' + repeat + ',Live: %d' % rate + '%'

                        rep_all += one_rep + "\n"
                        print(one_rep)

                        tmp = [u, str(len(proxies)), str(
                            GOODS), str(
                            len(proxies) - GOODS), repeat, '%.2f' % rate + '%']

                        all_xls_data.append(tmp)
                        time.sleep(5)

                    with open("check_result.txt", 'w') as f:
                        f.write(rep_all)

                    write_excel_xls_append(book_name_xls, all_xls_data)

                    end = time.time()
                    time_lauch = end - start
                    print('Have nice day! time: %.2f' % time_lauch)
                    print()

                except FileNotFoundError:
                    print(Fore.LIGHTRED_EX + 'Error!\nFile Not found!')
                except IndexError:
                    print(Fore.LIGHTRED_EX + 'Error!\nMissing filename!')
            elif argv[1] in ('-p',):
                try:
                    if check_proxy(argv[2]):
                        print(Fore.LIGHTGREEN_EX + 'GOOD PROXY ' + argv[2])
                    else:
                        print(Fore.LIGHTRED_EX + 'BAD PROXY ' + argv[2])
                except IndexError:
                    print(Fore.LIGHTRED_EX + 'Error! Missing proxy!')
        else:
            print(Fore.LIGHTRED_EX + 'Unknown option \"' + argv[1] + '\"')
    else:
        print_help()


class ThreadCrawl(threading.Thread):
    def __init__(self, threadName, pageQueue):

        super(ThreadCrawl, self).__init__()

        self.threadName = threadName

        self.pageQueue = pageQueue

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/60.0.3112.101 Safari/537.36'}

    def run(self):
        # print("start " + self.threadName)
        while not CRAWL_EXIT:

            if self.pageQueue.qsize() == 0:
                print("empty end " + self.threadName)
                break

            proxy = self.pageQueue.get()

            print(Fore.LIGHTCYAN_EX + '===========================================')

            try:
                if check_proxy(proxy):
                    print(Fore.LIGHTGREEN_EX + 'Good proxy ' + proxy)

                    global GOODS, GOOD_PROXY
                    GOOD_PROXY += proxy + "\n"
                    GOODS += 1

                else:
                    print(Fore.LIGHTRED_EX + 'Bad proxy ' + proxy)
                print(Fore.LIGHTCYAN_EX + '=================================================')
            except KeyboardInterrupt:
                print(Fore.LIGHTGREEN_EX + '\nExit.')
                exit()
        # print("end " + self.threadName)


if __name__ == "__main__":
    main()
