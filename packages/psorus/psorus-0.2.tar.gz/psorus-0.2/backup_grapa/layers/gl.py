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



class gl(Layer):
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
  def __init__(self,graphmax=20,graphvar=40,keepconst=10,iterations=1,alinearity=[-1.0,1.0],kernel_initializer='glorot_uniform',**kwargs):
    self.kernel_initializer=kernel_initializer
    self.graphmax=graphmax
    self.graphvar=graphvar
    self.keepconst=keepconst
    self.makezerolmat=K.constant(self.genmakezerolmat(graphmax))
    self.iterations=iterations
    self.activate=False
    if len(alinearity)==2:
      self.activate=True
      self.activation=alinearity#most general form of continous activation: const,x,const
    else:
      self.activation=[]

    super(gl,self).__init__(input_shape=(graphmax,graphmax+graphvar))

  def get_config(self):
    mi={"graphmax":self.graphmax,"graphvar":self.graphvar,"keepconst":self.keepconst,"iterations":self.iterations,"alinearity":self.activation,"kernel_initializer":self.kernel_initializer}
    th=super(gl,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gl(**config)
  
  def build(self, input_shape):
    self.neigintact=self.add_weight(name='neigthbourinteraction',
                                shape=(self.graphvar,self.graphvar-self.keepconst,),
                                initializer=self.kernel_initializer,
                                trainable=True)
    self.selfintact=self.add_weight(name='selfinteraction',
                                shape=(self.graphvar,self.graphvar-self.keepconst,),
                                initializer=self.kernel_initializer,
                                trainable=True)

    self.built=True

  def genmakezerolmat(self,n):
    ret=np.zeros((n,n))+1.0
    for i in range(n):
      ret[i,i]=0.0
    return ret

  def call(self,x):
    # print("!",x.shape)
    mat=x[:,:,:self.graphmax]
    val=x[:,:,self.graphmax:]
    con=val[:,:,:self.keepconst]
    var=val[:,:,self.keepconst:]
    mat0=mat*self.makezerolmat
    
    tra=trace(mat)
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

      var=K.permute_dimensions(var,(1,2,0))
      
      # return tra
      
      var/=tra
      var=K.permute_dimensions(var,(2,0,1))


      if self.activate:
        val=self.advrelu(val,self.activation)


      val=K.concatenate((con,var),axis=-1)

      # return K.sum(K.sum(val,axis=-1),axis=-1)
      # print("###",K.eval(val))
      
      
      # print(parta.shape,partb.shape,var.shape,val.shape)
    
    
    # exit()
    return K.concatenate((mat,val),axis=-1)
    
    # print("call")
    # # print(x.shape)
    # m=((K.dot(K.pow(x,2),self.kernel)))
    # # print("!",m.shape)
    # E=((K.dot(x,K.constant(np.array([[1.0],[0.0],[0.0],[0.0]])))))
    # px=((K.dot(x,K.constant(np.array([[0.0],[1.0],[0.0],[0.0]])))))
    # py=((K.dot(x,K.constant(np.array([[0.0],[0.0],[1.0],[0.0]])))))
    # pt=K.sqrt(K.square(px)+K.square(py))

    return x#K.constant([1,1])#K.concatenate((m,pt),axis=-1)#still missing: matrix*E+ matrix*abstand(vektor, ich)

    
  def compute_output_shape(self,input_shape):
    # return tuple([input_shape[0],40,60])
    # return tuple([input_shape[0]])
    # return tuple(input_shape)
    shape=list(input_shape)
    assert len(shape)==3
    assert shape[-1]==self.graphmax+self.graphvar
    assert shape[-2]==self.graphmax
    #shape[-1]=self.graphmax+self.graphvar#this layer should not chance the size of the network, so this line becomes kinda useless
    # shape[-2]=self.graphmax
    return tuple(shape)
    # return tuple([15,2])
    # return tuple(K.constant([1,1]).shape)
    
#    assert len(shape)==2
    # assert shape[-1]==4
    # shape[-1]=2
    # return tuple(shape)













