import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gfromparam(Layer):
  def __init__(self,gs=1,param=40,**kwargs):
    self.gs=gs
    self.param=param
    super(gfromparam,self).__init__(**kwargs)

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]

    return K.reshape(x,(-1,self.gs,self.param))

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==2
    assert input_shape[1]==self.gs*self.param
    return tuple([input_shape[0],self.gs,self.param])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param}
    th=super(gfromparam,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gfromparam(**config)













