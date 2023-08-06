import tensorflow as tf
'''点乘'''
def test_matmul(a = 2,b = 3,c = 4, transpose_b = False):
    tips = """
    tf.matmul or tf.linalg.matmul
    a = 2
    b = 3
    c = 4
    transpose_b = False
    """
    
    x1 = tf.cast(tf.reshape(tf.range(a*b),(a,b)),dtype = tf.float32)
    
    x2 = tf.cast(tf.reshape(tf.range(a*b,b*(a+c)),(b,c)),dtype = tf.float32)
    
    if transpose_b:
        #x2 = tf.reshape(x2,(c,b))
        x2 = tf.transpose(x2)
        
    #ans = tf.matmul(x1,x2,transpose_b = transpose_b)
    ans = tf.linalg.matmul(x1,x2,transpose_b = transpose_b)
    print("ans:\n",ans)
if __name__ == "__main__":
    test_matmul(transpose_b = True)

