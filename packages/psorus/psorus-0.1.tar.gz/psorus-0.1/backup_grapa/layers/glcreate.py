import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





#batch_size=100
#epochs=1000
#verbose=2
#lr=0.001



class glcreate(Layer):
  def __init__(self,gs=20,param=40,**kwargs):
    self.gs=gs
    self.param=param

    super(glcreate,self).__init__(**kwargs)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param}
    th=super(glcreate,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return glcreate(**config)
  
  def build(self, input_shape):

    self.built=True

  def call(self,x):
    #print("!",x[0].shape,x[1].shape)
    mat=x[0]
    val=x[1]
    wei=K.batch_dot(mat,val)
      
    ret=K.concatenate((val,wei),axis=-1)

    
    return ret


    
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==3
    assert pshape[-1]==self.gs
    assert pshape[-2]==self.gs

    shape=list(input_shape[1])
    assert len(shape)==3
    assert shape[-1]==self.param
    assert shape[-2]==self.gs

    return tuple([shape[0],self.gs,self.param*2])













