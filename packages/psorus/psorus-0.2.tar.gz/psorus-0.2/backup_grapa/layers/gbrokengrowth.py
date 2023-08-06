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



class gbrokengrowth(Layer):
  def __init__(self,inn=20,out=30,param=40,kernel_initializer="glorot_uniform",**kwargs):
    self.inn=inn
    self.out=out
    self.param=param
    self.kernel_initializer=kernel_initializer
    super(gbrokengrowth,self).__init__(**kwargs)

  def get_config(self):
    mi={"inn":self.inn,"out":self.out,"param":self.param}
    th=super(gbrokengrowth,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gbrokengrowth(**config)
  
  def build(self, input_shape):

    self.inc=self.add_weight(name='inc',
                                shape=(self.param*self.inn,self.param*(self.out-self.inn)),
                                initializer=self.kernel_initializer,
                                trainable=True)
    self.built=True

  def call(self,x):
    x=x[0]
    
    f=K.reshape(x,(-1,self.param*self.inn))
    fa=K.dot(f,self.inc)
    r=K.concatenate((f,fa),axis=-1)
    
    return K.reshape(r,(-1,self.out,self.param))
    
     

 
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==3
    assert pshape[-1]==self.param
    assert pshape[-2]==self.inn
    pshape[-2]=self.out
    return tuple(pshape)













