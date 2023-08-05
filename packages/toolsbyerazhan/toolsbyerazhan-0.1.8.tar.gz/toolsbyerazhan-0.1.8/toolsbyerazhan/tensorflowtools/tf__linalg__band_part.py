import tensorflow as tf

'''
原版本:tf.matrix_band_part
新版本:tf.linalg.band_part
作用是根据对角线的位置读取矩阵特定位置上的数据
可以作用在多维张量上，使用时参考官方文档的解释
二维的好理解一些

参数(二维):
input:就是矩阵
num_lower:整数,控制下三角,0就是只保留对角线元素不动,-1表示保留所有下三角元素,n=1表示保留对角线下n=1排
num_upper:整数,控制上三角,类似num_lower
name:操作名称

tf.linalg.band_part(inputs,0,0)就是只保留对角线的元素，其余元素均为0
tf.linalg.band_part(inputs,-1,-1)不做任何修改
'''

def test_band_part(lower = 0, upper = 0, r = 5, c = 6, use_ones = False):
    
    tips = '''
tip:
    params(default):
    lower:0
    upper:0
    r:5
    c:6
    use_ones:False

    examples:
    test_band_part()
    test_band_part(1,-1,3,5)
    test_band_part(1,2,use_ones = True)
    '''
    
    if use_ones:
        inputs = tf.ones([r,r],dtype = tf.float32)
    else:
        inputs = tf.reshape(tf.range(r*c),[r,c])
        inputs = tf.cast(inputs,dtype = tf.float32)
    print(tips)
    print("inputs.numpy():\n",inputs.numpy())
    
    ans = tf.linalg.band_part(inputs,lower,upper)
    print("ans.numpy():\n",ans.numpy())

if __name__ == "__main__":
    import toolsbyerazhan as tbe
    test_band_part()
    #pass
