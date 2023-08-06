import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace

from grapa.layers.kron import kronecker_product_b1 as kron_b1



class gcomgraphlevel(Layer):#takes a (?,gs,gs,c,c) and converts it into (?,c*gs,c*gs)
  def __init__(self,gs=20,c=2,**kwargs):
    self.gs=gs
    self.c=c
    super(gcomgraphlevel,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                           shape=(self.param,self.c*self.c),
    #                           initializer=self.initializer,
    #                           trainable=self.trainable)


    self.built=True

  #def R(self,x):
  #  return K.relu(self.c_const*(x-self.cut)+1)-K.relu(self.c_const*(x-self.c_const))
  def call(self,x):
    x=x[0]
    #print("x",x.shape)
    #exit()
    xp=K.permute_dimensions(x,(0,1,3,2,4))

    ret=K.reshape(xp,(-1,self.gs*self.c,self.gs*self.c))
    

    return ret

    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==5
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.gs
    assert g_shape[3]==self.c
    assert g_shape[4]==self.c
    return tuple([g_shape[0],self.gs*self.c,self.gs*self.c])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c}
    th=super(gcomgraphlevel,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomgraphlevel(**config)













