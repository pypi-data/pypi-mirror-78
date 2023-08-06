#NOTWORKINGYET
import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





#batch_size=100
#epochs=1000
#verbose=2
#lr=0.001



class gaddzeros(Layer):
  def __init__(self,inn=20,out=30,param=40,**kwargs):
    assert out>=inn
    self.inn=inn
    self.out=out
    self.param=param
    super(gaddzeros,self).__init__(**kwargs)

  def get_config(self):
    mi={"inn":self.inn,"out":self.out,"param":self.param}
    th=super(gaddzeros,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gaddzeros(**config)
  
  def build(self, input_shape):

    self.built=True

  def call(self,x):
    x=x[0]
    if self.inn==self.out:
      return x
    #print("x",x.shape)
    zero1=K.zeros_like(x[:,0,:])
    #print("zero1",zero1.shape)
    zero1=K.reshape(zero1,(-1,1,x.shape[2]))
    #print("zero1",zero1.shape)
    zerolis=[]
    for i in range(self.out-self.inn):
      zerolis.append(zero1)
    zeros=K.concatenate(zerolis,axis=-2)
    #print("zeros",zeros.shape)
    #print(zeros.shape)

    #exit()

    return K.concatenate((x,zeros),axis=-2)
   

 
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==3
    assert pshape[-1]==self.param
    assert pshape[-2]==self.inn
    pshape[-2]=self.out
    return tuple(pshape)













