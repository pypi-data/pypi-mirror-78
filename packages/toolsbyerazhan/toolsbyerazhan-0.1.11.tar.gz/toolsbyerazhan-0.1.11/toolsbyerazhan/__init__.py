#from toolsbyerazhan import *#无效
#from toolsbyerazhan import timetools,gpu4tftools#有效

#可直接用timetools.py和gputools.py文件中的所有函数
#from .timetools import *
#from .gputools import *

from . import gputools,jsontools,layers,models,ostools,timetools,tensorflowtools,transformers
from .gputools import set_gpu_memory_tf
set_gpu_memory_tf()
from .quicktools import whether_to_transfer
