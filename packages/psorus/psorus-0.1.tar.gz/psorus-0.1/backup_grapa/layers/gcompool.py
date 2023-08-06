import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gcompool(Layer):
  def __init__(self,gs=20,param=40,paramo=40,c=2,metrik_init="glorot_uniform",learnable=True,**kwargs):
    assert gs % c==0#assume there is an equal splitting
    self.gs=gs
    self.param=param
    self.metrik_init=metrik_init
    self.c=c
    self.ogs=int(self.gs/self.c)
    self.learnable=learnable
    self.paramo=paramo
    super(gcompool,self).__init__(**kwargs)

  def build(self, input_shape):

    self.trafo=self.add_weight(name="trafo",
                                shape=(self.param*self.c,self.paramo),
                                initializer=self.metrik_init,#ignores metrik_init completely
                                trainable=self.learnable,
                                regularizer=None)

#    self.metrik=self.add_weight(name="metrik",
#                                shape=(self.param,1),
#                                initializer=keras.initializers.ones(),#ignores metrik_init completely
#                                trainable=not self.learnable,
#                                regularizer=None)


    self.built=True


  def call(self,x):
    x=x[0]
 
    print("x",x.shape)
    

    print("trafo",self.trafo.shape)


    #currently just uses the last value as sorting param
    values=x[:,:,-1]#K.reshape(K.dot(x,self.metrik),(-1,self.gs))
    print("values",values.shape)

    _,valueorder=t.math.top_k(values,k=self.gs)
    print("valueorder",valueorder.shape)

    #valueorder=t.argsort(values,axis=-1)
    #print("valueorder",valueorder.shape)

    xg=t.gather(params=x,indices=valueorder,axis=1,batch_dims=1)
    print("xg",xg.shape)

    #exit()

    xs=K.reshape(xg,(-1,self.ogs,self.param*self.c))
    print("xs",xs.shape)


    traf=K.dot(xs,self.trafo)
    print("traf",traf.shape)

    return traf



    exit()

    

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.ogs,self.paramo])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"c":self.c,"metrik_init":self.metrik_init,"learnable":self.learnable,"paramo":self.paramo}
    th=super(gcompool,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcompool(**config)













