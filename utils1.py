import hashlib

salt = 'vin2018'

import time


def log(*args, **kwargs):
    print(*args, **kwargs)


def encryption(salt, password):
    hash = hashlib.sha256()
    hash.update((salt + password).encode('utf-8'))
    return hash.hexdigest()


# def time_flow(start, now):
#     interval = int(now - start)
#     minute_flow = int(interval / 60)
#     if interval < 60:
#         flow_str = '{} 秒前'.format(interval)
#     elif interval in range(60, 3600):
#         flow = int(interval / 60)
#         flow_str = '{} 分钟前'.format(flow)
#     elif interval in range(3600, 86400):
#         flow = int(interval / 3600)
#         flow_str = '{} 小时前'.format(flow)
#     elif interval in range(86400, 2592000):
#         flow = int(interval / 86400)
#         flow_str = '{} 天前'.format(flow)
#     elif interval in range(2592000, 31104000):
#         flow = int(interval / 2592000)
#         flow_str = '{} 月前'.format(flow)
#     else:
#         flow = int(interval / 31104000)
#         flow_str = '{} 年前'.format(flow)
#     return flow_str


# def change_time(times):
#     format = '%Y/%m/%d %H:%M:%S'
#     value = time.localtime(times)
#     dt = time.strftime(format, value)
#     return dt
