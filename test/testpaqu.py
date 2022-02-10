# -*- coding: utf-8 -*-
# Created by QQ 253713 on 2022-02-07
import json
import queue
import threading
from sys import argv

import requests
import xlrd
import xlwt
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


book_name_xls = 'proxy_url2.xls'

sheet_name_xls = 'test'

value_title = [["url", "proxy_number"], ]

write_excel_xls(book_name_xls, sheet_name_xls, value_title)

response = []

bad_url = ""


class ThreadCrawl(threading.Thread):
    def __init__(self, threadName, pageQueue):
        # threading.Thread.__init__(self)
        # 调用父类初始化方法
        super(ThreadCrawl, self).__init__()
        # 线程名
        self.threadName = threadName
        # 页码队列
        self.pageQueue = pageQueue

        # 请求报头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}

    def getHtml(self, url):
        retry_count = 3
        while retry_count > 0:
            try:
                html = requests.get(url, timeout=5).text
                return html
            except Exception:
                retry_count -= 1
        return None

    def run(self):
        print("启动 " + self.threadName)
        while not CRAWL_EXIT:
            try:
                page = self.pageQueue.get(False)
                url = page + "/count"
                num = self.getHtml(url)

                if num and "W3C" not in num:
                    if "total" in num:
                        num = json.loads(num)
                        proxy_num = num['count']['total']
                    else:
                        proxy_num = num
                    tmp = [page + "/count", proxy_num]
                    print(tmp)
                    response.append(tmp)
                else:
                    print('[-] ' + url)
                    bad_url += page + "\n"

                """
                        当页面只返回一个代理数量时 用上面方法
                        当页面返回json时 ，用下面方法
                """

                # if "total" not in num:
                #     url = page + "/get_status/"
                #     num = self.getHtml(url)
                #
                #     if "useful_proxy" in num:
                #         num = json.loads(num)
                #         proxy_num = num['useful_proxy']
                #     elif "count" in num:
                #         num = json.loads(num)
                #         proxy_num = num['count']
                #     else:
                #         print("========================")
                #         print('[-] ' + url)
                #         print(num)
                #         print("========================")
                #         continue
                #
                #     tmp = [page + "/get_status", proxy_num]
                #     print(tmp)
                #     response.append(tmp)
                #
                # else:
                #     print(num)
                #     num = json.loads(num)
                #
                #     proxy_num = num['count']['total']
                #     tmp = [page + "/count", proxy_num]
                #     print(tmp)
                #
                #     response.append(tmp)

            except KeyboardInterrupt:
                exit()

        print("结束 " + self.threadName)


CRAWL_EXIT = False
PARSE_EXIT = False


def main():
    if len(argv) > 1 and argv[1] in ('-f',):
        filename = int(argv[2])
    else:
        filename = "url.txt"

    with open(filename, "r") as f:
        urls = f.read()

    urllist = urls.splitlines()
    pageQueue = queue.Queue()
    for i in urllist:
        pageQueue.put(i)

    threadcrawl = []

    for i in range(20):
        threadName = "thread-" + str(i)
        thread = ThreadCrawl(threadName, pageQueue)
        thread.setDaemon = True
        thread.start()
        threadcrawl.append(thread)

    while not pageQueue.empty():
        pass

    global CRAWL_EXIT
    CRAWL_EXIT = True

    print("pageQueue is numpty")

    for thread in threadcrawl:
        thread.join()

    write_excel_xls_append(book_name_xls, response)


if __name__ == "__main__":
    main()
