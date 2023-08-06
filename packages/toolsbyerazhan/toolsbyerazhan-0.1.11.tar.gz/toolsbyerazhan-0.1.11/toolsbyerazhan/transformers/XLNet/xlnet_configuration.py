import tensorflow as tf
import numpy as np

class XLNetConfig(object):
    #model_type = "xlnet"
    #erazhan:最好还是从config.json中得到
    def __init__(
        self,
        vocab_size = 32000,
        d_model = 1024,
        n_layer = 24,
        n_head = 16,
        d_inner = 4096,
        ff_activation = "gelu",
        untie_r = True,#暂不
        attn_type = "bi",
        initializer_range = 0.02,#暂不
        layer_norm_eps = 1e-12,
        dropout = 0.1,
        mem_len = None,
        reuse_len = None,#暂不
        bi_data = False,#相对位置向量中
        clamp_len = -1,#同上
        same_length = False,
        summary_type = "last",#暂不
        summary_use_proj = True,#暂不
        summary_activation = "tanh",#暂不
        summary_last_dropout = 0.1,#暂不
        start_n_top = 5,#暂不
        end_n_top = 5,#暂不
        pad_token_id = 5,
        bos_token_id = 1,
        eos_token_id = 2,
        **kwargs
    ):
        
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.n_layer = n_layer
        self.n_head = n_head
        assert d_model % n_head == 0,"d_model must be an integral multiple of n_head "
        if "d_head" in kwargs:
            assert (kwargs["d_head"] == d_model // n_head), "`d_head` ({kwargs['d_head']}) should be equal to `d_model // n_head` ({d_model // n_head})"
        self.d_head = d_model // n_head
        self.ff_activation = ff_activation
        self.d_inner = d_inner
        self.untie_r = untie_r
        self.attn_type = attn_type

        self.initializer_range = initializer_range
        self.layer_norm_eps = layer_norm_eps

        self.dropout = dropout
        self.mem_len = mem_len
        self.reuse_len = reuse_len
        self.bi_data = bi_data
        self.clamp_len = clamp_len
        self.same_length = same_length

        self.summary_type = summary_type
        self.summary_use_proj = summary_use_proj
        self.summary_activation = summary_activation
        self.summary_last_dropout = summary_last_dropout
        self.start_n_top = start_n_top
        self.end_n_top = end_n_top

        self.bos_token_id = bos_token_id
        self.pad_token_id = pad_token_id
        self.eos_token_id = eos_token_id

        if mem_len is None or mem_len == 0:
            #源码中用了warning.warn()
            print("Warning: This config doesn't use attention memories, a core feature of XLNet.")
            
