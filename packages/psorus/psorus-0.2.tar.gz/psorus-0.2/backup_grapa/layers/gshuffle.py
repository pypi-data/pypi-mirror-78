import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gshuffle(Layer):#shuffles the param
  def __init__(self,gs=20,param=40,seed=None,**kwargs):
    self.gs=gs
    self.param=param
    self.seed=seed
    super(gshuffle,self).__init__(input_shape=(gs,param))

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]

    x=K.reshape(x,(-1,self.gs,self.param))

    x=K.permute_dimensions(x,(2,0,1))#can only shuffle the first dimension 

    x=t.random.shuffle(x,seed=self.seed)
    
    x=K.permute_dimensions(x,(1,2,0))#dispermute

    return x


  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    if len(input_shape)==2 and self.gs==1:
      assert input_shape[1]==self.param
      return tuple([input_shape[0],self.gs,self.param])
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.gs,self.param])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"seed":self.seed}
    th=super(gshuffle,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gshuffle(**config)













