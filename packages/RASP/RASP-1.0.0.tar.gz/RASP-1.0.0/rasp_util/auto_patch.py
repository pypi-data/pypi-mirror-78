"""
整合所有agent,此文件应该用户程序启动之前执行
"""

import sentry_sdk
import os

# 参数 'path' 可以换成任意存在的环境变量名
# 如果不存在，则输出None
sentry_dsn = os.environ.get('sentry_dsn')

# ---------------测试使用后期删掉--------------
if sentry_dsn is None:
    sentry_dsn = 'https://29022e09671a480c9dc3e9a1bd92b73e@sentry.micloud.d.xiaomi.net/268'

if sentry_dsn:
    sentry_sdk.init(dsn=sentry_dsn)

from monkey_patch import sql_patch

sql_patch.patch()

from monkey_patch import command_patch

command_patch.patch()

from monkey_patch import file_patch

file_patch.patch()

from monkey_patch import http_server_patch

http_server_patch.patch()

print("end")
