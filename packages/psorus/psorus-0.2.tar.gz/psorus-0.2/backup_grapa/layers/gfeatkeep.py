import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gfeatkeep(Layer):
  def __init__(self,gs=20,param=40,dimension=0,**kwargs):
    self.gs=gs
    self.param=param
    self.dimension=dimension
    super(gfeatkeep,self).__init__(input_shape=(gs,gs*(dimension+1)+param))

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"dimension":self.dimension}
    th=super(gfeatkeep,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gfeatkeep(**config)

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    return x[:,:,-self.param:]
    

    
  def compute_output_shape(self,input_shape):

    #print("called output of gfeatkeep for is=",input_shape)
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.gs*(self.dimension+1)+self.param
    return tuple([input_shape[0],self.gs,self.param])    















