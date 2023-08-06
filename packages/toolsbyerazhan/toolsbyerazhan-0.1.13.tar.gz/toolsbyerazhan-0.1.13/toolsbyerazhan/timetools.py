import time

def get_local_time(is_print = True):
    '''
    返回当前本地时间字符串格式
    is_print = True:打印当前时间
    '''
    local_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    if is_print:
        print(local_time)
    return local_time


