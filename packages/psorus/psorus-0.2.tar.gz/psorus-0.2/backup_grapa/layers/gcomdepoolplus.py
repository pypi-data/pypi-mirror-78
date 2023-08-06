import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gcomdepoolplus(Layer):#simply produces a constant graph additionally to gcomdepool
  def __init__(self,gs=20,param=40,paramo=40,c=2,metrik_init="glorot_uniform",graph_init=keras.initializers.Identity(),learnable=True,**kwargs):
    self.gs=gs
    self.param=param
    self.metrik_init=metrik_init
    self.graph_init=graph_init
    self.c=c
    self.ogs=int(self.gs*self.c)
    self.learnable=learnable
    self.paramo=paramo
    super(gcomdepoolplus,self).__init__(**kwargs)

  def build(self, input_shape):

    self.trafo=self.add_weight(name="trafo",
                                shape=(self.param,self.paramo*self.c),
                                initializer=self.metrik_init,
                                trainable=self.learnable,
                                regularizer=None)

    self.graph=self.add_weight(name="graph",
                                shape=(self.c,self.c),
                                initializer=self.graph_init,
                                trainable=self.learnable,
                                regularizer=None)


    self.built=True


  def call(self,x):
    x=x[0]
 
    #print("x",x.shape)
    

    #print("trafo",self.trafo.shape)


    traf=K.dot(x,self.trafo)
    #print("traf",traf.shape)


    ret=K.reshape(traf,(-1,self.ogs,self.paramo))
    #print("ret",ret.shape)
    
    return ret,self.graph

    #exit()

  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.ogs,self.paramo]),tuple([self.c,self.c])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"c":self.c,"metrik_init":self.metrik_init,"graph_init":self.graph_init,"learnable":self.learnable,"paramo":self.paramo}
    th=super(gcomdepoolplus,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomdepoolplus(**config)













