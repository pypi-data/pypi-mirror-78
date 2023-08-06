import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gmultiply(Layer):
  def __init__(self,gs=30,param=40,c=2,**kwargs):
    self.gs=gs
    self.param=param
    self.c=c
    super(gmultiply,self).__init__(**kwargs)


  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]
   



    l=[]
    for i in range(self.c):
      l.append(x)

    #print("l",l,len(l),self.c)
    #exit()




    q=K.concatenate(l,axis=-1)
    #print("q",q.shape)
    #exit()
    ret=K.reshape(q,(-1,self.gs*self.c,self.param))
    return ret
 
    
    exit() 



    return x

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[-1]==self.param
    assert input_shape[-2]==self.gs
    return tuple([input_shape[0],self.gs*self.c,self.param])    

  def get_config(self):
    mi={"ga":self.gs,"param":self.param,"c":self.c}
    th=super(gmultiply,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gmultiply(**config)













