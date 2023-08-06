import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace


def R(self,x,c_const=1000.0,cut=0.5):
  return K.relu(c_const*(x-cut)+1)-K.relu(c_const*(x-c_const))
def doand(x,mode="prod",c_const=1000.0,cut=0.5):


  if mode=="and":
    ret=R(K.prod(x,axis=-1),c_const=c_const,cut=cut)
  if mode=="prod":
    ret=K.prod(x,axis=-1)
  if mode=="or":
    ret=R(K.sum(x,axis=-1),c_const=c_const,cut=cut)
  if mode=="sum":
    ret=K.sum(x,axis=-1)


  return ret



class gcomgraphand2(Layer):#is capable of running "and" operations on two (?,c*gs,c*gs) graphs, resulting in (?,c*gs,c*gs) 
  def __init__(self,gs=20,c=2,mode="prod",cut=0.5,c_const=1000.0,**kwargs):
    self.gs=gs
    self.c=c
    self.mode=mode
    self.cut=cut
    self.c_const=c_const
    super(gcomgraphand2,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                           shape=(self.param,self.c*self.c),
    #                           initializer=self.initializer,
    #                           trainable=self.trainable)


    self.built=True

  def call(self,q):
    y=q[1]
    x=q[0]

    x=K.reshape(x,(-1,self.gs*self.c,self.gs*self.c,1))
    y=K.reshape(y,(-1,self.gs*self.c,self.gs*self.c,1))

    q=K.concatenate((x,y),axis=-1)

    ret=doand(q,mode=self.mode,c_const=self.c_const,cut=self.cut)
    
    return ret

    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    g_shape2=input_shape[1]
    assert len(g_shape)==3
    assert g_shape[1]==self.gs*self.c
    assert g_shape[2]==self.gs*self.c
    assert g_shape2[1]==self.gs*self.c
    assert g_shape2[2]==self.gs*self.c
    return tuple([g_shape[0],self.gs*self.c,self.gs*self.c])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c,"mode":self.mode,"cut":self.cut,"c_const":self.c_const}
    th=super(gcomgraphand2,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomgraphand2(**config)













