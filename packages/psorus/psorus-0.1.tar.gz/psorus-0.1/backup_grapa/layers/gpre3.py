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



class gpre3(Layer):#just like gpre2, but with flag at 0
  def __init__(self,gs=20,numericC=10000,**kwargs):
    self.gs=gs
    self.numericC=numericC

    super(gpre3,self).__init__(input_shape=(gs,4))#fixed dimension, since specialised layer

  def get_config(self):
    mi={"gs":self.gs,"numericC":self.numericC}
    th=super(gpre3,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gpre3(**config)
  
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

    meta=K.mean(eta,axis=-2)
    mphi=K.mean(phi,axis=-2)

    #print("meta",meta.shape,"mphi",mphi.shape)

    #deta=eta#-meta##not sure if abs here
    #dphi=phi#-mphi##not sure here either


    deta=iszero*K.permute_dimensions(K.permute_dimensions(eta,(1,0,2))-meta,(1,0,2))#not sure if abs here required
    dphi=iszero*K.permute_dimensions(K.permute_dimensions(phi,(1,0,2))-mphi,(1,0,2))#also not sure here either

    #print("deta",deta.shape,"dphi",dphi.shape)

    lpt=iszero*K.log(pt+0.0000001)##
    lE=iszero*K.log(E+0.0000001)##
    
    #print("lpt",lpt.shape,"lE",lE.shape)

    #rpt=K.reshape(pt,(-1,self.gs))

    spt=K.sum(pt,axis=-2)
    #print("spt",spt.shape)
   

    #return K.permute_dimensions(K.log(1.0+K.abs(K.permute_dimensions(pt,(1,0,2))/(K.abs(spt)+1.0))),(1,0,2)) 
    #ispt=1/(spt+0.000000001)
    #print("ispt",ispt.shape)

    ppt=-iszero*K.permute_dimensions(K.log(0.000000001+K.permute_dimensions(pt,(1,0,2))/(spt+0.0000001)),(1,0,2))#please note the added sign in comparison to the original paper
    #ppt=K.reshape(K.permute_dimensions(K.log(0.000000001+K.permute_dimensions(rpt,(1,0,2))/(spt+0.0000001)),(1,0)),(-1,self.gs,1))##
    #ppt=K.reshape(K.permute_dimensions(K.log(0.000000001+K.permute_dimensions(rpt,(1,0))/(spt+0.0000001)),(1,0)),(-1,self.gs,1))##
    #ppt=K.reshape(K.log(0.000000001+K.permute_dimensions(rpt,(1,0))/(spt+0.0000001)),(-1,self.gs,1))##
    #ppt=iszero*K.log(pt/(spt+0.00000001))##
    #print("ppt",ppt.shape)

    sE=K.sum(E,axis=-2)
    #print("sE",sE.shape)
    
    pE=-iszero*K.permute_dimensions(K.log(0.000000001+K.permute_dimensions(E,(1,0,2))/(sE+0.0000001)),(1,0,2))#here was also a sign added
    #pE=-iszero*K.log(sE/(E+0.00000001))##
    #pE=-iszero
    #print("pE",pE.shape)

    dR=K.sqrt(deta**2+dphi**2)##
    #print("dR",dR.shape)

    ret=K.concatenate((iszero,deta,dphi,lpt,lE,ppt,pE,dR),axis=-1)#adding iszero for numerical reasons
   
    #print(ret.shape,x.shape)
    #exit() 

    return ret

    
  def compute_output_shape(self,input_shape):
    shape=list(input_shape)
    assert len(shape)==3
    assert shape[-1]==4
    assert shape[-2]==self.gs
    shape[-1]=8#?
    return tuple(shape)













