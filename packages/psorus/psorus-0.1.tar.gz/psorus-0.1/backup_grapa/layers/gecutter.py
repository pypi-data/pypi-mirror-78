import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gecutter(Layer):#like gcutter, but leaves only the last elements
  def __init__(self,inn=30,param=40,out=20,**kwargs):
    assert inn>=out
    self.inn=inn
    self.param=param
    self.out=out
    super(gecutter,self).__init__(**kwargs)


  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]
 
    return x[:,-self.out:,:self.param]

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[-1]==self.param
    assert input_shape[-2]==self.inn
    return tuple([input_shape[0],self.out,self.param])    

  def get_config(self):
    mi={"inn":self.inn,"param":self.param,"out":self.out}
    th=super(gecutter,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gecutter(**config)













