import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gkeepbuilder(Layer):
  def __init__(self,gs=30,param=10,free=30,learnable=True,dimension=0,use0=False,**kwargs):
    self.gs=gs
    self.param=param
    self.free=free
    self.learnable=True
    self.dimension=dimension
    self.use0=use0
    super(gkeepbuilder,self).__init__(input_shape=(gs,(gs*(dimension+1))+param))

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"free":self.free,"learnable":self.learnable,"dimension":self.dimension,"use0":self.use0}
    th=super(gkeepbuilder,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gkeepbuilder(**config)


  def fromdistsq(self,dsq):
    return K.exp(-dsq)

  def build(self, input_shape):
    if self.use0:
      self.metrik=self.add_weight(name="weight",
                                shape=(self.dimension+1,1),
                                initializer=keras.initializers.Ones(),
                                trainable=self.learnable)
    else:
      self.metrik=self.add_weight(name="weight",
                                shape=(self.dimension,1),
                                initializer=keras.initializers.Ones(),
                                trainable=self.learnable)
    self.built=True
  def lisshape(self,x):
    ret=[]
    for e in x:
      ret.append(e.shape)
    return ret
  def call(self,x):
    #print(x.shape)
   
    gs=self.gs 
    mats=[]
    for i in range(self.dimension+1):
      amat=(x[:,:gs,gs*i:gs*(i+1)])
      amat=K.reshape(amat,(-1,gs,gs,1))
      mats.append(amat)
    data=x[:,:gs,gs*(self.dimension+1):]

    mat0=mats[0]
    if self.use0:
      mat=K.concatenate(mats,axis=-1)
    else:
      mat=K.concatenate(mats[1:],axis=-1)
    metrik=self.metrik


    
    dsq=K.dot(mat,metrik)
    
    basegraph=self.fromdistsq(dsq)
    #mats.insert(0,basegraph)
    mats[0]=basegraph
    pregraph=K.concatenate(mats,axis=2)
    basegraph=K.reshape(pregraph,(-1,gs,gs*(self.dimension+1))) 
     
    #print(metrik.shape,xm.shape,xt.shape,dsq.shape)
    #print(basegraph.shape)
    
    parax=data
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
    #print("!!!", K.concatenate((basegraph,parax,zeros)).shape,basegraph.shape,pregraph.shape,parax.shape,zeros.shape,self.lisshape(mats)) 
    return K.concatenate((basegraph,parax,zeros))

    
  def compute_output_shape(self,input_shape):
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.gs*(1+self.dimension)+self.param
    return tuple([input_shape[0],input_shape[1],input_shape[2]+self.free])    















