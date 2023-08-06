import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class ghealparam(Layer):#takes in a splittet param list (created by gcutparam), and merges them again
  def __init__(self,gs=20,param1=20,param2=20,**kwargs):
    self.gs=gs
    self.param1=param1
    self.param2=param2
    super(ghealparam,self).__init__(**kwargs)

  def get_config(self):
    mi={"gs":self.gs,"param1":self.param1,"param2":self.param2}
    th=super(ghealparam,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return ghealparam(**config)

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x1=x[0]
    x2=x[1]
   
    r=K.concatenate((x1,x2),axis=-1)

 
    
    return r

    
  def compute_output_shape(self,input_shape):
    assert len(input_shape)==2
    i1=input_shape[0]
    i2=input_shape[1]
    assert len(i1)==3
    assert len(i2)==3
    assert i1[1]==self.gs
    assert i2[1]==self.gs
    assert i1[2]==self.param1
    assert i2[2]==self.param2
    return tuple([input_shape[0],self.gs,self.param1+self.param2])    















