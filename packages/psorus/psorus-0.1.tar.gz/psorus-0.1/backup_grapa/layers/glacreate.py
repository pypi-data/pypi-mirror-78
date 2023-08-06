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



class glacreate(Layer):
  def __init__(self,gs=20,param=40,a=2,**kwargs):
    self.gs=gs
    self.param=param
    self.a=a

    super(glacreate,self).__init__(**kwargs)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"a":self.a}
    th=super(glacreate,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return glacreate(**config)
  
  def build(self, input_shape):

    self.built=True

  def call(self,x):
    #print("!",x[0].shape,x[1].shape)
    mat=x[0]
    val=x[1]

    rmat=K.reshape(mat,(-1,self.gs,self.gs))
    rval=K.reshape(val,(-1,self.gs,self.param))
    
    rwei=K.batch_dot(rmat,rval)
    wei=K.reshape(rwei,(-1,self.a,self.gs,self.param)) 



    ret=K.concatenate((val,wei),axis=-1)

    
    return ret


    
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==4
    assert pshape[-3]==self.a
    assert pshape[-1]==self.gs
    assert pshape[-2]==self.gs

    shape=list(input_shape[1])
    assert len(shape)==4
    assert shape[-3]==self.a
    assert shape[-1]==self.param
    assert shape[-2]==self.gs

    return tuple([shape[0],self.a,self.gs,self.param*2])













