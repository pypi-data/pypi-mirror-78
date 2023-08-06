import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gcomfullyconnected(Layer):#shall take a 3d parameter layer (?,gs,param) and output a fully connected graph of type (?,gs,gs) 
  def __init__(self,gs=20,param=30,**kwargs):
    #c=2
    #mode="min"
    assert gs>0 and param>0
    self.gs=gs
    self.param=param
    super(gcomfullyconnected,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                           shape=(self.param,self.c*self.c),
    #                           initializer=self.initializer,
    #                           trainable=self.trainable)


    self.built=True


  def call(self,x):
    x=x[0]#params  (?,gs,param)
     
    s=x[:,0,0]
    s=K.reshape(s,(-1,1,1))
    s*=0.0
    s+=1.0

    ret=[]
    for i in range(self.gs):
      toa=[]
      for j in range(self.gs):
         toa.append(s)
      ret.append(K.concatenate(toa,axis=1))
    ret=K.concatenate(ret,axis=2)

    return ret 




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==3
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.param
    return tuple([g_shape[0],self.gs,self.gs])

  def get_config(self):
    mi={"gs":self.gs,"param":self.param}
    th=super(gcomfullyconnected,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomfullyconnected(**config)













