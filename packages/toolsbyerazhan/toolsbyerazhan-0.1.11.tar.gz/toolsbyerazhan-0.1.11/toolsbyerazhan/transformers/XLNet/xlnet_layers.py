import tensorflow as tf
import numpy as np

from tensorflow.keras.layers import Layer,Embedding
'''
说明：以下参考https://github.com/CyberZHG

keras-embed-sim：EmbeddingRet、EmbeddingSim
CyberZHG/keras-trans-mask：CreateMask
MaskEmbedding参考CyberZHG/keras-xlnet本身当中的mask_embed
keras-bert：Extract（很简单的操作）
keras_transformer_xl：Memory
'''

#其实如果用不到的话,不用构造这么麻烦,构造个基本能实现功能的就行了
class EmbeddingRet(Embedding):
    #除了Embedding正常的功能外,还会返回权重(self.embedding)
    #当前对应的shape也要修改
    def compute_output_shape(self,input_shape):
        return [super(Embedding,self).compute_output_shape(input_shape),
                (self.input_dim,self.output_dim),]

    def compute_mask(self,input,mask = None):
        '''
        Embedding中按照mask_zero是否为True来决定是否计算mask
        如果mask_zero=True就是需要让pad用0表示，计算mask时将
        非pad位标记为1，pad位标记为0
        '''
        return [super(EmbeddingRet,self).compute_mask(inputs,mask),None,]
    
    def call(self,inputs):
        return [super(EmbeddingRet,self).call(inputs),
                self.embeddings + 0.0,]
    #self.embedding是Embedding的属性

class EmbeddingSim(tf.keras.layers.Layer):
    """Calculate similarity between features and token embeddings with bias term."""
    #暂时还不知道在哪里用上
    def __init__(self,
                 use_bias=True,
                 initializer='zeros',
                 regularizer=None,
                 constraint=None,
                 stop_gradient=False,
                 **kwargs):
        """Initialize the layer.
        :param output_dim: Same as embedding output dimension.
        :param use_bias: Whether to use bias term.
        :param initializer: Initializer for bias.
        :param regularizer: Regularizer for bias.
        :param constraint: Constraint for bias.
        :param stop_gradient: Whether to stop gradient for input embedding.
        :param kwargs: Arguments for parent class.
        """
        super(EmbeddingSim, self).__init__(**kwargs)
        self.supports_masking = True
        self.use_bias = use_bias
        self.initializer = keras.initializers.get(initializer)
        self.regularizer = keras.regularizers.get(regularizer)
        self.constraint = keras.constraints.get(constraint)
        self.stop_gradient = stop_gradient
        self.bias = None

    def get_config(self):
        config = {
            'use_bias': self.use_bias,
            'initializer': keras.initializers.serialize(self.initializer),
            'regularizer': keras.regularizers.serialize(self.regularizer),
            'constraint': keras.constraints.serialize(self.constraint),
            'stop_gradient': self.stop_gradient,
        }
        base_config = super(EmbeddingSim, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def build(self, input_shape):
        if self.use_bias:
            embed_shape = input_shape[1]
            token_num = int(embed_shape[0])
            self.bias = self.add_weight(
                shape=(token_num,),
                initializer=self.initializer,
                regularizer=self.regularizer,
                constraint=self.constraint,
                name='bias',
            )
        super(EmbeddingSim, self).build(input_shape)

    def compute_output_shape(self, input_shape):
        feature_shape, embed_shape = input_shape
        token_num = embed_shape[0]
        return feature_shape[:-1] + (token_num,)

    def compute_mask(self, inputs, mask=None):
        if mask is None:
            return None
        return mask[0]

    def call(self, inputs, mask=None, **kwargs):
        inputs, embeddings = inputs
        if self.stop_gradient:
            embeddings = K.stop_gradient(embeddings)
        outputs = K.dot(inputs, K.transpose(embeddings))
        if self.use_bias:
            outputs = K.bias_add(outputs, self.bias)
        return keras.activations.softmax(outputs)

class CreateMask(Layer):
    """Create mask from input tensor.
    The shape of the mask equals to the shape of the input tensor.
    # Input shape
        Tensor with shape: `(batch_size, ...)`.
    # Output shape
        Tensor with shape: `(batch_size, ...)`.
    """

    def __init__(self, mask_value=0., **kwargs):
        super(CreateMask, self).__init__(**kwargs)
        self.supports_masking = True
        self.mask_value = mask_value

    def compute_output_shape(self, input_shape):
        return input_shape

    def compute_mask(self, inputs, mask=None):
        '''
        #这是官方Embedding中的compute_mask函数
        def compute_mask(self, inputs, mask=None):
            if not self.mask_zero:
                return None

            return math_ops.not_equal(inputs, 0)
        '''

        #K改为了tf
        return tf.not_equal(inputs, self.mask_value)

    def call(self, inputs, **kwargs):
        #K改为了tf，这个全0矩阵好像只是为了保持形状？
        return tf.zeros_like(inputs)

    def get_config(self):
        config = {'mask_value': self.mask_value}
        base_config = super(CreateMask, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

class RestoreMask(Layer):
    """Restore mask from the second tensor.
    # Input shape
        Tensor with shape: `(batch_size, ...)`.
        Tensor with mask and shape: `(batch_size, ...)`.
    # Output shape
        Tensor with shape: `(batch_size, ...)`.
    """

    def __init__(self, **kwargs):
        super(RestoreMask, self).__init__(**kwargs)
        self.supports_masking = True

    def compute_output_shape(self, input_shape):
        return input_shape[0]
    
    def compute_mask(self, inputs, mask=None):
        '''
        inputs = [token_embed,masking]
        mask = [mask0,mask1]
        最后的输出mask[1]=mask1的解释就是
        我们的输入inputs列表有两个元素
        一个是token_embed一个通过Createmask层计算的全为0的masking(仅用于传递新mask)
        那么因为self.supports_masking=True(都是支持mask传递的)
        两个输入在上一层计算中对应都有通过compute_mask函数计算得到
        的mask,那么我们将第2个输入masking对应的mask1作为
        第1个输入token_embed的新mask，因为token_embed原来的
        mask1(由EmbeddingRet得到，本质还是用Embedding计算)在mask_index!=0时
        计算为None
        '''
        return mask[1]
    #使用中,inputs=[token_embed,masking]
    #第一个是Embedding层后的词向量[batch_size,T,embed_size]
    #第二个是masking,[batch_size,T]全为0
    def call(self, inputs, **kwargs):
        return inputs[0] + 0.0

#这个是从
class MaskEmbedding(Layer):
    """Embedding for query tokens.

    # Arguments
        units: int >= 0. Number of hidden units.

    # Input shape
        Token embeddings, 3D tensor with shape: `(batch_size, seq_len, units)`.
        Query input, 2D tensor with shape: `(batch_size, seq_len)`.

    # Output shape
        3D tensor with shape: `(batch_size, seq_len, units)`.

    # References
        - [XLNet: Generalized Autoregressive Pretraining for Language Understanding](https://arxiv.org/pdf/1906.08237)
    """

    def __init__(self,
                 units,
                 initializer='uniform',
                 regularizer=None,
                 constraint=None,
                 **kwargs):
        super(MaskEmbedding, self).__init__(**kwargs)
        self.supports_masking = True
        self.units = units
        self.initializer = initializers.get(initializer)
        self.regularizer = regularizers.get(regularizer)
        self.constraint = constraints.get(constraint)

        self.embeddings = None

    def build(self, input_shape):
        #这个就是论文中的g_i^{(0)} = w
        self.embeddings = self.add_weight(
            shape=(1, 1, self.units),
            initializer=self.initializer,
            regularizer=self.regularizer,
            constraint=self.constraint,
            name='embeddings',
        )
        super(MaskEmbedding, self).build(input_shape)

    def compute_output_shape(self, input_shape):
        return input_shape[0]

    def compute_mask(self, inputs, mask=None):
        output_mask = None
        if mask is not None:
            output_mask = mask[0]
        return output_mask

    def call(self, inputs, **kwargs):
        token_embed, query = inputs
        query = tf.expand_dims(tf.cast(query,dtype = tf.float32),axis = -1)
        #query = K.expand_dims(K.cast(query, dtype=K.floatx()), axis=-1)

        #不理解怎么操作的啊，实际上query仅仅在预训练阶段使用，下游任务中是不需要的
        #[batch_size,seq_length,1]*[1,1,units]+[batch_size,seq_length]*[batch_size,seq_length,units]
        #query位置上为1(有几个位置？应该只有一个吧)，用专用的embedding，其它的位置上仍然用原来的token_embed
        #或者说query的位置上就是
        #因为训练时为了方便，是将一句话切分成两段，第二段的token作为预测token
        #query中这些预测位的token就是1，非预测位对应0,形式为[0,0,0,0,1,1](没有计算排列)
        #初始时预测位的token用一个可训练的vector代替本身wordembedding,
        #非预测位的token就还沿用本身的wordembedding
        #当然还要看最后的permutationmask怎么做，最后再总结一下
        #暂停
        return query * self.embeddings + (1.0 - query) * token_embed

    def get_config(self):
        config = {
            'units': self.units,
            'initializer': initializers.serialize(self.initializer),
            'regularizer': regularizers.serialize(self.regularizer),
            'constraint': constraints.serialize(self.constraint),
        }
        base_config = super(MaskEmbedding, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

class Extract(Layer):
    """Extract from index.
    See: https://arxiv.org/pdf/1810.04805.pdf
    """

    def __init__(self, index, **kwargs):
        super(Extract, self).__init__(**kwargs)
        self.index = index
        self.supports_masking = True

    def get_config(self):
        config = {
            'index': self.index,
        }
        base_config = super(Extract, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def compute_output_shape(self, input_shape):
        return input_shape[:1] + input_shape[2:]

    def compute_mask(self, inputs, mask=None):
        return None

    def call(self, x, mask=None):
        return x[:, self.index]


class Memory(Layer):
    """Positional embeddings.
    # Arguments
        batch_size: int > 0. Maximum batch size.
        memory_len: int > 0. Maximum memory length.
        target_len: int > 0. Maximum length of targets.
        output_dim: int > 0. Dimension of outputs.
    # Input shape
        3D tensor with shape: `(batch_size, sequence_length, output_dim)`.
        1D tensor with shape: `(batch_size,)` represents length of memory.
    # Output shape
        3D tensor with shape: `(batch_size, sequence_length + memory_length, output_dim)`.
    # References
        - [Transformer-XL](https://arxiv.org/pdf/1901.02860.pdf)
    """

    def __init__(self, batch_size, memory_len, target_len, output_dim, **kwargs):
        super(Memory, self).__init__(**kwargs)
        self.supports_masking = True
        self.stateful = True#支持在不同的batch中进行传递信息，在推理中也会运行

        self.batch_size = batch_size
        self.memory_len = memory_len
        self.target_len = target_len
        self.output_dim = output_dim

        self.memory = None

    def build(self, input_shape):
        self.memory = self.add_weight(
            shape=(self.batch_size, self.memory_len + self.target_len, self.output_dim),
            initializer='zeros',
            trainable=False,#不可训练，是根据上一个batch最后一层计算得到的?
            name='memory',
        )
        super(Memory, self).build(input_shape)

    def compute_output_shape(self, input_shape):
        return input_shape[0][0], None, self.output_dim

    def compute_mask(self, inputs, mask=None):
        if mask is None:
            return None
        return mask[0]

    def call(self, inputs, **kwargs):
        #注意这里要把K换成tf等，否则保错
        #inputs：[batch_size,seq_length,hidden_size]
        #memory_length：[batch_siz,1]
        inputs, memory_length = inputs
        memory_length = tf.cast(memory_length[0][0], 'int32')
        batch_size = tf.cast(tf.shape(inputs)[0], 'int32')
        seq_len = tf.cast(tf.shape(inputs)[1], 'int32')

        # Build new memory
        pad = tf.tile(inputs[0:1, ...], (self.batch_size - batch_size, 1, 1))
        padded = tf.concatenate([inputs, pad], axis=0)              # (self.batch_size, seq_len, output_dim)
        new_memory = tf.concatenate([self.memory, padded], axis=1)  # (self.batch_size, self.memory_len + seq_len, ...)
        new_memory = tf.slice(                                     # (self.batch_size, self.memory_len, output_dim)
            new_memory,
            (0, seq_len, 0),
            (self.batch_size, self.memory_len + self.target_len, self.output_dim),
        )
        self.add_update(K.update(self.memory, new_memory), inputs)

        # Build output
        old_memory = tf.slice(                                     # (batch_size, memory_length, output_dim)
            new_memory,
            (0, K.maximum(0, self.memory_len + self.target_len - seq_len - memory_length), 0),
            (batch_size, K.minimum(self.memory_len, memory_length), self.output_dim),
        )

        return old_memory

    def get_config(self):
        config = {
            'batch_size': self.batch_size,
            'memory_len': self.memory_len,
            'target_len': self.target_len,
            'output_dim': self.output_dim,
        }
        base_config = super(Memory, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))
