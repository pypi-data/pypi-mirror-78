import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gtlbuilder(Layer):
  def __init__(self,gs=30,param=10,free=30,**kwargs):
    self.gs=gs
    self.param=param
    self.free=free
    super(gtlbuilder,self).__init__(input_shape=(gs,gs+gs+param))

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"free":self.free}
    th=super(gtlbuilder,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gtlbuilder(**config)


  def getmetrik(self):
    return [[1],[1]]
  def fromdistsq(self,dsq):
    return K.exp(-dsq)

  def build(self, input_shape):
    self.metrik=self.add_weight(name="weight",
                                shape=(2,1),
                                initializer=keras.initializers.Ones(),
                                trainable=True)
    self.built=True

  def call(self,x):
    #print(x.shape)
   
    gs=self.gs 
    mata=x[:,:gs,:gs]
    matb=x[:,:gs,gs:gs+gs]
    data=x[:,:gs,gs+gs:]

    mata=K.reshape(mata,(-1,gs,gs,1))
    matb=K.reshape(matb,(-1,gs,gs,1))
     
    mat=K.concatenate((mata,matb),axis=-1)
    metrik=self.metrik
    
    dsq=K.reshape(K.dot(mat,metrik),(-1,gs,gs))
    
    basegraph=self.fromdistsq(dsq)
    
    
     
    #print(metrik.shape,xm.shape,xt.shape,dsq.shape)
    #print(basegraph.shape)
    
    parax=x[:,:,self.gs+self.gs:]#please note, that this layer is build to read two times the same data: first the one for the distance generation, and afterwards the one for node data, also note, that glbuilder does not do this, but instead works on the same dataset
    #print(parax.shape)
    
    if self.free==0:return K.concatenate((basegraph,parax),axis=-1) 
    zero1=K.zeros_like(x[:,:,0])
    zero1=K.reshape(zero1,(-1,x.shape[1],1))
    #print("!",zero1.shape)
    zerolis=[]
    for i in range(self.free):
      zerolis.append(zero1)
    zeros=K.concatenate(zerolis,axis=-1)
    #print(zeros.shape)
    
    return K.concatenate((basegraph,parax,zeros))

    
  def compute_output_shape(self,input_shape):
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.gs+self.gs+self.param
    return tuple([input_shape[0],self.gs,self.gs+self.param+self.free])    















