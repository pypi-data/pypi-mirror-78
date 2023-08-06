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



class gmake1graph(Layer):
  def __init__(self,**kwargs):
    super(gmake1graph,self).__init__(**kwargs)

  def get_config(self):
    mi={}
    th=super(gmake1graph,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gmake1graph(**config)
  
  def build(self, input_shape):

    self.built=True

  def call(self,x):
    x=x[0]

    xs=x.shape
    par=1
    for i in range(1,len(xs)):
      par*=xs[i]


    x=K.reshape(x,[-1,par])[:,0]*0+1
    x=K.reshape(x,[-1,1,1])


    return x


 
  def compute_output_shape(self,input_shape):
    shape=list(input_shape[0])
    assert len(shape)>1
    return tuple([shape[0],1,1])













