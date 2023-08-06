#NOTWORKINGYET
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



class gsym(Layer):
  def __init__(self,gs=20,**kwargs):
    self.gs=gs
    super(gsym,self).__init__(**kwargs)

  def get_config(self):
    mi={"gs":self.gs}
    th=super(gsym,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gsym(**config)
  
  def build(self, input_shape):

    self.built=True

  def call(self,x):
    x=x[0]
    xp=K.permute_dimensions(x,(0,2,1))
    
    s=x+xp
    s=K.relu(5*s)-K.relu(5*s-1)    
    
    return s
   

 
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==3
    assert pshape[-1]==self.gs
    assert pshape[-2]==self.gs
    return tuple(pshape)













