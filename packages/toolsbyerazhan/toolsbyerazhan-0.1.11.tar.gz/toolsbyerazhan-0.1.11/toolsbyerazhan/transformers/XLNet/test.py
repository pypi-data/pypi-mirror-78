import tensorflow as tf
import numpy as np

from xlnet_layers import CreateMask
from utils import *

#[batch_size,seq_length]
inputs = tf.convert_to_tensor([[0,2,1],[0,1,1]],dtype = tf.int32)
masks = CreateMask(mask_value=1)(inputs)
print(inputs.numpy())
print(masks.numpy())
