import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gadd1(Layer):#used to simply train gltk on glmp data
  def __init__(self,gs=20,**kwargs):
    self.gs=gs
    super(gadd1,self).__init__(**kwargs)

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]
    return x+K.eye(self.gs)
    

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.gs
    return tuple([input_shape[0],self.gs,self.gs])    

  def get_config(self):
    mi={"gs":self.gs}
    th=super(gadd1,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gadd1(**config)













