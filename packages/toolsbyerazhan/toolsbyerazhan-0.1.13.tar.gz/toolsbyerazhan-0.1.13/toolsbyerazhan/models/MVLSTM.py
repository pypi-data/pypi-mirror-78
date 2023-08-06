import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import Layer,Embedding,Bidirectional,LSTM,Input,Dot,Reshape,Lambda,Dense,Dropout

#from tensorflow.keras import Sequential

class MVLSTM(tf.keras.Model):
    def __init__(self, hyper_params, *args, **kwargs):
        super(MVLSTM,self).__init__(*args,**kwargs)
        self.hp = hyper_params
        self.embeddings = Embedding(self.hp.vocab_size,self.hp.embed_units,mask_zero = True)

        self.bilstm1 = Bidirectional(LSTM(self.hp.num_units,return_sequences=True,dropout=self.hp.dropout))
        self.bilstm2 = Bidirectional(LSTM(self.hp.num_units,return_sequences=True,dropout=self.hp.dropout))

        self.mlp_layer = [Dense(self.hp.mlp_num_units,activation=self.hp.mlp_activation) for _ in range(self.hp.num_mlp_layer)]
        self.mlp_layer.append(Dense(self.hp.mlp_num_fan_out,activation=self.hp.mlp_activation))
        
        self.dropout=Dropout(rate=self.hp.dropout)

        #预测模型，采用hinge_loss,也可以考虑分类模型
        self.dense=Dense(1,activation='linear')
        

    def build(self,input_shape):
        if self.hp.bilinear:
            self.bilinear = self.add_weight(name = "bilinear weight",shape = (self.hp.embed_units,self.hp.embed_units),initializer = 'glorot_uniform',trainable = True)

        super(MVLSTM,self).build(input_shape)
        
    def call(self,inputs):
        """inputs:[left,right],left:[batch_size,T1],right:[batch_size,T2]"""
        
        #inputs作为列表输入
        left,right=inputs[0],inputs[1]
        
        left = self.embedding(left)
        right = self.embedding(right)
        
        left = self.bilstm1(left)#[batch_size,T1,embed_size]
        right = self.bilstm2(right)#[batch_size,T2,embed_size]
        
        match_matrix = Dot(axes=[2,2],normalize = False)([left,right])
        
        matching_signals=Reshape((-1,))(match_matrix)
