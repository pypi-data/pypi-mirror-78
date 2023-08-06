import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace
from grapa.layers.kron import kronecker_product as kron
from grapa.layers.kron import kronecker_product_b1 as kron_b1
from grapa.layers.kron import kronecker_product_b1fx1 as kron_b1fx1
from grapa.layers.kron import kronecker_product_b2 as kron_b2




#batch_size=100
#epochs=1000
#verbose=2
#lr=0.001



class gliam(Layer):#not anymore using keepconst, also not setting the diagonal to zero
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
  def __init__(self,gs=20,param=40,a=10,iterations=1,alinearity=[-1.0,1.0],kernel_initializer='glorot_uniform',self_initializer=None,neig_initializer=None,learnable=True,**kwargs):
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
    self.a=a
    self.iterations=iterations
    self.activate=False
    if len(alinearity)==2:
      self.activate=True
      self.activation=alinearity
    else:
      self.activation=[]
    self.learnable=learnable

    super(gliam,self).__init__(**kwargs)

  
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

  def call(self,x):
    mat=x[0]#Matrix A
    val=x[1]

    eye=K.eye(self.gs)
 
    p1=kron(eye,self.selfintact)
    p2=kron_b1fx1(mat,self.neigintact)

    p=p1+p2


 

    v=K.reshape(val,(-1,self.gs*self.param))
    p=K.reshape(p,(-1,self.gs*self.param,self.gs*self.param))


    p=t.linalg.inv(p)#invert the matrix p, is only truly the inverse of glm if activate=False

    #print("p",p.shape,"v",v.shape)
    #exit()
    #does not yet work, how to define products with 2 batch dimensions
    #a bit inelegant if you ask me   

    for i in range(self.iterations):
      v=K.batch_dot(p,v)
      if self.activate:
        v=self.advrelu(v,self.activation)
    #print("v",v.shape,"a",self.a,"gs",self.gs,"param",self.param)
    #exit()
 
    ret=K.reshape(v,(-1,self.a,self.gs,self.param))#keine Ahnung ob richtig rum #doch scheint zu passen

    return ret




    #    v=K.reshape(val,(-1,self.a,self.gs*self.param))
    #    #p=K.reshape(p,(-1,self.gs*self.param,self.gs*self.param))
    #
    #    #print("p",p.shape,"v",v.shape)
    #    #exit()
    #    #does not yet work, how to define products with 2 batch dimensions
    #    #a bit inelegant if you ask me   
    #
    #    vs=[]
    #    for j in range(self.a):
    #      av=v[:,j,:]
    #      ap=p[:,j,:,:]
    #      for i in range(self.iterations):
    #        av=K.batch_dot(ap,av)
    #        if self.activate:
    #          av=self.advrelu(av,self.activation)
    #      av=K.reshape(av,(-1,1,self.gs*self.param))
    #      vs.append(av)
    #    v=K.concatenate(vs,axis=1)
    #    #print("v",v.shape,"a",self.a,"gs",self.gs,"param",self.param)
    #    #exit()
    # 
    #    ret=K.reshape(v,(-1,self.a,self.gs,self.param))#keine Ahnung ob richtig rum #doch scheint zu passen
    #
    #    return ret






    
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==4
    assert pshape[-1]==self.gs
    assert pshape[-2]==self.gs
    assert pshape[-3]==self.a

    shape=list(input_shape[1])
    assert len(shape)==4
    assert shape[-1]==self.param
    assert shape[-2]==self.gs
    assert shape[-3]==self.a

    return tuple(shape)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"a":self.a,"iterations":self.iterations,"alinearity":self.activation,"self_initializer":self.self_initializer,"neig_initializer":self.neig_initializer,"learnable":self.learnable}
    th=super(gliam,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gliam(**config)










