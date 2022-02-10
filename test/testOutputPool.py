# -*- coding: utf-8 -*-
# Created by QQ 253713 on 2022-02-07
import queue
import re
import threading
import time
from sys import argv

import requests


def get_proxy():
    return requests.get("http://185.194.148.73:5010/get/").json()


def delete_proxy(proxy):
    print('del proxy')
    requests.get("http://185.194.148.73:5010/delete/?proxy={}".format(proxy))


# use proxy
def getHtmlProxy(url):
    retry_count = 3
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.get(url, timeout=3, proxies={"http": "http://{}".format(proxy)})
            return html
        except Exception:
            retry_count -= 1
    # del proxy
    delete_proxy(proxy)
    return None


# no proxy
def getHtml(url):
    retry_count = 3
    while retry_count > 0:
        try:
            html = requests.get(url, timeout=3)
            return html
        except Exception:
            retry_count -= 1
    return None


proxy_list = []
bad_url = ""


class ThreadCrawl(threading.Thread):
    def __init__(self, threadName, pageQueue):

        super(ThreadCrawl, self).__init__()

        self.threadName = threadName

        self.pageQueue = pageQueue

    def run(self):
        print("start  " + self.threadName)
        while not CRAWL_EXIT:
            try:
                if self.pageQueue.empty():
                    print("empty end " + self.threadName)
                    break

                page = self.pageQueue.get(False)

                html = getHtml(page)

                if html.status_code == 200:
                    resp = html.text
                    tmp_list = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', resp)
                    if tmp_list:
                        global proxy_list
                        proxy_list += tmp_list
                        print('[+] ' + page)
                    else:
                        print('[-] ' + page)
                        global bad_url
                        bad_url += page + "\n"
                else:
                    pass

                time.sleep(3)
            except:
                pass
        print("end " + self.threadName)


CRAWL_EXIT = False


def Output(filename):
    global proxy_list
    proxy_list = set(proxy_list)
    lists = [line + "\n" for line in proxy_list]

    with open(filename, "w") as f:
        f.writelines(lists)

    with open("Output_bad_url.txt", "a") as f:
        f.write(bad_url)


def main():
    start = time.time()

    if len(argv) > 1 and argv[1] in ('-f',):
        filename = str(argv[2])
    else:
        filename = "url.txt"

    if len(argv) > 3 and argv[3] in ('-o',):
        Outname = int(argv[4])
    else:
        Outname = "ip.txt"

    with open(filename, "r") as f:
        url = f.read().splitlines()

    urllist = url
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

    Output(Outname)

    end = time.time()

    global proxy_list
    print("Good , total proxy : " + str(len(proxy_list)) + "!")
    print("It runs for :" + str(end - start) + "s !")


if __name__ == "__main__":
    main()
