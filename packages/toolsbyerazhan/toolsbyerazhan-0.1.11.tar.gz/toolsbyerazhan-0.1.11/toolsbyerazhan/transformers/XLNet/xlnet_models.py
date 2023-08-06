import tensorflow as tf
import numpy as np

#from tensorflow.keras import Input
#from tensorflow.keras.models import Model
#from tensorflow.keras.layers import Layer,Embedding

#from xlnet_layers import EmbeddingRet,EmbeddingSim

#from xlnet_configuration import XLNetConfig 
from .xlnet_configuration import XLNetConfig
from .xlnet_utils import get_initializer,shape_list

#尽量保证,源码中有的都不删除,放在那就行,注意有一些是必须占位置的就赋值为None
'''
def gelu(x):
    return 0.5 * x * (1.0 + tf.math.erf(x / np.sqrt(2.0)))
'''
def gelu(x):
    """ Implementation of the gelu activation function.
        XLNet is using OpenAI GPT's gelu
        Also see https://arxiv.org/abs/1606.08415
    """
    cdf = 0.5 * (1.0 + tf.tanh((np.sqrt(2 / np.pi) * (x + 0.044715 * tf.pow(x, 3)))))
    return x * cdf

def swish(x):
    return x * tf.sigmoid(x)


ACT2FN = {
    "gelu": tf.keras.layers.Activation(gelu),
    "relu": tf.keras.activations.relu,
    "swish": tf.keras.layers.Activation(swish),
}

'''
#后续依次加上
custom_objects = {
    'gelu':gelu
    }
#也可以直接用赋值的方式
tf.keras.utils.get_custom_objects().update(custom_objects)

#最好都是把pad设置为0,可以 省去很多麻烦
#build_xlnet中mask_index!=0的情况暂时不考虑？
#这个不记得在哪里用了
'''
#{XLNetConfig,}注释掉的是原版

'''
#测试自定义的XLNetConfig
#config_class = XLNetConfig()
#print(config_class.vocab_size)
'''



class TFXNetRelativeAttention(tf.keras.layers.Layer):
    def __init__(self,config,**kwargs):
        super().__init__(**kwargs)
        if config.d_model % config.n_head != 0:
            raise ValueError(
                "The hidden size (%d) is not a multiple of the number of attention "
                "heads (%d)" % (config.d_model, config.n_head)
            )

        self.n_head = config.n_head
        self.d_head = config.d_head
        self.d_model = config.d_model
        self.scale = 1 / (config.d_head ** 0.5)#Attention之后softmax之前进行的scale
        self.initializer_range = config.initializer_range#各种训练参数的初始化方式

        self.layer_norm = tf.keras.layers.LayerNormalization(epsilon = config.layer_norm_eps, name = "layer_norm")
        self.dropout = tf.keras.layers.Dropout(config.dropout)
    
    def build(self, input_shape):
        initializer = get_initializer(self.initializer_range)#transformer:(d_model,d_model),xlnet:(d_model, n_head, d_head),应该是为了做head_mask
        self.q = self.add_weight(
            shape=(self.d_model, self.n_head, self.d_head), initializer=initializer, trainable=True, name="q"
        )
        self.k = self.add_weight(
            shape=(self.d_model, self.n_head, self.d_head), initializer=initializer, trainable=True, name="k"
        )
        self.v = self.add_weight(
            shape=(self.d_model, self.n_head, self.d_head), initializer=initializer, trainable=True, name="v"
        )
        self.o = self.add_weight(
            shape=(self.d_model, self.n_head, self.d_head), initializer=initializer, trainable=True, name="o"
        )
        self.r = self.add_weight(#用于相对位置向量
            shape=(self.d_model, self.n_head, self.d_head), initializer=initializer, trainable=True, name="r"
        )
        self.r_r_bias = self.add_weight(#相对位置向量偏置项
            shape=(self.n_head, self.d_head), initializer="zeros", trainable=True, name="r_r_bias"
        )
        self.r_s_bias = self.add_weight(#seg相对位置向量偏置项
            shape=(self.n_head, self.d_head), initializer="zeros", trainable=True, name="r_s_bias"
        )
        self.r_w_bias = self.add_weight(#词向量偏置项
            shape=(self.n_head, self.d_head), initializer="zeros", trainable=True, name="r_w_bias"
        )
        self.seg_embed = self.add_weight(#seg相对位置词向量
            shape=(2, self.n_head, self.d_head), initializer=initializer, trainable=True, name="seg_embed"
        )##和token_type_ids相关,只有2个embedding，在同一个seg中用第1个，不在同一个seg中(前后句)用第2个，注意这和Bert中的(绝对)位置向量也是不同的
        super().build(input_shape)

    def rel_shift(self, x, klen=-1):##用于调整bd(相对位置向量)的维度
        """perform relative shift to form the relative attention score."""
        x_size = shape_list(x)
        #只有这样转换才会和想要的结果一致,test_xlnet_function有测试函数
        x = tf.reshape(x, (x_size[1], x_size[0], x_size[2], x_size[3]))
        x = x[1:, ...]
        x = tf.reshape(x, (x_size[0], x_size[1] - 1, x_size[2], x_size[3]))
        x = x[:, 0:klen, :, :]
        
        return x

    def rel_attn_core(self, inputs, training=False):
        """Core relative positional attention operations."""
        #q_head:[qlen or num_predict,bsz,n_head,d_head],#qlen是context stream,num_predict是query stream
        #k_head_r:[klen(+1) or klen+qlen,bsz,n_head,d_head],
        #k(v)_head_h:[klen,bsz,n_head,d_head],
        #seg_mat:[qlen,klen,bsz,2]
        #attn_mask:[qlen,klen,bsz,1(d_model)]
        #head_mask = None
        #output_attentions= False
        q_head, k_head_h, v_head_h, k_head_r, seg_mat, attn_mask, head_mask, output_attentions = inputs

        # content based attention score
        ac = tf.einsum("ibnd,jbnd->ijbn", q_head + self.r_w_bias, k_head_h)##[qlen,klen,bsz,n_head]#如果不使用memory,klen=qlen

        # position based attention score
        bd = tf.einsum("ibnd,jbnd->ijbn", q_head + self.r_r_bias, k_head_r)##[qlen,klen+1 or klen+qlen,bsz,n_head]
        bd = self.rel_shift(bd, klen=shape_list(ac)[1])##bd的第二个维度上先去掉距离为klen的然后选klen-1->0,总的来说就是从klen,(klen-1),...,1,0,-1,...,-(qlen-1)中选(klen-1),...,1,0,变成了[qlen,klen,bsz,n_head]

        # segment based attention score
        if seg_mat is None:
            ef = 0
        else:##self.seg_embed就在build中定义了,s代表了2
            ef = tf.einsum("ibnd,snd->ibns", q_head + self.r_s_bias, self.seg_embed)#erazhan:这两步实际上是先用seg_mat与seg_embed作用生成位置词嵌入,然后再用q_head与位置词嵌入作用生成ef,这里的实现其实就是顺序不一样
            ef = tf.einsum("ijbs,ibns->ijbn", seg_mat, ef)##[qlen,klen,bsz,n_head]

        # merge attention scores and perform masking
        attn_score = (ac + bd + ef) * self.scale
        if attn_mask is not None:#erazhan:attn_mask维度就是[qlen,klen,bsz,1(d_model)]
            # attn_score = attn_score * (1 - attn_mask) - 1e30 * attn_mask
            attn_score = attn_score - 1e30 * attn_mask#dtype = tf.float32

        # attention probability
        attn_prob = tf.nn.softmax(attn_score, axis=1)

        attn_prob = self.dropout(attn_prob, training=training)

        # Mask heads if we want to##erazhan应该是用不上的,暂时不管
        if head_mask is not None:
            attn_prob = attn_prob * head_mask

        # attention output#erazhan:[qlen,klen,bsz,n_head]*[klen,bsz,n_head,d_head]->[qlen,bsz,n_head,d_head]
        attn_vec = tf.einsum("ijbn,jbnd->ibnd", attn_prob, v_head_h)
        
        if output_attentions is True:
            return attn_vec, attn_prob

        return attn_vec
    
    def post_attention(self, inputs, residual = True, training = False):##attention结束后,再经过一个o_dense层
        """Post-attention processing."""
        # post-attention projection (back to `d_model`)
        h, attn_vec = inputs

        attn_out = tf.einsum("ibnd,hnd->ibh", attn_vec, self.o)

        attn_out = self.dropout(attn_out, training=training)

        if residual:##实现残差连接,必须使用,h就是经过attention层之前的数据
            attn_out = attn_out + h
        output = self.layer_norm(attn_out)##加一层LN

        return output

    def call(self, inputs, training=False):
        (h, g, attn_mask_h, attn_mask_g, r, seg_mat, mems, target_mapping, head_mask, output_attentions) = inputs
        #h是词向量[qlen,bsz,d_model],g:[qlen,bsz,d_model],target_mapping:[num_predict,qlen?,bsz]
        #attn_mask_h就是non_tgt_mask,attn_mask_g就是attn_mask
        if g is not None:#h,g分别对应context stream,query stream,h是一定会有的,r就是pos_embed位置向量[klen(+1?单向) klen+qlen(双向),bsz,d_model]
            # Two-stream attention with relative positional encoding.
            # content based attention score
            if mems is not None and len(shape_list(mems)) > 1:##使用mems,如果两句话是上下句关系,那么会使用mems,否则不使用(训练语料会按0.5的概率选择上下句)
                cat = tf.concat([mems, h], axis=0)##mems:[mlen,bsz,d_model]
            else:
                cat = h##后续用cat

            # content-based key head
            k_head_h = tf.einsum("ibh,hnd->ibnd", cat, self.k)##[qlen or klen,batch_size,n_head,d_head]

            # content-based value head
            v_head_h = tf.einsum("ibh,hnd->ibnd", cat, self.v)##[qlen or klen,batch_size,n_head,d_head]

            # position-based key head
            k_head_r = tf.einsum("ibh,hnd->ibnd", r, self.r)##[klen(+1) or klen+qlen,batch_size,n_head,d_head]

            # h-stream
            # content-stream query head
            q_head_h = tf.einsum("ibh,hnd->ibnd", h, self.q)#[qlen,batch_size,n_head,d_head]#不考虑mems

            # core attention ops
            attn_vec_h = self.rel_attn_core(
                [q_head_h, k_head_h, v_head_h, k_head_r, seg_mat, attn_mask_h, head_mask, output_attentions],
                training=training,
            )

            if output_attentions is True:
                attn_vec_h, attn_prob_h = attn_vec_h

            # post processing
            output_h = self.post_attention([h, attn_vec_h], training=training)

            # g-stream
            # query-stream query head
            q_head_g = tf.einsum("ibh,hnd->ibnd", g, self.q)#[num_predict,bsz,n_head,d_head]它和q_head_h共用self.q,所有两个stream相互是有影响的

            # core attention ops
            if target_mapping is not None:#erazhan:只有query steam才有,这部分理解了,target_mapping在下面用了两次,1次将[num_predict,bsz,n_head,d_head]->[qlen,bsz,n_head,d_head],另1次效果相反
                q_head_g = tf.einsum("mbnd,mlb->lbnd", q_head_g, target_mapping)#每个能决定num_predict个token的正文token用num_predict个token的embedding表示求和，有点像Embedding层
                attn_vec_g = self.rel_attn_core(##只需计算num_predict个token的embedding表示就行了
                    [q_head_g, k_head_h, v_head_h, k_head_r, seg_mat, attn_mask_g, head_mask, output_attentions],
                    training=training,
                )

                if output_attentions is True:
                    attn_vec_g, attn_prob_g = attn_vec_g

                attn_vec_g = tf.einsum("lbnd,mlb->mbnd", attn_vec_g, target_mapping)##得到qlen个token的embedding后，再映射到num_predict维度(就是将seq_length个embedding求和)
            else:#没有target_mapping
                attn_vec_g = self.rel_attn_core(
                    [q_head_g, k_head_h, v_head_h, k_head_r, seg_mat, attn_mask_g, head_mask, output_attentions],
                    training=training,
                )

                if output_attentions is True:
                    attn_vec_g, attn_prob_g = attn_vec_g

            # post processing
            output_g = self.post_attention([g, attn_vec_g], training=training)

            if output_attentions is True:
                attn_prob = attn_prob_h, attn_prob_g

        else:#g is None也就是只有content stream,finetune阶段
            # Multi-head attention with relative positional encoding
            if mems is not None and len(shape_list(mems)) > 1:
                cat = tf.concat([mems, h], axis=0)
            else:
                cat = h

            # content heads
            q_head_h = tf.einsum("ibh,hnd->ibnd", h, self.q)
            k_head_h = tf.einsum("ibh,hnd->ibnd", cat, self.k)
            v_head_h = tf.einsum("ibh,hnd->ibnd", cat, self.v)

            # positional heads
            k_head_r = tf.einsum("ibh,hnd->ibnd", r, self.r)

            # core attention ops
            attn_vec = self.rel_attn_core(
                [q_head_h, k_head_h, v_head_h, k_head_r, seg_mat, attn_mask_h, head_mask, output_attentions],
                training=training,
            )

            if output_attentions is True:
                attn_vec, attn_prob = attn_vec

            # post processing
            output_h = self.post_attention([h, attn_vec], training=training)
            output_g = None

        outputs = (output_h, output_g)
        if output_attentions is True:
            outputs = outputs + (attn_prob,)
        return outputs
    

class TFXLNetFeedForward(tf.keras.layers.Layer):
    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.layer_norm = tf.keras.layers.LayerNormalization(epsilon=config.layer_norm_eps, name="layer_norm")
        self.layer_1 = tf.keras.layers.Dense(
            config.d_inner, kernel_initializer=get_initializer(config.initializer_range), name="layer_1"
        )
        self.layer_2 = tf.keras.layers.Dense(
            config.d_model, kernel_initializer=get_initializer(config.initializer_range), name="layer_2"
        )
        self.dropout = tf.keras.layers.Dropout(config.dropout)
        if isinstance(config.ff_activation, str):
            self.activation_function = ACT2FN[config.ff_activation]
        else:
            self.activation_function = config.ff_activation

    def call(self, inp, training=False):
        output = inp
        output = self.layer_1(output)
        output = self.activation_function(output)
        output = self.dropout(output, training=training)
        output = self.layer_2(output)
        output = self.dropout(output, training=training)
        output = self.layer_norm(output + inp)
        return output

class TFXLNetLayer(tf.keras.layers.Layer):
    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.rel_attn = TFXLNetRelativeAttention(config, name="rel_attn")
        self.ff = TFXLNetFeedForward(config, name="ff")
        self.dropout = tf.keras.layers.Dropout(config.dropout)

    def call(self, inputs, training=False):
        outputs = self.rel_attn(inputs, training=training)
        output_h, output_g = outputs[:2]

        if output_g is not None:
            output_g = self.ff(output_g, training=training)
        output_h = self.ff(output_h, training=training)
        
        outputs = (output_h, output_g)# + outputs[2:]  # Add again attentions if there are there # outputs[2:]暂时先不管
        return outputs

class TFXLNetLMHead(tf.keras.layers.Layer):
    #这个是预训练阶段预测时,用了共享的Embedding后,还需要加上一个偏置项
    def __init__(self,config,input_embeddings,**kwargs):
        super().__init__(**kwargs)
        self.vocab_size = config.vocab_size
        self.input_embeddings = input_embeddings

    def build(self,input_shape):
        self.bias = self.add_weight(shape = (self.vocab_size,),initializer = "zeros", trainable = True,name = "bias")
        super().build(input_shape)

    def call(self, hidden_states):
        #hidden_states:[bsz,qlen,d_model]->[bsz,qlen,vocab_size]->[bsz,qlen,vocab_size](add bias)
        hidden_states = self.input_embeddings(hidden_states,model="linear")
        hidden_states = hidden_states + self.bias
        return hidden_states

class TFXLNetMainLayer(tf.keras.layers.Layer):
    '''config参数在其它地方赋值'''
    #config_class = XLNetConfig
    def __init__(self,config,**kwargs):
        super().__init__(**kwargs)
        self.output_hidden_states = config.output_hidden_states
        self.oupput_attentions = config.output_attentions
        self.return_dict = config.return_dict#这是个啥

        self.mem_len = config.mem_len
        self.reuse_len = config.reuse_len
        self.d_model = config.d_model
        self.same_length = config.same_length#保留吧,在create_uni_mask中使用到
        self.attn_type = config.attn_type
        self.bi_data = config.bi_data#不考虑
        self.clamp_len = config.clamp_len
        self.n_layer = config.n_layer
        #self.use_bfloat16 = config.use_bfloat16#统统用tf.float32
        self.initializer_range = config.initializer_range

        self.word_embedding = TFSharedEmbeddings(
            config.vocab_size, config.d_model, initializer_range=config.initializer_range, name="word_embedding"
        )
        self.layer = [TFXLNetLayer(config, name="layer_._{}".format(i)) for i in range(config.n_layer)]
        self.dropout = tf.keras.layers.Dropout(config.dropout)
    def get_input_embeddings(self):
        return self.word_embedding

    def set_input_embeddings(self,value):
        self.word_embedding.weight = value
        self.word_embedding.vocab_size = value.shape[0]
    
    def build(self,input_shape):

        initializer = get_initializer(self.initializer_range)
        #在modeling_tf_utils中定义

        #这个用于构造初始query stream中的g,对应[num_predict,bsz,d_model],表示要预测token的词向量表示
        self.mask_emb = self.add_weight(shape = (1,1,self.d_model),initializer = initializer, trainable = True, name = "mask_emb")

    def create_uni_mask(self,qlen, mlen, dtype = tf.float32):
        '''单向模型时产生初始的attn_mask,此时不需要双向模型的perm_mask'''
        
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
        if self.same_length:
            mask_l = tf.linalg.band_part(attn_mask, -1, 0)
            ret = tf.concat([ret[:, :qlen] + mask_l - mask_dia, ret[:, qlen:]], 1)
        return ret

    def cache_mem(self, curr_out, prev_mem):
        #关于mem的用法还不是很懂
        """cache hidden states into memory."""
        if self.reuse_len is not None and self.reuse_len > 0:
            curr_out = curr_out[: self.reuse_len]

        if prev_mem is None:
            new_mem = curr_out[-self.mem_len :]
        else:
            new_mem = tf.concat([prev_mem, curr_out], 0)[-self.mem_len :]

        return tf.stop_gradient(new_mem)

    @staticmethod
    def positional_embedding(pos_seq, inv_freq, bsz=None):
        sinusoid_inp = tf.einsum("i,d->id", pos_seq, inv_freq)
        pos_emb = tf.concat([tf.sin(sinusoid_inp), tf.cos(sinusoid_inp)], axis=-1)
        pos_emb = pos_emb[:, None, :]

        if bsz is not None:
            pos_emb = tf.tile(pos_emb, [1, bsz, 1])

        return pos_emb

    def relative_positional_encoding(self, qlen, klen, bsz=None, dtype = tf.float32):
        """create relative positional encoding."""
        freq_seq = tf.range(0, self.d_model, 2.0)
        freq_seq = tf.cast(freq_seq, dtype=dtype)

        inv_freq = 1 / (10000 ** (freq_seq / self.d_model))
        assert self.att_type == "bi" or self.att_type == "uni", "att_type must be 'bi' or 'uni'"
        if self.attn_type == "bi":
            # beg, end = klen - 1, -qlen
            beg, end = klen, -qlen
        else:#self.attn_type == "uni"
            # beg, end = klen - 1, -1
            beg, end = klen, -1

        fwd_pos_seq = tf.range(beg, end, -1.0)
        fwd_pos_seq = tf.cast(fwd_pos_seq, dtype = dtype)
        if self.clamp_len > 0:
            fwd_pos_seq = tf.clip_by_value(fwd_pos_seq, -self.clamp_len, self.clamp_len)
        pos_emb = self.positional_embedding(fwd_pos_seq, inv_freq, bsz)#bsz仅仅用处只有一个

        return pos_emb

    def call(self,
             inputs,
             attention_mask = None,
             mems = None,
             perm_mask = None,
             target_mapping = None,
             token_type_ids = None,
             input_mask = None,
             head_mask = None,#这个暂不考虑,
             inputs_embeds = None,
             use_cache = True,
             output_attentions = None,
             output_hidden_states = None,
             #return_dict = None,#这个是新版本的,暂不考虑
             training = False
             ):
        #判断inputs格式,至少有input_ids,这里暂不考虑dict,BatchEncoding格式(源码中的第2种)
        if isinstance(inputs, (tuple,list)):
            #输入严格按照顺序来
            input_ids = inputs[0]#[bsz,qlen]
            attention_mask = inputs[1] if len(inputs) > 1 else attention_mask#[bsz,qlen,qlen],0代表mask
            mems = inputs[2] if len(inputs) > 2 else mems#列表,个数是attention的层数,后续补充使用说明
            perm_mask = inputs[3] if len(inputs) > 3 else perm_mask#[bsz,qlen,qlen(klen?)]
            target_mapping = inputs[4] if len(inputs) > 4 else target_mapping#维度[bsz,num_predict,qlen(klen)]
            token_type_ids = inputs[5] if len(inputs) > 5 else token_type_ids#[bsz,qlen]
            input_mask = inputs[6] if len(inputs) > 6 else input_mask#[bsz,qlen],和attention_mask相反,1代表mask
            head_mask = inputs[7] if len(inputs) > 7 else head_mask#对不同的head进行mask,暂不考虑,直接填个None就行
            inputs_embeds = inputs[8] if len(inputs) > 8 else inputs_embeds#[bsz,qlen,d_model(hidden_size)]就是word_embedding(input_ids)
            use_cache = inputs[9] if len(inputs) > 9 else use_cache#是否使用memory机制,默认True
            output_attentions = inputs[10] if len(inputs) > 10 else output_attentions#是否输出每个attention层后的qk(还没到qkv),暂不考虑
            output_hidden_states = inputs[11] if len(inputs) > 11 else output_hidden_states##输出每一层的结果(后续再完善理解),暂不考虑
            assert len(inputs) <= 12, "Too many inputs."
        else:
            input_ids = inputs

        #放这里,先不考虑
        #output_attentions = output_attentions if output_attentions is not None else self.output_attentions
        #output_hidden_states = output_hidden_states if output_hidden_states is not None else self.output_hidden_states
        
        if input_ids is not None and inputs_embeds is not None:
            raise ValueError("You cannot specify both input_ids and inputs_embeds at the same time")
        elif input_ids is not None:#[bsz,qlen]->[qlen,bsz]
            input_ids = tf.transpose(input_ids, perm=(1, 0))
            qlen, bsz = shape_list(input_ids)[:2]
        elif inputs_embeds is not None:#[bsz,qlen,d_model]->[qlen,bsz,d_model]
            inputs_embeds = tf.transpose(inputs_embeds, perm=(1, 0, 2))
            qlen, bsz = shape_list(inputs_embeds)[:2]
        else:
            raise ValueError("You have to specify either input_ids or inputs_embeds")

        token_type_ids = tf.transpose(token_type_ids, perm=(1, 0)) if token_type_ids is not None else None#[bsz,qlen]->[qlen,bsz]
        input_mask = tf.transpose(input_mask, perm=(1, 0)) if input_mask is not None else None#[bsz,qlen]->[qlen,bsz]
        attention_mask = tf.transpose(attention_mask, perm=(1, 0)) if attention_mask is not None else None#[bsz,qlen]->[qlen,bsz]
        perm_mask = tf.transpose(perm_mask, perm=(1, 2, 0)) if perm_mask is not None else None#[bsz,qlen,qlen]->[qlen,qlen,bsz]#第2个确定是qlen,后续计算好data_mask后加上mlen
        target_mapping = tf.transpose(target_mapping, perm=(1, 2, 0)) if target_mapping is not None else None#[bsz,num_predict,qlen]->[num_predict,qlen,bsz]

        mlen = shape_list(mems[0])[0] if mems is not None and mems[0] is not None else 0#mlen和memory有关
        klen = mlen + qlen

        # Attention mask
        # causal attention mask
        if self.attn_type == "uni":#选择单向模型,此处得到的atten_mask其实和Transformer的decoder的mask一样，注意该符号和attention_mask的区别
            attn_mask = self.create_uni_mask(qlen, mlen)
            attn_mask = attn_mask[:, :, None, None]#[qlen,klen]->[qlen,klen,1(bsz),1(d_model or d_head?)]
        elif self.attn_type == "bi":#选择双向模型,此时不用attn_mask,而是用perm_mask,二者只需一个
            attn_mask = None
        else:
            raise ValueError("Unsupported attention type: {}".format(self.attn_type))

        # data mask: input mask & perm mask
        assert input_mask is None or attention_mask is None, (#input_mask和attention_mask二选一
            "You can only use one of input_mask (uses 1 for padding) "
            "or attention_mask (uses 0 for padding, added for compatbility with BERT). Please choose one."
        )
        if input_mask is None and attention_mask is not None:
            input_mask = 1.0 - tf.cast(attention_mask, dtype = tf.float32)#input_mask中1是被mask,后续只用input_mask
        if input_mask is not None and perm_mask is not None:#使用input_mask和perm_mask,Tensor加个None效果是增加1个第0维,原来的维度向后移一维
            data_mask = input_mask[None] + perm_mask#维度为[qlen,qlen,bsz],data_mask可能出现2,最后转为1.0
        elif input_mask is not None and perm_mask is None:#没有perm_mask
            data_mask = input_mask[None]
        elif input_mask is None and perm_mask is not None:#没有input_mask
            data_mask = perm_mask
        else:
            data_mask = None#两个mask都没有
     
        if data_mask is not None:
            # all mems can be attended to
            if mlen > 0:#加上memory,对应的mask全为0,也就是不mask
                mems_mask = tf.zeros([shape_list(data_mask)[0], mlen, bsz], dtype = tf.float32)#[qlen,mlen,bsz]
                data_mask = tf.concat([mems_mask, data_mask], axis=1)#[qlen,klen,bsz]
            if attn_mask is None:#双向
                attn_mask = data_mask[:, :, :, None]
            else:#单向,此时data_mask中的perm_mask应该不用给定
                attn_mask += data_mask[:, :, :, None]#data_mask和attn_mask相加,保留attn_mask

        if attn_mask is not None:
            attn_mask = tf.cast(attn_mask > 0, dtype = tf.float32)

        if attn_mask is not None:##将attn_mask->non_tgt_mask,就是将对角线上元素设置为0,被perm_mask掉的token在计算权重时是需要考虑自身token对自己产生的影响的,比如将最后两个词作为预测token
            non_tgt_mask = -tf.eye(qlen, dtype = tf.float32)##对角线上的全部设置为0，消除当前token从1变成0，说实话还不是很懂为什么要这么做,感觉是多余的?
            if mlen > 0:
                non_tgt_mask = tf.concat([tf.zeros([qlen, mlen], dtype = tf.float32), non_tgt_mask], axis=-1)
            non_tgt_mask = tf.cast((attn_mask + non_tgt_mask[:, :, None, None]) > 0, dtype = tf.float32)
        else:
            non_tgt_mask = None
        #后续使用attn_mask和non_tgt_mask,在双向模式时,attn_mask用于query stream,non_tgt_mask用于contest stream
        
        # Word embeddings and prepare h & g hidden states
        if inputs_embeds is not None:
            word_emb_k = inputs_embeds#[qlen,bsz,d_model]
        else:
            word_emb_k = self.word_embedding(input_ids)
        output_h = self.dropout(word_emb_k, training = training)#[qlen,bsz,d_model]#这个就是k_head_h
        if target_mapping is not None:#erazhan:[1,1,d_model] -> [num_predict,bsz,d_model],在预训练阶段我们只需要得到num_predict个token的最终词向量表示进行计算损失函数
            word_emb_q = tf.tile(self.mask_emb, [shape_list(target_mapping)[0], bsz, 1])
            #初始化用每个bsz每个token的表示用同一个向量表示    
            output_g = self.dropout(word_emb_q, training = training)
        else:
            output_g = None

        # Segment embedding
        if token_type_ids is not None:#token_type_ids:[qlen,bsz]
            # Convert `token_type_ids` to one-hot `seg_mat`
            if mlen > 0:
                mem_pad = tf.zeros([mlen, bsz], dtype=tf.int32)
                cat_ids = tf.concat([mem_pad, token_type_ids], 0)
            else:
                cat_ids = token_type_ids

            # `1` indicates not in the same segment [qlen x klen x bsz]##erazhan:[qlen,1,bsz] [1,qlen or klen,bsz]->[qlen,qlen or klen,bsz]
            seg_mat = tf.cast(tf.logical_not(tf.equal(token_type_ids[:, None], cat_ids[None, :])), tf.int32)#参考test_xlnet_functions中的test_seg_mat
            seg_mat = tf.one_hot(seg_mat, 2, dtype=dtype_float)##最后还会与2维的segment矩阵相乘，后续再看怎么用[qlen,klen,bsz,2]
        else:##seg_mat也是考虑相对位置的(也就是对于1个token对另一个token),在同一个seg中用相同的seg_embed,不同的seg则用另外一个(在bert中我理解的seg embed是在前后seg分别对应用一个词嵌入,没有考虑相对位置)
            seg_mat = None

        # Positional encoding
        pos_emb = self.relative_positional_encoding(qlen, klen, bsz = bsz, dtype = tf.float32)
        pos_emb = self.dropout(pos_emb, training = training)

        #head_mask暂时不管

        new_mems = ()#每层一个,mems[i]:[bsz,mlen,d_model](具体再看后续)
        if mems is None:
            mems = [None] * len(self.layer)

        attentions = []#[qlen,klen,bsz,d_model]?
        hidden_states = []#[qlen,bsz,d_model]?

        for i, layer_module in enumerate(self.layer):
            # cache new mems
            if self.mem_len is not None and self.mem_len > 0 and use_cache is True:
                new_mems = new_mems + (self.cache_mem(output_h, mems[i]),)
            #这个暂时先不管
            #if cast_bool_to_primitive(output_hidden_states) is True:
            #    hidden_states.append((output_h, output_g) if output_g is not None else output_h)

            outputs = layer_module(#self.layer TFXLNetRelativeAttention
                [
                    output_h,
                    output_g,
                    non_tgt_mask,
                    attn_mask,
                    pos_emb,
                    seg_mat,
                    mems[i],
                    target_mapping,
                    head_mask[i],
                    output_attentions,
                ],
                training=training,
            )
            output_h, output_g = outputs[:2]
            #暂不考虑
            #if cast_bool_to_primitive(output_attentions) is True:
            #    attentions.append(outputs[2])

        # Add last hidden state
        #if cast_bool_to_primitive(output_hidden_states) is True:
        #    hidden_states.append((output_h, output_g) if output_g is not None else output_h)

        #预训练阶段或者语言模型生成token用query stream的结果预测最后两个token,其它情况直接用最后的[bsz,qlen,d_model]作为token的词向量表示参与下游任务(和Bert类似,但是具体细节还要研究下)
        output = self.dropout(output_g if output_g is not None else output_h, training=training)

        # Prepare outputs, we transpose back here to shape [bsz, len, hidden_dim] (cf. beginning of forward() method)
        outputs = (tf.transpose(output, perm=(1, 0, 2)),)

        if self.mem_len is not None and self.mem_len > 0 and use_cache is True:
            outputs = outputs + (new_mems,)
        """
        if cast_bool_to_primitive(output_hidden_states) is True:
            if output_g is not None:
                hidden_states = tuple(tf.transpose(h, perm=(1, 0, 2)) for hs in hidden_states for h in hs)
            else:
                hidden_states = tuple(tf.transpose(hs, perm=(1, 0, 2)) for hs in hidden_states)
            outputs = outputs + (hidden_states,)
        if cast_bool_to_primitive(output_attentions) is True:
            attentions = tuple(tf.transpose(t, perm=(2, 3, 0, 1)) for t in attentions)
            outputs = outputs + (attentions,)
        """
        
        return outputs  # outputs, (new_mems), (hidden_states), (attentions)   

#PreTrainedModel
class TFXLNetModel(tf.keras.Model):
    def __init__(self,config,*inputs,**kwargs):
        super().__init__(*inputs,**kwargs)
        self.transformer = TFXLNetMainLayer(config, name = "transformer")

    def call(self,inputs,**kwargs):
        outputs = self.transformer(inputs,**kwargs)
        return outputs
        
class TFXNetLMHeadModel(tf.keras.Model):
    def __init__(self,config,*inputs,**kwargs):
        self.transformer = TFXLNetMainLayer(*config, name = "transformer")
        self.lm_loss = TFXLNetLMHead(config,self.transformer.word_embedding,name = "lm_loss")
    def get_output_embeddings(self):
        return self.lm_loss.input_embeddings

    def call(
        self,
        inputs,
        attention_mask = None,
        mems = None,
        perm_mask = None,
        target_mapping = None,
        token_type_ids = None,
        input_mask = None,
        head_mask = None,
        inputs_embeds = None,
        use_cache = True,
        output_attentions = None,
        output_hidden_states = None,
        labels = None,
        training = False,
        ):
        if isinstance(inputs, (tuple, list)):
            labels = inputs[12] if len(inputs) > 12 else labels
            if len(inputs) > 12:
                inputs = inputs[:12]
        elif isinstance(inputs, (dict, BatchEncoding)):
            labels = inputs.pop("labels", labels)

        transformer_outputs = self.transformer(
            inputs,
            attention_mask=None,
            mems=None,
            perm_mask=None,
            target_mapping=None,
            token_type_ids=None,
            input_mask=None,
            head_mask=None,
            inputs_embeds=None,
            use_cache=True,
            output_attentions=None,
            output_hidden_states=None,
            training=training,
        )
        hidden_state = transformer_outputs[0]
        logits = self.lm_loss(hidden_state, training=training)

        outputs = (logits,) + transformer_outputs[1:]  # Keep mems, hidden states, attentions if there are in it

        if labels is not None:
            # shift labels to the left and cut last logit token
            logits = logits[:, :-1]
            labels = labels[:, 1:]
            loss = self.compute_loss(labels, logits)
            outputs = (loss,) + outputs

        return outputs  # return logits, (mems), (hidden states), (attentions)

if __name__ == "__main__":
    import toolsbyerazhan as tbe
    tbe.set_gpu_memory_tf()





        
