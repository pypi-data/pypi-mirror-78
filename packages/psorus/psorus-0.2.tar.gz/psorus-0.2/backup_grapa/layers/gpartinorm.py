import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





class gpartinorm(Layer):#takes in -1*gs*param, and returns a array in which for all i,j x[i,:,j] has std 1 (ignores atm that this is kinda stupid for flag)
  def __init__(self,gs=20,param=40,alpha=0.01,**kwargs):
    self.gs=gs
    self.param=param
    self.alpha=alpha#constant to remove numerical problems from std=0
    super(gpartinorm,self).__init__(input_shape=(gs,param))

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"alpha":self.alpha}
    th=super(gpartinorm,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gpartinorm(**config)

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]
    
    #-1,gs,param
    #print("x",x.shape)

    xp=K.permute_dimensions(x,(1,0,2))
    #gs,-1,param
    #print("xp",xp.shape)

    xpr=K.reshape(xp,(self.gs,-1))
    #gs,-1
    #print("xpr",xpr.shape)

    xm0=K.mean(xpr,axis=0)
    xpr-=xm0

    xm=K.mean(K.abs(xpr),axis=0)
    xpr-=xm
        
    xs=K.max(K.abs(xpr),axis=0)+self.alpha
    #-1
    #print("xs",xs.shape)

    xd=xpr/xs
    #gs,-1
    #print("xd",xd.shape)

    xdr=K.reshape(xd,(self.gs,-1,self.param))
    #gs,-1,param
    #print("xdr",xdr.shape)

    xf=K.permute_dimensions(xdr,(1,0,2))
    #-1,gs,param
    #print("xf",xf.shape)

    return xf

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.gs,self.param])    















