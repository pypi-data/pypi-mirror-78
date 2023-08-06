import tensorflow as tf
import numpy as np

from tensorflow.keras.layers import Layer
#注:该部分代码从笔记的tensorflow文件夹中复制

'''
数据名称说明：
inputs:[batch_size,max_seq_length],tf.int32
targets:[batch_size,max_seq_length],tf.int32
input_length:[batch_size,],tf.int32
logits:[batch_size,max_seq_length,num_tags],tf.float32
transition_params:[num_tags,num_tags],tf.float32
'''

class CRFLayer(Layer):
    
    def __init__(self,num_tags,**kwargs):
        
        super(CRFLayer,self).__init__(**kwargs)
        self.num_tags = num_tags

    def build(self, input_shape):
        super(CRFLayer,self).build(input_shape)
        shape = (self.num_tags,self.num_tags)
        self.transition_params = self.add_weight(name = "transition_params",
                                                 shape = shape,
                                                 initializer = 'glorot_uniform',
                                                 trainable = True)
        
    def call(self, logits, transition_params = None):
        "input_length是要给定的,input代表最开始的输入,在bilstm的Embedding层接收的inputs" 
        
        self.batch_size, self.max_seq_length= tf.TensorShape(tf.shape(logits))[:2]
        assert self.num_tags == tf.TensorShape(tf.shape(logits))[-1], "inputs的维度与self.num_tags不匹配"
        
        #手动给定transition_params,用于测试CRFLayer效果
        if transition_params is not None:
            self.transition_params = transition_params
        
        return logits
    
    def crf_log_likelihood(self, logits, targets, input_lengths):

        unary_score = self.crf_unary_score(logits, targets, input_lengths)
        binary_score = self.crf_binary_score(targets, input_lengths)

        score = unary_score + binary_score
        log_norm = self.crf_log_norm(logits, input_lengths)
        loss = score - log_norm

        return loss

    def crf_log_norm(self, logits, input_lengths):

        transition_params = tf.expand_dims(self.transition_params, 0)
        
        _state = logits[:,0,:]

        last_index = tf.cast(tf.maximum(0, input_lengths - 1),dtype = tf.int32)
        all_alphas = tf.expand_dims(_state, 1)

        for i in range(1, self.max_seq_length):
            _input = logits[:,i,:]
            
            _state = tf.expand_dims(_state, 2)
            transition_scores = _state + transition_params

            _state = _input + tf.reduce_logsumexp(transition_scores, [1])

            all_alphas = tf.concat([all_alphas, tf.expand_dims(_state, 1)],axis = 1)

        idxs = tf.stack([tf.range(self.batch_size),last_index], axis = 1)

        #all_alphas维度为[batch_size,num_tags],每个batch的num_tags个元素代表的是最后一个时间步的分值
        all_alphas = tf.gather_nd(all_alphas, idxs)

        #log_norm的维度为[batch_size,]
        log_norm = tf.reduce_logsumexp(all_alphas, [1])

        #确保出现长度为0的输入对应的loss为0
        log_norm = tf.where(tf.less_equal(input_lengths, 0), tf.zeros_like(log_norm), log_norm)
        return log_norm
    
    def crf_unary_score(self, logits, targets, input_lengths):
        '''思路是将logits铺开，变成一个一维向量，维度维batch_size*max_seq_length*num_tags，
            然后构造根据targets计算出选择的位置'''
        '''求S1,输出维度维度为(batch_size,)'''
        batch_size,max_seq_length,num_tags = tf.TensorShape(tf.shape(logits))[:3]

        #维度由[batch_size,max_seq_length,num_tags]变成了batch_size*max_seq_length*num_tags
        #效果展示看test_func_1()
        flattened_logits = tf.reshape(logits, [-1])

        #维度最后是(batch_size,1)数字从0开始每次加max_seq_length*num_tags
        #效果展示看test_func_2()
        offsets = tf.expand_dims(tf.range(batch_size) * max_seq_length * num_tags, 1)

        #最后维度是(batch_size,max_seq_length),每个元素从0开始依次加num_tags
        #效果展示看test_func_3()
        offsets += tf.expand_dims(tf.range(max_seq_length) * num_tags,0)

        #这样做的目标完全就是为了带入tf.gather
        flattened_tag_offsets = tf.reshape(offsets + targets, [-1])

        unary_scores = tf.reshape(tf.gather(flattened_logits, flattened_tag_offsets), (batch_size,max_seq_length))

        #一定要转为tf.float32格式，否则最后计算时会报错
        #参考代码笔记中的tf.sequence_mask
        masks = tf.sequence_mask(input_lengths, maxlen = tf.shape(targets)[1], dtype = tf.float32)

        unary_scores = tf.reduce_sum(unary_scores * masks, 1)

        return unary_scores
    
    def crf_binary_score(self, targets, input_lengths):
        '''求S2，当然也可以用tf.einsum，但是个人偏好用这种更底层的方式'''

        #也可以用tf.slice切片
        start_targets = targets[:,:-1]
        end_targets = targets[:,1:]

        #建立相邻两个时间步状态对(yp,y)，计算平坦化后位置顺序，维度为[batch_size, max_seq_length - 1]
        start_to_end = start_targets * self.num_tags + end_targets

        #将转移概率矩阵平坦化
        flattened_transition_params = tf.reshape(self.transition_params, [-1])

        #根据start_to_end在flattened_transition_params中找相应位置的数字，维度和start_to_end相同
        binary_scores = tf.gather(flattened_transition_params, start_to_end)

        #根据长度构造masks，维度为[batch_size,max_seq_length]
        masks = tf.sequence_mask(input_lengths, maxlen = tf.shape(targets)[1],dtype = tf.float32)

        #将masks的维度匹配成和binary_scores一样，均为[batch_size,max_seq_length-1]
        #不用masks[:,:-1]的原因是start为True，但end可能为False,
        #start为True,end不一定为True，也可能 是False
        #end为True,start一定为True
        #end为False,那么就没必要计算这对评分值了
        
        masks = masks[:,1:]
        binary_scores = tf.reduce_sum(binary_scores * masks, 1)

        return binary_scores

    def viterbi_decode(self, logits):
        '''
        logits：[1,seq_length,num_tags]或者[seq_length,num_tags],如果是前者则将其转为后者,且用numpy进行操作
        return：path_scores，path_states
        '''
        n_dims = len(tf.shape(logits))

        assert n_dims == 2 or (n_dims == 3 and tf.shape(logits)[0] == 1), "n_dims必须为2或3,只处理一条数据"
        
        if n_dims == 3:
            
            logits = tf.squeeze(logits, 0)

        #score的维度为
        logits = np.array(logits, dtype = np.float32)
        
        transition_params = np.array(self.transition_params, dtype = np.float32)
        
        seq_length, num_tags = logits.shape
        
        pathScores = np.zeros_like(logits, dtype = np.float32)
        pathStates = np.zeros_like(logits, dtype = np.int32)
        
        pathScores[0] = logits[0]
    
        for i in range(seq_length - 1):

            scores = pathScores[i]
            temM = scores[:, np.newaxis] + transition_params
            
            pathScores[i + 1] = np.max(temM, axis = 0) + logits[i+1]
            pathStates[i + 1] = np.argmax(temM, axis = 0) 

        path = np.zeros(seq_length, dtype = np.int32)
        path[-1] = np.argmax(pathScores[-1])

        for i in range(seq_length - 1, 0, -1):
            path[i-1] = pathStates[i,path[i]]

        return list(path), np.max(pathScores[-1])
    
    def crf_decode(self):
        #处理一个batch的数据,后续补充,可采用RNNCell
        pass

if __name__=="__main__":
    pass



    
