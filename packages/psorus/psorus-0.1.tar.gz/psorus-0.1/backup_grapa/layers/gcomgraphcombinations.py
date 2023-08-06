import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gcomgraphcombinations(Layer):#shall take a 4d layer (?,gs,c,c) and output a corresponding combination assamble (?,gs,gs,c,c,2) (c,c of all combinations of gs) 
  def __init__(self,gs=20,c=2,**kwargs):
    self.gs=gs
    self.c=c
    super(gcomgraphcombinations,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                           shape=(self.param,self.c*self.c),
    #                           initializer=self.initializer,
    #                           trainable=self.trainable)


    self.built=True


  def call(self,x):
    x=x[0]#params

    parts=[]
    for i in range(self.gs):
      ac=x[:,i,:self.c,:self.c]
      ac=K.reshape(ac,(-1,1,1,self.c,self.c,1))
      parts.append(ac)

    ret=[]
    for x in range(self.gs):
      toc=[]
      for y in range(self.gs):
        ac=K.concatenate((parts[x],parts[y]),axis=-1)
        toc.append(ac)
      ret.append(K.concatenate(toc,axis=2))
    ret=K.concatenate(ret,axis=1)

    return ret
    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==4
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.c
    assert g_shape[3]==self.c
    return tuple([g_shape[0],self.gs,self.gs,self.c,self.c,2])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c}
    th=super(gcomgraphcombinations,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomgraphcombinations(**config)













