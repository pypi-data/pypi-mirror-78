import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gcomparamcombinations(Layer):#shall take a 3d layer (?,gs,param) and output a corresponding combination assemble (?,gs,gs,param,2) (param of all combinations of gs) 
  def __init__(self,gs=20,param=30,**kwargs):
    self.gs=gs
    self.param=param
    super(gcomparamcombinations,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                           shape=(self.param,self.c*self.c),
    #                           initializer=self.initializer,
    #                           trainable=self.trainable)


    self.built=True


  def call(self,x):
    x=x[0]#params

    parts=[]
    for i in range(self.gs):
      ac=x[:,i,:self.param]
      ac=K.reshape(ac,(-1,1,1,self.param,1))
      parts.append(ac)

    ret=[]
    for x in range(self.gs):
      toc=[]
      for y in range(self.gs):
        ac=K.concatenate((parts[x],parts[y]),axis=-1)
        toc.append(ac)
      ret.append(K.concatenate(toc,axis=2))
    ret=K.concatenate(ret,axis=1)

    return ret
    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==3
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.param
    return tuple([g_shape[0],self.gs,self.gs,self.param,2])

  def get_config(self):
    mi={"gs":self.gs,"param":self.param}
    th=super(gcomparamcombinations,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomparamcombinations(**config)













