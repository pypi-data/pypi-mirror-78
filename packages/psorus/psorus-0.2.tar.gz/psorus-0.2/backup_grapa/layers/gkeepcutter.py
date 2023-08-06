import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gkeepcutter(Layer):
  def __init__(self,inn=30,param=40,out=20,dimension=0,**kwargs):
    assert inn>=out
    self.inn=inn
    self.param=param
    self.out=out
    self.dimension=dimension
    super(gkeepcutter,self).__init__(input_shape=(inn,inn*(dimension+1)+param))


  def build(self, input_shape):

    self.built=True


  def call(self,x):
    
    x=x[:,:self.out,:]
    mainmat=x[:,:,:self.out]
    otmats=[]
    for i in range(self.dimension):
      otmats.append(x[:,:,self.inn*(i+1):self.inn*(i+1)+self.out])
    params=x[:,:,-self.param:]
    
    otmats.insert(0,mainmat)
    otmats.append(params)

    return K.concatenate(otmats,axis=-1)

    
  def compute_output_shape(self,input_shape):
    assert len(input_shape)==3
    assert input_shape[1]==self.inn
    assert input_shape[2]==self.inn*(self.dimension+1)+self.param
    return tuple([input_shape[0],self.out,self.out*(self.dimension+1)+self.param])    

  def get_config(self):
    mi={"inn":self.inn,"param":self.param,"out":self.out,"dimension":self.dimension}
    th=super(gkeepcutter,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gkeepcutter(**config)













