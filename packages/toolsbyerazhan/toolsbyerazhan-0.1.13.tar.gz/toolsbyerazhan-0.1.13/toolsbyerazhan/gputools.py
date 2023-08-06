'''
#查看gpu能否使用
旧版
print(tf.test.is_gpu_available())
新版
#可不加experimental
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
'''

'''
import torch
#查看torch的gpu版本是否安装成功
print(torch.cuda.is_available())
'''

'''
#ubuntu命令行查看gpu使用情况
#nvidia-smi
#删除占用gpu内存进程
#kill -9 pid
'''

'''
#使用方法
旧版:
import tensorflow as tf
if tf.config.experimental.list_physical_devices('GPU'):
    from toolsbyerazhan.gputools import set_gpu_memory_tf
    set_gpu_memory_tf()

新版:
import toolsbyerazhan as tbe
tbe.set_gpu_memory_tf()
'''
def set_gpu_memory_tf():
    #一般要用到本函数的,都已经安装了tensorflow
    
    import tensorflow as tf
    if tf.config.experimental.list_physical_devices('GPU'):
        print("set gpu memory for tensorflow")
        gpus = tf.config.experimental.list_physical_devices('GPU')
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)

