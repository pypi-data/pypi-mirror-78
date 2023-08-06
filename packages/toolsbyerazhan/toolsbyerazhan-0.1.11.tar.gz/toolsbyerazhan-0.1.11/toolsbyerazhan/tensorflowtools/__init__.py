#tensorflowtools专门用于理解tensorflow中的函数
#用__代替.例如tf.linalg.band_part用tf__linalg__band_part代替
#一个.py文件只有一个函数,文件名对于tf中从tf目录到具体函数名,
#它内部的函数命名规则是test_函数名,例如test_band_part

from .tf__keras__layers import test_Activation
from .tf__linalg__band_part import test_band_part
from .tf__linalg__matmul import test_matmul
from .tf__shape import test_shape
