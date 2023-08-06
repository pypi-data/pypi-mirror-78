import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gchooseparam(Layer):
  def __init__(self,gs=50,param=30,q=[0,3],**kwargs):
    self.gs=gs
    self.param=param
    self.q=q
    super(gchooseparam,self).__init__(**kwargs)


  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]

    parts=[]
    for q in self.q:
      ac=K.reshape(x[:,:self.gs,q],(-1,self.gs,1))
      parts.append(ac)

    ret=K.concatenate(parts,axis=-1)   

 

    return ret

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[-1]==self.param
    assert input_shape[-2]==self.gs
    return tuple([input_shape[0],self.gs,len(self.q)])    

  def get_config(self):
    mi={"param":self.param,"gs":self.gs,"q":self.q}
    th=super(gchooseparam,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gchooseparam(**config)













