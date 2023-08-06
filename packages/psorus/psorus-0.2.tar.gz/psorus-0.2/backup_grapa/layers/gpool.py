import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gpool(Layer):
  def __init__(self,gs=20,param=40,mode="max",**kwargs):
    self.gs=gs
    self.param=param
    self.mode=mode
    super(gpool,self).__init__(input_shape=(gs,param))

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]
    if self.mode=="max":
      return K.max(x,axis=-1)
    if self.mode=="mean":
      return K.mean(x,axis=-1)
    if self.mode=="sum":
      return K.sum(x,axis=-1)

    

    
  def compute_output_shape(self,input_shape):
    print("inputting",input_shape,"param",self.param)
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.gs])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"mode":self.mode}
    th=super(gpool,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gpool(**config)













