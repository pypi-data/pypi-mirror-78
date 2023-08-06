import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gcomreopool(Layer):
  def __init__(self,gs=20,param=40,**kwargs):
    #c=2
    #mode="min"
    self.gs=gs
    self.param=param
    super(gcomreopool,self).__init__(**kwargs)

  def build(self, input_shape):



    self.built=True


  def call(self,x):
    A=x[0]#adjacency matrix
    x=x[1]#parameters
 
    #print("x",x.shape)
    #print("A",A.shape) 

    #print("trafo",self.trafo.shape)


    #currently just uses the last value as sorting param
    values=x[:,:,-1]#K.reshape(K.dot(x,self.metrik),(-1,self.gs))
    #print("values",values.shape)

    _,valueorder=t.math.top_k(values,k=self.gs)
    #print("valueorder",valueorder.shape)

    #valueorder=t.argsort(values,axis=-1)
    #print("valueorder",valueorder.shape)

    xg=t.gather(params=x,indices=valueorder,axis=1,batch_dims=1)
    #print("xg",xg.shape)

    #exit()

    #xs=K.reshape(xg,(-1,self.ogs,self.param*self.c))
    #print("xs",xs.shape)


    #traf=K.dot(xs,self.trafo)
    #print("traf",traf.shape)



    At1=t.gather(params=A,indices=valueorder,axis=1,batch_dims=1)
    At2=t.gather(params=At1,indices=valueorder,axis=2,batch_dims=1)

    return At2,xg



    exit()

    

    
  def compute_output_shape(self,input_shape):
    grap_shape=input_shape[0]
    input_shape=input_shape[1]
    assert len(input_shape)==3
    assert len(grap_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    assert grap_shape[1]==self.gs
    assert grap_shape[2]==self.gs
    return tuple([grap_shape[0],self.gs,self.gs]),tuple([input_shape[0],self.gs,self.param])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param}
    th=super(gcomreopool,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomreopool(**config)













