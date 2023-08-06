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



class gpre5(Layer):#just like gpre2, but with flag at 0
  def __init__(self,gs=20,numericC=10000,**kwargs):
    self.gs=gs
    self.numericC=numericC

    super(gpre5,self).__init__(input_shape=(gs,4))#fixed dimension, since specialised layer

  def get_config(self):
    mi={"gs":self.gs,"numericC":self.numericC}
    th=super(gpre5,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gpre5(**config)
  
  def build(self, input_shape):

    self.built=True

  def call(self,x):
    # print("!",x.shape)

    E=K.reshape(x[:,:,0],(-1,self.gs,1))
    p1=K.reshape(x[:,:,1],(-1,self.gs,1))
    p2=K.reshape(x[:,:,2],(-1,self.gs,1))
    p3=K.reshape(x[:,:,3],(-1,self.gs,1))


    
    pt=K.sqrt(p1**2+p2**2)
    p=K.sqrt(pt**2+p3**2)
    iszero=p**2+E**2
    iszero=1-K.relu(1-self.numericC*iszero)+K.relu(-self.numericC*iszero)



    #return iszero

    eta=iszero*0.5*K.log(0.0000000001+(p+p3)/(p-p3+0.0000000001))
    #phi=iszero*t.math.acos(p3/(p+0.0000001))
    phi=iszero*t.math.atan2(p2,p1)

    #print("eta",eta.shape,"phi",phi.shape)


    eta=K.reshape(eta,(-1,self.gs))
    phi=K.reshape(phi,(-1,self.gs))


    meta=K.mean(eta,axis=-1)

    mp1=K.mean(p1,axis=-2)
    mp2=K.mean(p2,axis=-2)

    #print(p2.shape,p1.shape)
    #print(mp1.shape,mp2.shape)
    #exit()

    mphi=t.math.atan2(mp2,mp1)
    #print("meta",meta.shape,"mphi",mphi.shape)

    #mphi=K.mean(phi,axis=-1)

    #exit()


    meta=K.reshape(K.repeat_elements(meta,self.gs,0),(-1,self.gs))
    mphi=K.repeat_elements(mphi,self.gs,1)

    #print("meta",meta.shape,"mphi",mphi.shape)

    #deta=eta#-meta##not sure if abs here
    #dphi=phi#-mphi##not sure here either

    siszero=K.reshape(iszero,(-1,self.gs))

    deta=K.reshape(siszero*(eta-meta),(-1,self.gs,1))
    dphi=K.reshape(siszero*(phi-mphi),(-1,self.gs,1))

    pi=t.constant(math.pi)

    #dphi=K.min([t.math.floormod(dphi,2*pi),t.math.floormod(-dphi,2*pi)],axis=0)

    opta=t.math.floormod(dphi,2*pi)
    optb=t.math.floormod(-dphi,2*pi)

    dphi=t.where(t.greater(opta,optb),optb,-opta)



    #dphi=K.reshape(dphi,(-1,self.gs,1))#should actually be useless?
    
    #dphi=K.min(K.concatenate((t.math.floormod(dphi,2*pi),t.math.floormod(-dphi,2*pi)),axis=-1),axis=-1)

    #dphi=K.reshape(dphi,(-1,self.gs,1))


    #deta=iszero*K.permute_dimensions(K.permute_dimensions(eta,(1,0,2))-meta,(1,0,2))#not sure if abs here required
    #dphi=iszero*K.permute_dimensions(K.permute_dimensions(phi,(1,0,2))-mphi,(1,0,2))#also not sure here either


    spt=K.sum(pt,axis=-2)
    ppt=-iszero*K.permute_dimensions(K.log(0.000000001+K.permute_dimensions(pt,(1,0,2))/(spt+0.0000001)),(1,0,2))#please note the added sign in comparison to the original paper

    #print(iszero.shape,deta.shape,dphi.shape,ppt.shape)
    #print(eta.shape,meta.shape)
    #print(phi.shape,mphi.shape)
    #exit()

    #print(iszero.shape,deta.shape,dphi.shape,pt.shape)
    #exit()


    #meta=K.reshape(meta,(-1,self.gs,1))
    #mphi=K.reshape(mphi,(-1,self.gs,1))
    #phi=K.reshape(phi,(-1,self.gs,1))

    ret=K.concatenate((iszero,deta,dphi,ppt),axis=-1)#adding iszero for numerical reasons
   
    #print(ret.shape,x.shape)
    #exit() 

    return ret

    
  def compute_output_shape(self,input_shape):
    shape=list(input_shape)
    assert len(shape)==3
    assert shape[-1]==4
    assert shape[-2]==self.gs
    shape[-1]=4#?
    return tuple(shape)













