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



class glom(Layer):#not anymore using keepconst, also not setting the diagonal to zero
  def advrelu(self,x,q):
    i1=(type(q[0])==type(""))
    i2=(type(q[1])==type(""))
    if i1:
      if i2:
        return x
      else:
        return q[1]-K.relu(q[1]-x)
    else:
      if i2:
        return K.relu(x-q[0])+q[0]
      else:
        return K.relu(x-q[0])-K.relu(x-q[1])+q[0]
      
  #high number of iterations fail..why?
  def __init__(self,gs=20,param=40,iterations=1,alinearity=[-1.0,1.0],kernel_initializer='glorot_uniform',self_initializer=None,neig_initializer=None,learnable=True,**kwargs):
    if self_initializer==None:
      self.self_initializer=kernel_initializer
    else:
      self.self_initializer=self_initializer
    if neig_initializer==None:
      self.neig_initializer=kernel_initializer
    else:
      self.neig_initializer=neig_initializer

    self.gs=gs
    self.param=param
    self.iterations=iterations
    self.activate=False
    if len(alinearity)==2:
      self.activate=True
      self.activation=alinearity
    else:
      self.activation=[]
    self.learnable=learnable

    super(glom,self).__init__(**kwargs)

  
  def build(self, input_shape):
    self.neigintact=self.add_weight(name='neigthbourinteraction',#Matrix N
                                shape=(self.param,self.param),
                                initializer=self.neig_initializer,
                                trainable=self.learnable)
    self.selfintact=self.add_weight(name='selfinteraction',#Matrix S
                                shape=(self.param,self.param),
                                initializer=self.self_initializer,
                                trainable=self.learnable)

    self.built=True



  def tp(A,B):
    #A has shape (param,param), B has shape (?,gs,gs), should return (?,gs,gs,param,param)
    return K.zeros((1,self.gs,self.gs,self.param,self.param))#does not do what is intended
    
    





  def call(self,x):
    mat=x[0]#Matrix A
    val=x[1]
   
    N=self.neigintact
    S=self.selfintact
    
    print("N",N.shape)
    print("S",S.shape)
    
    
    t1=self.tp(S,K.eye(self.gs))

    print("t1",t1.shape)



    exit()

 
    for i in range(self.iterations):
      weignei=K.batch_dot(mat,val)#Neighbours of the current nodes
      
      parta=K.dot(weignei,self.neigintact)#Neighbour part
      partb=K.dot(val,self.selfintact)#Self Interaction Part
      val=parta+partb

      if self.activate:
        val=self.advrelu(val,self.activation)

    return val


    
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==3
    assert pshape[-1]==self.gs
    assert pshape[-2]==self.gs

    shape=list(input_shape[1])
    assert len(shape)==3
    assert shape[-1]==self.param
    assert shape[-2]==self.gs

    return tuple(shape)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"iterations":self.iterations,"alinearity":self.activation,"self_initializer":self.self_initializer,"neig_initializer":self.neig_initializer,"learnable":self.learnable}
    th=super(glom,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return glom(**config)










