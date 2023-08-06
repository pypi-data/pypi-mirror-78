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



class gpre1(Layer):
  def __init__(self,gs=20,numericC=10000,**kwargs):
    self.gs=gs
    self.numericC=numericC

    super(gpre1,self).__init__(input_shape=(gs,4))#fixed dimension, since specialised layer

  def get_config(self):
    mi={"gs":self.gs,"numericC":self.numericC}
    th=super(gpre1,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gpre1(**config)
  
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
    eta=iszero*0.5*K.log(0.0000000001+(p+p3)/(p-p3+0.0000000001))
    #phi=iszero*t.math.acos(p3/(p+0.0000001))
    phi=iszero*t.math.atan2(p2,p1)
    m=K.sqrt(K.relu(E**2-p**2))

    ret= K.concatenate((E,p1,p2,p3,eta,phi,m,pt,p,iszero),axis=-1)
    

    return ret

    
  def compute_output_shape(self,input_shape):
    shape=list(input_shape)
    assert len(shape)==3
    assert shape[-1]==4
    assert shape[-2]==self.gs
    shape[-1]=10#?
    return tuple(shape)













