import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gcutparam(Layer):#takes in a param list, and splits it up into two differnt kind of params
  def __init__(self,gs=20,param1=20,param2=20,**kwargs):
    self.gs=gs
    self.param1=param1
    self.param2=param2
    super(gcutparam,self).__init__(**kwargs)


  def get_config(self):
    mi={"gs":self.gs,"param1":self.param1,"param2":self.param2}
    th=super(gcutparam,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcutparam(**config)

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]
    
    x1=x[:,:,:self.param1]
    x2=x[:,:,self.param1:]

 
    x1=K.reshape(x1,(-1,self.gs,self.param1))
    x2=K.reshape(x2,(-1,self.gs,self.param2))#to keep the shape   

 
    return x1,x2

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param1+self.param2
    return tuple([input_shape[0],self.gs,self.param1]),tuple([input_shape[0],self.gs,self.param2])    















