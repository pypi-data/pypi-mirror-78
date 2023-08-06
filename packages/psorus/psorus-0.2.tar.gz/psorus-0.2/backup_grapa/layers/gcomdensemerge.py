import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gcomdensemerge(Layer):
  def __init__(self,gs=20,param=30,paramo=40,ags=10,initializer="glorot_uniform",trainable=True,**kwargs):
    #c=2
    #mode="min"
    self.gs=gs
    self.param=param
    self.paramo=paramo
    self.ags=ags
    self.initializer=initializer
    self.trainable=trainable
    super(gcomdensemerge,self).__init__(**kwargs)

  def build(self, input_shape):

    self.trafo=self.add_weight(name="trafo",
                               shape=(self.ags*self.param,self.paramo),
                               initializer=self.initializer,
                               trainable=self.trainable)


    self.built=True


  def call(self,x):
    x=x[0]#params

    #shall take a 4d feature vector of shape (-1,gs,ags,param), and transform it using trafo into (-1,gs,paramo)

    #print("x",x.shape)

    xi=K.reshape(x,(-1,self.gs,self.ags*self.param))
    #print("xi",xi.shape)

    xt=K.dot(xi,self.trafo)
    #print("xt",xt.shape)


    return xt

    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==4
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.ags
    assert g_shape[3]==self.param
    return tuple([g_shape[0],self.gs,self.paramo])

  def get_config(self):
    mi={"gs":self.gs,"ags":self.ags,"param":self.param,"paramo":self.paramo,"initializer":self.initializer,"trainable":self.trainable}
    th=super(gcomdensemerge,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomdensemerge(**config)













