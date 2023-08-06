import tensorflow as tf
import numpy as np

#按照函数名进行排序
def test_Activation(activation = 'relu'):
    from tensorflow.keras.layers import Activation
    tips = """
tips:
    params:
    activation:'relu'(default),'gelu','square'
    """
    
    def my_square(x):
        return x**2
        
    def gelu(x):
    	return 0.5 * x * (1.0 + tf.math.erf(x / np.sqrt(2.0)))

    if activation == 'square':
        ac_fun = my_square#自定义的函数要写函数名,不能加引号
    elif activation == 'gelu':
        ac_fun = gelu
    else:
        ac_fun = 'relu'
    layer = Activation(ac_fun)

    inputs = tf.convert_to_tensor([0,-1,2,-3,4,-5,6,-7,8,-9],dtype = tf.float32)

    print(tips)

    print("inputs.numpy():\n",inputs.numpy())

    output = layer(inputs)
    print("output.numpy():\n",output.numpy())

def test_Dot(a1 = 2, a2 = 2):
    from tensorflow.keras.layers import Dot
    tips= """
tips:
    将两个tensor进行point-wise点乘
    
    Dot参数:
    axes：两个tensor各自相乘的维度，比如[2,2]，就表示将x和y的第2维对应相乘（维度从0开始）
    normalize：是否是将两个向量相乘结果标准化，即求余弦相似度

    注意使用方式，Dot内部参数调整位置，需要将x,y写为列表形式[x,y]进行带入Dot层进行call运算

    test_Dot参数:
    axes = [a1,a2],本示例中,a1可为1或2，a2固定为2，它们对应的维度必须相等
    """
    x = tf.convert_to_tensor([[[1,1,1],[2,2,2],[3,3,3]]],dtype=tf.float32)
    y = tf.convert_to_tensor([[[3,3,3],[4,4,4]]],dtype=tf.float32)
    m = tf.keras.layers.Dot(axes=[a1,a2],normalize=False)([x,y])
    print(tips)
    print("x:\n",x)
    print("y:\n",y)
    print("m:\n",m)
    #print(m.numpy())

def test_Dropout(print_remarks = False):
    from tensorflow.keras.layers import Layer,Dropout
    tips = """
tips:
    Dropout层的实现过程:
    1、对每个元素按照概率rate进行丢弃
    2、对剩下没被丢弃的元素乘上1/(1 - rate)
    test_Dropout参数:
    print_remarks：是否print出remarks(理解Dropout时的总结)
    """
    remarks = """
remarks:
    注意在第二种写法中的training=True,它是在Dropout层中的
    call方法的参数,默认为None,如果设定为True,则会在测试
    中展现效果,否则它会自动判断是否在训练中，如果在训练中
    则会实现dropout效果

    https://zhuanlan.zhihu.com/p/32846476
    该网址很好的解释了tf.layers.dropout的原理（另外还讲了BN，后续详细看）

    https://blog.csdn.net/nini_coded/article/details/79302800
    原理是将inputs中每个元素按概率rate随机丢弃，剩下的乘上1/(1-rate)进行rescale
    开始理解错了，以为是从所有元素中选rate*N个进行丢弃
    """

    print(tips)
    if print_remarks:
        print(remarks)
        
    class MyDropout(Layer):
        '''自定义Dropout层'''
        def __init__(self, rate = None, **kwargs):
            super(MyDropout, self).__init__(**kwargs)
            self.rate = rate
        '''不要用自己层，因为暂时做不到让它自己判断是否在训练中，这里只是为了理解dropout的原理实现'''
    
        def call(self, inputs, training = False):

            if training == False:
                return inputs
        
            if self.rate is not None:
            
                mask = tf.random.uniform(shape = tf.shape(inputs),minval = 0, maxval = 1,dtype = tf.float32)
                mask = tf.cast(mask > self.rate, dtype = tf.float32)/(1 - self.rate)
                inputs = inputs * mask

            return inputs

    rate = 0.5
    
    inputs = tf.reshape(tf.range(1,25),(2,3,4))
    inputs = tf.cast(inputs, dtype = tf.float32)

    print("inputs.numpy()\n",inputs.numpy(),'\n')

    #y=tf.nn.dropout(x,rate=0.31)
    ans1 = Dropout(rate = rate)(inputs, training = True)
    ans2 = MyDropout(rate = rate)(inputs, training = True)

    print("MyDropout Layer:\n",ans1.numpy())
    print("Dropout Layer:\n",ans2.numpy())

    #print("tf.reduce_sum(inputs):",tf.reduce_sum(inputs).numpy())
    #print("tf.reduce_sum(ans1):",tf.reduce_sum(ans1).numpy())
    #print("tf.reduce_sum(ans2):",tf.reduce_sum(ans2).numpy())

def test_Reshape():
    from tensorflow.keras.layers import Reshape
    tips = """
tips:
    a.shape:[3,4,10]
    b = Reshape((-1,))(a)
    c = Reshape((5,8))(a)

remarks:
    Reshape层默认将第一维看作batch_size
    接口参数是不包括batch_size维的
    所以除了不考虑batch_size维度
    Reshape的规则和tf.reshape的规则是一样的
    """
    print(tips)
    a = tf.reshape(tf.range(120),(3,4,10))
    b = Reshape((-1,))(a)
    c = Reshape((5,8))(a)
    

    print("a.shape:",a.shape)
    print("b.shape:",b.shape)
    print("c.shape:",c.shape)

#按照函数名进行排序
if __name__ == "__main__":
    #import toolsbyerazhan as tbe
    #tbe.set_gpu_memory_tf()
    #test_Activation('square')
    #test_Dot(1,2)
    #test_Dropout(True)
    test_Reshape()
    pass
