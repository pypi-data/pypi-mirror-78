import tensorflow as tf

#-----------------------------------------------------------------------------------------------------
def test_non_tgt_mask():
    qlen,mlen = 5,3#0
    attn_mask = tf.ones([qlen,qlen],dtype = tf.float32)
    mask_u = tf.linalg.band_part(attn_mask,0,-1)
    print("mask_u.numpy():\n",mask_u.numpy())
    
    non_tgt_mask = -tf.eye(qlen,dtype = tf.float32)
    print("non_tgt_mask.numpy():\n",non_tgt_mask.numpy())
    if mlen > 0:
        non_tgt_mask = tf.concat([tf.zeros([qlen,mlen],dtype =tf.float32),non_tgt_mask],axis = -1)
    print("non_tgt_mask.numpy():\n",non_tgt_mask.numpy())
    #维度是[qlen,qlen or klen],后续要与attn_mask相加前扩维成[qlen,qlen or klen,1(bsz),1(num_head?)]
'''
mask_u.numpy():
[[1. 1. 1. 1. 1.]
 [0. 1. 1. 1. 1.]
 [0. 0. 1. 1. 1.]
 [0. 0. 0. 1. 1.]
 [0. 0. 0. 0. 1.]]

mlen = 0
non_tgt_mask.numpy():
[[-1. -0. -0. -0. -0.]
 [-0. -1. -0. -0. -0.]
 [-0. -0. -1. -0. -0.]
 [-0. -0. -0. -1. -0.]
 [-0. -0. -0. -0. -1.]]

mlen = 3
non_tgt_mask.numpy():
[[ 0.  0.  0. -1. -0. -0. -0. -0.]
 [ 0.  0.  0. -0. -1. -0. -0. -0.]
 [ 0.  0.  0. -0. -0. -1. -0. -0.]
 [ 0.  0.  0. -0. -0. -0. -1. -0.]
 [ 0.  0.  0. -0. -0. -0. -0. -1.]]

'''
#-----------------------------------------------------------------------------------------------------
def test_seg_mat(qlen = 5, mlen = 3):
    f = int(qlen * 0.6)
    ids = [0]*f + [1]*(qlen-f)
    bsz = 1#测试只看1个batch_size
    token_type_ids = tf.convert_to_tensor([ids],dtype = tf.int32)
    token_type_ids = tf.reshape(token_type_ids,[qlen,bsz])
   
    if mlen == 0:
        cat_ids =token_type_ids
    if mlen > 0:
        mem_pad = tf.zeros([mlen, bsz], dtype=tf.int32)
        cat_ids = tf.concat([mem_pad, token_type_ids], 0)

    seg_mat = tf.cast(tf.logical_not(tf.equal(token_type_ids[:, None], cat_ids[None, :])), tf.int32)

    ans = seg_mat[:,:,0]
    print(ans.numpy())
'''
mlen = 0,ans = 
[[0 0 0 1 1]
 [0 0 0 1 1]
 [0 0 0 1 1]
 [1 1 1 0 0]
 [1 1 1 0 0]]

mlen = 3,ans =
[[0 0 0 0 0 0 1 1]
 [0 0 0 0 0 0 1 1]
 [0 0 0 0 0 0 1 1]
 [1 1 1 1 1 1 0 0]
 [1 1 1 1 1 1 0 0]]
'''
#-----------------------------------------------------------------------------------------------------
def test_pos_emb():
    #其实就是self.relative_positional_encoding(qlen,klen,bsz=bsz,dtype = tf.float32)
    qlen,mlen = 5,3#0 or 3
    klen = qlen + mlen
    bsz = 1
    d_model = 8#512    
    attn_type = "uni"#"bi" or "uni"
    bi_data = False#暂时不知道有什么用，双倍的数据?
    clamp_len = 0#截断值,超过这个距离(>0)的通通按这个距离算
    
    def positional_embedding(pos_seq, inv_freq, bsz=None):
        sinusoid_inp = tf.einsum("i,d->id", pos_seq, inv_freq)
        print("sinusoid_inp.numpy()\n",sinusoid_inp.numpy())
        pos_emb = tf.concat([tf.sin(sinusoid_inp), tf.cos(sinusoid_inp)], axis=-1)
        #erazhan:这样拼接是把奇数都放一起,把偶数都放一起,后续怎么word embedding(观察它的维度)拼接呢??
        
        pos_emb = pos_emb[:, None, :]

        if bsz is not None:
            pos_emb = tf.tile(pos_emb, [1, bsz, 1])

        return pos_emb

    freq_seq = tf.range(0,d_model,2)
    freq_seq = tf.cast(freq_seq,dtype = tf.float32)
    print("freq_seq.numpy():\n",freq_seq.numpy())

    inv_freq = 1 / (10000 ** (freq_seq / d_model))
    print("inv_freq.numpy():\n",inv_freq.numpy())
    if attn_type == "bi":##双向,这个beg,end有什么用,先假设qlen=3,mlen=2,klen=qlen+mlen=5
        # beg, end = klen - 1, -qlen
        beg, end = klen, -qlen##双向8,-5由8->-5这个是表示距离？
    elif attn_type == "uni":##单向
        # beg, end = klen - 1, -1
        beg, end = klen, -1#应该用上面那个，后续再看
    #为什么单向是klen -> 0,双向就是klen -> 0 -> -qlen
    if bi_data:
        pass#搞懂了bi_data再来补充
    else:
        fwd_pos_seq = tf.range(beg, end, -1.0)
        fwd_pos_seq = tf.cast(fwd_pos_seq,dtype = tf.float32)
        print("fwd_pos_seq.numpy()\n",fwd_pos_seq.numpy())
        if clamp_len > 0:
            fwd_pos_seq = tf.clip_by_value(fwd_pos_seq,-clamp_value,clamp_value)
        pos_emd = positional_embedding(fwd_pos_seq,inv_freq)
    print("pos_emd:\n",pos_emd)
    #bi&mlen=0:[10,1,8]
    #bi&mlen=3:[13,1,8]
    #uni&mlen=0:[6,1,8]
    #ubi&mlen=3:[9,1,8]
#-----------------------------------------------------------------------------------------------------
def test_uni_mask(qlen = 5, mlen = 4, same_length = False, dtype=tf.float32):
    """
        Creates causal attention mask. Float mask where 1.0 indicates masked, 0.0 indicates not-masked.

        Args:
            qlen: TODO Lysandre didn't fill
            mlen: TODO Lysandre didn't fill

        ::

                  same_length=False:      same_length=True:
                  <mlen > <  qlen >       <mlen > <  qlen >
               ^ [0 0 0 0 0 1 1 1 1]     [0 0 0 0 0 1 1 1 1]
                 [0 0 0 0 0 0 1 1 1]     [1 0 0 0 0 0 1 1 1]
            qlen [0 0 0 0 0 0 0 1 1]     [1 1 0 0 0 0 0 1 1]
                 [0 0 0 0 0 0 0 0 1]     [1 1 1 0 0 0 0 0 1]
               v [0 0 0 0 0 0 0 0 0]     [1 1 1 1 0 0 0 0 0]

    """
    attn_mask = tf.ones([qlen, qlen], dtype=dtype)
    mask_u = tf.linalg.band_part(attn_mask, 0, -1)
    mask_dia = tf.linalg.band_part(attn_mask, 0, 0)
    attn_mask_pad = tf.zeros([qlen, mlen], dtype=dtype)
    ret = tf.concat([attn_mask_pad, mask_u - mask_dia], 1)
    if same_length:
        mask_l = tf.linalg.band_part(attn_mask, -1, 0)
        #注意第1项中的ret[:,:qlen]中第2维是到qlen
        ret = tf.concat([ret[:, :qlen] + mask_l - mask_dia, ret[:, qlen:]], 1)
    print("ret.numpy():\n",ret.numpy())
    return ret
#-----------------------------------------------------------------------------------------------------
def test_cache_mem():
    """cache hidden states into memory."""
    """
    1、mlen < qlen
    2、reuse_len = None,从curr_out中选最后mlen个;
    3、reuse_len > 0,从curr_out中选前reuse_len(放后面)个,和prev_mem(放前面)拼接,选最后mlen个
    注:reuse_len < mlen才会用到prev_mem
    """
    qlen, mlen, reuse_len = 5, 3, 2
    bsz = 1
    d_model = 13
    
    curr_out = tf.reshape(tf.range(qlen*bsz*d_model),[qlen,bsz,d_model])#[qlen,bsz,d_model] 
    prev_mem = tf.reshape(tf.range(-mlen*bsz*d_model, 0),[mlen,bsz,d_model])#[mlen,bsz,d_model]
    print("curr_out.numpy():\n",curr_out.numpy())
    print("prev_mem.numpy():\n",prev_mem.numpy())

    if reuse_len is not None and reuse_len > 0:
        curr_out = curr_out[: reuse_len]

    if prev_mem is None:
        new_mem = curr_out[-mlen :]
    else:
        new_mem = tf.concat([prev_mem, curr_out], 0)[-mlen :]
    print("new_mem:\n",new_mem)
    #return tf.stop_gradient(new_mem)
#-----------------------------------------------------------------------------------------------------
def test_rel_shift():
    x = tf.range(2*3*4*5)
    x = tf.reshape(x,[2,3,4,5])
    shape = x.shape.as_list()

    print("原始数据x:\n",x)
    y = tf.reshape(x[:,1:,:,:],[shape[0],shape[1]-1,shape[2],shape[3]])

    print("直接转换(错误做法)y:\n",y)

    z = tf.reshape(x,[shape[1],shape[0],shape[2],shape[3]])

    z = z[1:,...]
    z = tf.reshape(z,[shape[0],shape[1]-1,shape[2],shape[3]])
    print("间接转换(正确做法)z:\n",z)
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------

'''
#根据input_ids产生,经过该层不用自己创建mask,pad位上是0(也就是attention_mask)
from xlnet_layers import CreateMask

#[batch_size,seq_length]
inputs = tf.convert_to_tensor([[0,2,1],[0,1,1]],dtype = tf.int32)
masks = CreateMask(mask_value=1)(inputs)
print(inputs.numpy())
print(masks.numpy())
'''
#-----------------------------------------------------------------------------------------------------

if __name__ == "__main__":
        
    import toolsbyerazhan as tbe
    tbe.set_gpu_memory_tf()

    #test_non_tgt_mask()
    #test_seg_mat()
    #test_pos_emb()
    #test_uni_mask(same_length = True)
    #test_cache_mem()
    test_rel_shift()
