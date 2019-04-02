import time


def created_time():
    current_time = time.localtime()
    return current_time


def change_time(times):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(times)
    dt = time.strftime(format, value)
    return dt


def time_flow(start, now):
    interval = int(now - start)
    minute_flow = int(interval / 60)
    if interval < 60:
        flow_str = '{} 秒前'.format(interval)
    elif interval in range(60, 3600):
        flow = int(interval / 60)
        flow_str = '{} 分钟前'.format(flow)
    elif interval in range(3600, 86400):
        flow = int(interval / 3600)
        flow_str = '{} 小时前'.format(flow)
    elif interval in range(86400, 2592000):
        flow = int(interval / 86400)
        flow_str = '{} 天前'.format(flow)
    elif interval in range(2592000, 31104000):
        flow = int(interval / 2592000)
        flow_str = '{} 月前'.format(flow)
    else:
        flow = int(interval / 31104000)
        flow_str = '{} 年前'.format(flow)
    return flow_str


#     1 min ~ 60 min
#     60s ~ 3600s

# 1519562217.8605072
# 1519562233.386086

def __main():
    # print(creat_time())
    # print(test())
    print(int(time.time()))
    print(time_flow(0, 1519562217))
    print(time_flow(1519562233, int(time.time())))
    print(change_time(1519562233))


__main()