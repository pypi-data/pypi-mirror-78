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



class gltknd(Layer):
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
  def __init__(self,gs=20,param=40,keepconst=10,iterations=1,alinearity=[-1.0,1.0],kernel_initializer='glorot_uniform',self_initializer=None,neig_initializer=None,learnable=True,**kwargs):
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
    self.keepconst=keepconst
    self.makezerolmat=K.constant(self.genmakezerolmat(gs))
    self.iterations=iterations
    self.activate=False
    if len(alinearity)==2:
      self.activate=True
      self.activation=alinearity#most general form of continous activation: const,x,const
    else:
      self.activation=[]
    self.learnable=learnable

    super(gltknd,self).__init__(**kwargs)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"keepconst":self.keepconst,"iterations":self.iterations,"alinearity":self.activation,"self_initializer":self.self_initializer,"neig_initializer":self.neig_initializer,"learnable":self.learnable}
    th=super(gltknd,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gltknd(**config)
  
  def build(self, input_shape):
    self.neigintact=self.add_weight(name='neigthbourinteraction',
                                shape=(self.param,self.param-self.keepconst,),
                                initializer=self.neig_initializer,
                                trainable=self.learnable)
    self.selfintact=self.add_weight(name='selfinteraction',
                                shape=(self.param,self.param-self.keepconst,),
                                initializer=self.self_initializer,
                                trainable=self.learnable)

    self.built=True

  def genmakezerolmat(self,n):
    ret=np.zeros((n,n))+1.0
    for i in range(n):
      ret[i,i]=0.0
    return ret

  def call(self,x):
    #print("!",x[0].shape,x[1].shape)
    mat=x[0]
    val=x[1]
    con=val[:,:,:self.keepconst]
    var=val[:,:,self.keepconst:]
    mat0=mat*self.makezerolmat
    
    tra=trace(mat)
    sumtra=K.sum(mat,axis=-1)
    msumtra=K.mean(sumtra,axis=-1)

    #print("tra",tra.shape)
    #print("sumtra",sumtra.shape)

    #exit()

    # print(mat0.shape,val.shape)
    # val=K.permute_dimensions(val,(1,0,2))
    # print(mat0.shape,val.shape)
    # mat0=K.permute_dimensions(mat0,(1,0,2))
    # val =K.permute_dimensions(val ,(1,2,0))
    # print(mat0.shape,val.shape)

    # weignei=K.dot(mat0,val)
    # weignei=K.dot(val,mat0)
    for i in range(self.iterations):
      weignei=K.batch_dot(mat0,val)
      
      # print("---",weignei.shape)
      # return K.sum(K.sum(weignei,axis=-1),axis=-1)
      # exit()
      
      # print(weignei.shape)
      
      
      parta=K.dot(weignei,self.neigintact)
      partb=K.dot(val,self.selfintact)
      # print(parta.shape,tra.shape)

      # print(parta.shape)
      
      # exit()
      var=parta+partb

      #var=K.permute_dimensions(var,(1,2,0))
      
      # return tra
      
      #var/=msumtra
      #var=K.permute_dimensions(var,(2,0,1))

      if self.activate:
        var=self.advrelu(var,self.activation)


      val=K.concatenate((con,var),axis=-1)

      # return K.sum(K.sum(val,axis=-1),axis=-1)
      # print("###",K.eval(val))
      
      
      # print(parta.shape,partb.shape,var.shape,val.shape)
    
    
    # exit()
    return val
    #return K.concatenate((mat,val),axis=-1)
    
    # print("call")
    # # print(x.shape)
    # m=((K.dot(K.pow(x,2),self.kernel)))
    # # print("!",m.shape)
    # E=((K.dot(x,K.constant(np.array([[1.0],[0.0],[0.0],[0.0]])))))
    # px=((K.dot(x,K.constant(np.array([[0.0],[1.0],[0.0],[0.0]])))))
    # py=((K.dot(x,K.constant(np.array([[0.0],[0.0],[1.0],[0.0]])))))
    # pt=K.sqrt(K.square(px)+K.square(py))


    
  def compute_output_shape(self,input_shape):
    # return tuple([input_shape[0],40,60])
    # return tuple([input_shape[0]])
    # return tuple(input_shape)
    pshape=list(input_shape[0])
    assert len(pshape)==3
    assert pshape[-1]==self.gs
    assert pshape[-2]==self.gs

    shape=list(input_shape[1])
    assert len(shape)==3
    assert shape[-1]==self.param
    assert shape[-2]==self.gs
    #shape[-1]=self.graphmax+self.graphvar#this layer should not chance the size of the network, so this line becomes kinda useless
    # shape[-2]=self.graphmax
    return tuple(shape)
    # return tuple([15,2])
    # return tuple(K.constant([1,1]).shape)
    
#    assert len(shape)==2
    # assert shape[-1]==4
    # shape[-1]=2
    # return tuple(shape)













