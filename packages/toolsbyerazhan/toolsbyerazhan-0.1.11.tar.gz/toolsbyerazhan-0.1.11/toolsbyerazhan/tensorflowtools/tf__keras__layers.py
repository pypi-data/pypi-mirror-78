import tensorflow as tf
import numpy as np

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

if __name__ == "__main__":
    import toolsbyerazhan as tbe
    #tbe.set_gpu_memory_tf()
    test_Activation('square')
    #pass
