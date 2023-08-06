import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gcomdensediverge(Layer):#shall take a 3d layer (?,gs,param) and output a 4d layer (?,gs,c,paramo)
  def __init__(self,gs=20,param=30,paramo=40,c=2,initializer="glorot_uniform",trainable=True,**kwargs):
    #c=2
    #mode="min"
    self.gs=gs
    self.param=param
    self.paramo=paramo
    self.c=c
    self.initializer=initializer
    self.trainable=trainable
    super(gcomdensediverge,self).__init__(**kwargs)

  def build(self, input_shape):

    self.trafo=self.add_weight(name="trafo",
                               shape=(self.param,self.paramo*self.c),
                               initializer=self.initializer,
                               trainable=self.trainable)


    self.built=True


  def call(self,x):
    x=x[0]#params

    #shall take a 3d feature vector of shape (-1,gs,param), and transform it using trafo into (-1,gs,c,paramo)

    #print("x",x.shape)

    #xi=K.reshape(x,(-1,self.gs,self.ags*self.param))
    #print("xi",xi.shape)

    xt=K.dot(x,self.trafo)
    #print("xt",xt.shape)

    xp=K.reshape(xt,(-1,self.gs,self.c,self.paramo))
    
    #print("xp",xp.shape)

    #exit()

    return xp

    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==3
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.param
    return tuple([g_shape[0],self.gs,self.c,self.paramo])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c,"param":self.param,"paramo":self.paramo,"initializer":self.initializer,"trainable":self.trainable}
    th=super(gcomdensediverge,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomdensediverge(**config)













