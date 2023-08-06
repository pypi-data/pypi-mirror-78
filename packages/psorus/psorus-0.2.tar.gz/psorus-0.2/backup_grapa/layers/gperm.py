import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace



def perm_init(shape,dtype=None):
  #works only for 16x16
  data=np.zeros((16,16))

  data[0,0]=1
  data[1,2]=1
  data[2,1]=1
  data[3,5]=1
  data[4,4]=1
  data[5,3]=1
  data[6,9]=1
  data[7,8]=1
  data[8,6]=1
  data[9,7]=1
  data[10,12]=1
  data[11,13]=1
  data[12,11]=1
  data[13,14]=1
  data[14,15]=1
  data[15,10]=1
  
  return t.constant(data,dtype=dtype)

class gperm(Layer):#multiplies all elements with one orthogonal matrix
  def __init__(self,gs=20,param=40,**kwargs):
    self.gs=gs
    self.param=param
    super(gperm,self).__init__(input_shape=(gs,param))

  def build(self, input_shape):

    self.trafo=self.add_weight(name='orthogonal_trafo',#Matrix N
                               shape=(self.param,self.param),
                               initializer=perm_init,
                               trainable=False)



    self.built=True


  def call(self,x):
    x=x[0]

    x=K.reshape(x,(-1,self.gs,self.param))


    x=K.dot(x,self.trafo)
    
    return x


  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    if len(input_shape)==2 and self.gs==1:
      assert input_shape[1]==self.param
      return tuple([input_shape[0],self.gs,self.param])
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.gs,self.param])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param}
    th=super(gperm,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gperm(**config)













