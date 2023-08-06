import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gcomparastract(Layer):
  def __init__(self,gs=20,param=30,c=2,**kwargs):
    #c=2
    #mode="min"
    assert gs % c==0#assume there is an equal splitting
    self.gs=gs
    self.param=param
    self.c=c
    self.ogs=int(self.gs/self.c)
    super(gcomparastract,self).__init__(**kwargs)

  def build(self, input_shape):




    self.built=True


  def call(self,x):
    x=x[0]#reordered params gs*param

    #shall take x and take out the ogs c*param features, and concat them   

    feats=[]

    ogs=self.ogs
    c=self.c

    for i in range(ogs):
      start=i*c
      end=(i+1)*c
      amat=x[:,start:end,:self.param]
      amat=K.reshape(amat,(-1,1,c,self.param))
      feats.append(amat)
    

    ret=K.concatenate(feats,axis=1)

    return ret


    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==3
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.param
    return tuple([g_shape[0],self.ogs,self.c,self.param])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c,"param":self.param}
    th=super(gcomparastract,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomparastract(**config)













