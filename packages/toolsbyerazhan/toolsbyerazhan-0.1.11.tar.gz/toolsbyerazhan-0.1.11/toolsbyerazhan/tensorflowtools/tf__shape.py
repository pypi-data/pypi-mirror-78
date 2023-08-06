import tensorflow as tf

def test_shape(bsz = None, seq_len = 4, hidden_size = 5):
    tips = """
tips:
    params:
    bsz:None,ans is equal to static shape else dynamic shape
    seq_len:4
    hidden_size:6
    """
    if bsz == None:
        from tensorflow.keras import Input
        x = Input((seq_len,hidden_size),dtype = tf.float32)
    else:
        x = tf.range(bsz * seq_len * hidden_size)
        x = tf.reshape(x,[bsz,seq_len,hidden_size])
        x = tf.cast(x,tf.float32)

    static = x.shape.as_list()
    dynamic = tf.shape(x)
    ans = [dynamic[i] if s is None else s for i, s in enumerate(static)]
    print(tips)
    print(ans)
if __name__ == "__main__":
    test_shape()
