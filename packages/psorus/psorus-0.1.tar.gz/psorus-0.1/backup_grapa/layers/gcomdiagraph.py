import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gcomdiagraph(Layer):
  def __init__(self,gs=20,c=2,**kwargs):
    #c=2
    #mode="min"
    assert gs % c==0#assume there is an equal splitting
    self.gs=gs
    self.c=c
    self.ogs=int(self.gs/self.c)
    super(gcomdiagraph,self).__init__(**kwargs)

  def build(self, input_shape):




    self.built=True


  def call(self,x):
    A=x[0]#reordered matrix gs*gs

    #shall take A and take the ogs diagonal c*c matrices, and concat them   

    graphs=[]

    ogs=self.ogs
    c=self.c

    for i in range(ogs):
      start=i*c
      end=(i+1)*c
      amat=A[:,start:end,start:end]
      amat=K.reshape(amat,(-1,1,c,c))
      graphs.append(amat)
    

    ret=K.concatenate(graphs,axis=1)

    return ret


    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==3
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.gs
    return tuple([g_shape[0],self.ogs,self.c,self.c])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c}
    th=super(gcomdiagraph,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomdiagraph(**config)













