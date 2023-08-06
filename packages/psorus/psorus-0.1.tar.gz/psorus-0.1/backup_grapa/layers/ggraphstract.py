import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace

from tensorflow.python.ops import array_ops
#from
#https://github.com/tensorflow/tensorflow/blob/r1.8/tensorflow/contrib/kfac/python/ops/utils.py

def kron(mat1, mat2):
  """Computes the Kronecker product two matrices."""
  m1, n1 = mat1.get_shape().as_list()
  mat1_rsh = array_ops.reshape(mat1, [m1, 1, n1, 1])
  m2, n2 = mat2.get_shape().as_list()
  mat2_rsh = array_ops.reshape(mat2, [1, m2, 1, n2])
  return array_ops.reshape(mat1_rsh * mat2_rsh, [m1 * m2, n1 * n2])
def kron_b1(mat1, mat2):
  """Computes the Kronecker product two matrices, assuming batchdim(mat1)=1."""
  m1, n1 = mat1.get_shape().as_list()[1:]
  mat1_rsh = array_ops.reshape(mat1, [-1,m1, 1, n1, 1])
  m2, n2 = mat2.get_shape().as_list()
  mat2_rsh = array_ops.reshape(mat2, [1, m2, 1, n2])
  return array_ops.reshape(mat1_rsh * mat2_rsh, [-1,m1 * m2, n1 * n2])
def kron_b2(mat1, mat2):
  """Computes the Kronecker product two matrices, assuming batchdim(mat2)=1."""
  m1, n1 = mat1.get_shape().as_list()
  mat1_rsh = array_ops.reshape(mat1, [m1, 1, n1, 1])
  m2, n2 = mat2.get_shape().as_list()[1:]
  mat2_rsh = array_ops.reshape(mat2, [-1,1, m2, 1, n2])
  return array_ops.reshape(mat1_rsh * mat2_rsh, [-1,m1 * m2, n1 * n2])
def kron_bb(mat1, mat2):
  """Computes the Kronecker product two matrices, assuming batchdim(mat1/2)=1."""
  m1, n1 = mat1.get_shape().as_list()[1:]
  mat1_rsh = array_ops.reshape(mat1, [-1, m1, 1, n1, 1])
  m2, n2 = mat2.get_shape().as_list()[1:]
  mat2_rsh = array_ops.reshape(mat2, [-1, 1, m2, 1, n2])
  return array_ops.reshape(mat1_rsh * mat2_rsh, [-1,m1 * m2, n1 * n2])
def kron_b1fx1(mat1, mat2):
  """Computes the Kronecker product two matrices, assuming batchdim(mat1)=1."""
  f1, m1, n1 = mat1.get_shape().as_list()[1:]
  mat1_rsh = array_ops.reshape(mat1, [-1,f1,m1, 1, n1, 1])
  m2, n2 = mat2.get_shape().as_list()
  mat2_rsh = array_ops.reshape(mat2, [1, m2, 1, n2])
  return array_ops.reshape(mat1_rsh * mat2_rsh, [-1,f1,m1 * m2, n1 * n2])



#batch_size=100
#epochs=1000
#verbose=2
#lr=0.001



class ggraphstract(Layer):
  def __init__(self,in1=20,in2=30,**kwargs):
    self.in1=in1
    self.in2=in2
    super(ggraphstract,self).__init__(**kwargs)

  def get_config(self):
    mi={"in1":self.in1,"in2":self.in2}
    th=super(ggraphstract,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return ggraphstract(**config)
  
  def build(self, input_shape):

    self.built=True

  def call(self,x):
    i1=x[0]
    i2=x[1]

    l1=len(i1.shape)
    l2=len(i2.shape)
    


    if l1==3:
      if l2==3:
        return kron_bb(i1,i2)
      else:
        return kron_b1(i1,i2)
    else:
      if l2==3:
        return kron_b2(i1,i2)
      else:
        return kron(i1,i2)


    return kron(i1,i2)

    
    
     

 
  def compute_output_shape(self,input_shape):
    shape1=list(input_shape[0])
    shape2=list(input_shape[1])
    assert len(shape1)==2 or len(shape1)==3
    assert len(shape2)==2 or len(shape2)==3
    assert shape1[-1]==self.in1
    assert shape1[-2]==self.in1
    assert shape2[-1]==self.in2
    assert shape2[-2]==self.in2
    if len(shape1)+len(shape2)==4:
      return tuple([self.in1*self.in2,self.in1*self.in2])
    else:
      return tuple([-1,self.in1*self.in2,self.in1*self.in2])













