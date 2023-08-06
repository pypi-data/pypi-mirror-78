import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gfeat(Layer):
  def __init__(self,gs=20,param=40,**kwargs):
    self.gs=gs
    self.param=param
    super(gfeat,self).__init__(input_shape=(gs,param))

  def get_config(self):
    mi={"gs":self.gs,"param":self.param}
    th=super(gfeat,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gfeat(**config)

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    return x[:,:,self.gs:self.gs+self.param]
    

    
  def compute_output_shape(self,input_shape):
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.gs+self.param
    return tuple([input_shape[0],self.gs,self.param])    















