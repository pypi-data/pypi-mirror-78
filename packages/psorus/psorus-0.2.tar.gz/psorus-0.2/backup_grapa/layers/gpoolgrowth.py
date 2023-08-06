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



class gpoolgrowth(Layer):
  def __init__(self,inn=20,out=30,param=40,kernel_initializer="glorot_uniform",**kwargs):
    self.inn=inn
    self.out=out
    self.param=param
    self.kernel_initializer=kernel_initializer
    super(gpoolgrowth,self).__init__(**kwargs)

  def get_config(self):
    mi={"inn":self.inn,"out":self.out,"param":self.param}
    th=super(gpoolgrowth,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gpoolgrowth(**config)
  
  def build(self, input_shape):

    self.inc=self.add_weight(name='inc',
                                shape=(self.param,self.param*(self.out-self.inn)),
                                initializer=self.kernel_initializer,
                                trainable=True)
    self.built=True

  def call(self,x):
    s=x[0]
    add=x[1]

    
    fa=K.dot(s,self.inc)
    fr=K.reshape(fa,(-1,self.out-self.inn,self.param))
    r=K.conatenate((add,fr),axis=-2)
    
    return r
    
     

 
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    xshape=list(input_shape[1])
    assert len(pshape)==2
    assert len(xshape)==3
    assert pshape[-1]==self.param
    assert xshape[-1]==self.param
    assert xshape[-2]==self.inn
    ret=[pshape[0],self.out,self.out]
    return tuple(ret)













