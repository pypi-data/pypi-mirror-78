import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gcomgraphcutter(Layer):#takes a reordered gs*gs graph, and cuts it in pieces of c, which get pooled by a given rule
  def __init__(self,gs=20,c=2,mode="mean",cut=0.5,c_const=1000,**kwargs):
    #c=2
    #mode="min"
    assert gs % c==0#assume there is an equal splitting
    self.gs=gs
    self.c=c
    self.ogs=int(self.gs/self.c)
    self.mode=mode
    self.cut=cut
    self.c_const=c_const
    super(gcomgraphcutter,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                            shape=(self.param*self.c,self.paramo),
    #                            initializer=self.metrik_init,#ignores metrik_init completely
    #                            trainable=self.learnable,
    #                            regularizer=None)



    self.built=True


  def call(self,x):
    A=x[0]#adjacency matrix
 


    Ar=K.reshape(A,(-1,self.ogs,self.c,self.ogs,self.c))
    #print("Ar",Ar.shape)

    if self.mode=="mean":
      Am=K.mean(Ar,axis=(2,4))
    if self.mode=="min":
      Am=K.min(Ar,axis=(2,4))
    if self.mode=="max":
      Am=K.max(Ar,axis=(2,4))

    #print("Am",Am.shape)
    
    C=self.c_const
    cut=self.cut
    
    Ar=K.relu(1+C*(Am-cut))-K.relu(C*(Am-cut))
    

    #print("Ar",Ar.shape)


    #exit()


    return Ar



    exit()

    

    
  def compute_output_shape(self,input_shape):
    grap_shape=input_shape[0]
    assert len(grap_shape)==3
    assert grap_shape[1]==self.gs
    assert grap_shape[2]==self.gs
    return tuple([grap_shape[0],self.ogs,self.ogs])

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"c":self.c,"metrik_init":self.metrik_init,"learnable":self.learnable,"paramo":self.paramo,"mode":self.mode,"cut":self.cut,"c_const":self.c_const}
    th=super(gcomgraphcutter,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomgraphcutter(**config)













