# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     setting.py
   Description :   配置文件
   Author :        JHao
   date：          2019/2/15
-------------------------------------------------
   Change Activity:
                   2019/2/15:
-------------------------------------------------
"""

BANNER = r"""
****************************************************************
*** ______  ********************* ______ *********** _  ********
*** | ___ \_ ******************** | ___ \ ********* | | ********
*** | |_/ / \__ __   __  _ __   _ | |_/ /___ * ___  | | ********
*** |  __/|  _// _ \ \ \/ /| | | ||  __// _ \ / _ \ | | ********
*** | |   | | | (_) | >  < \ |_| || |  | (_) | (_) || |___  ****
*** \_|   |_|  \___/ /_/\_\ \__  |\_|   \___/ \___/ \_____/ ****
****                       __ / /                          *****
************************* /___ / *******************************
*************************       ********************************
****************************************************************
"""

VERSION = "2.4.0"

# ############### server config ###############
HOST = "0.0.0.0"

PORT = 6020

# ############### database config ###################
# db connection uri
# example:
#      Redis: redis://:password@ip:port/db
#      Ssdb:  ssdb://:password@ip:port
DB_CONN = 'redis://:proxy666@127.0.0.1:6379/0'

# proxy table name
TABLE_NAME = 'use_proxy'

# ###### config the proxy fetch function ######
PROXY_FETCHER = [
    # "freeProxy01",
    "customProxy00",
    # "customProxy01",
    # "customProxy01",
    # "freeProxy03",
    # "freeProxy04",
    # "freeProxy05",
    # "freeProxy06",
    # "freeProxy07",
    # "freeProxy08",
    # "freeProxy09",
    # "freeProxy10"
]

# ############# proxy validator #################
# 代理验证目标网站
HTTP_URL = "http://www.baidu.com"
HTTPS_URL = "https://www.qq.com"
VALIDATE_HEADER = 'Server'  # 仅用于HEAD验证方式，百度响应头Server字段KEYWORD可填：bfe   httpbin相应为 gunicorn
VALIDATE_KEYWORD = 'bfe'

# check 时的线程数量
CHECK_THREAD = 1000

# 代理验证时超时时间
VERIFY_TIMEOUT = 10

# 近PROXY_CHECK_COUNT次校验中允许的最大失败次数,超过则剔除代理
MAX_FAIL_COUNT = 1

# 近PROXY_CHECK_COUNT次校验中允许的最大失败率,超过则剔除代理
# MAX_FAIL_RATE = 0.1

# proxyCheck时代理数量少于POOL_SIZE_MIN触发抓取
POOL_SIZE_MIN = CHECK_THREAD * 2

# ############# scheduler config #################

# Set the timezone for the scheduler forcely (optional)
# If it is running on a VM, and
#   "ValueError: Timezone offset does not match system offset"
#   was raised during scheduling.
# Please uncomment the following line and set a timezone for the scheduler.
# Otherwise it will detect the timezone from the system automatically.

TIMEZONE = "Asia/Shanghai"
