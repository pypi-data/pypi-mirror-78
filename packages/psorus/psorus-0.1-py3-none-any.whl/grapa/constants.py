import numpy as np
from tensorflow.keras import backend as K
import tensorflow.keras as keras
import tensorflow as t
import json




###definitions of classes that will be used to define a current Network State

class state:
  def __init__(self,gs=10,param=10):
    self.gs=gs
    self.param=param
  def __str__(self):
    return str(self.gs)+"*"+str(self.param)
  def __repr__(self):
    return str(self)
class grap:
  A=None
  X=None
  s=None
  def __init__(self,s):
    self.A=None
    self.X=None
    self.s=s
  def __str__(self):
    return str(self.s)+"("+str(self.A.shape)+"*"+str(self.X.shape)+")"
  def __repr__(self):
    return str(self)
class setting:

  def __init__(self,**kwargs):
    for key in kwargs:
      setattr(self,key,kwargs[key])
  def __str__(self):
    dic={}
    for key in dir(self):
      dic[key]=str(getattr(self,key))
    return json.dumps(dic,indent=2,sort_keys=True)#yes i litterally import json just for this

  def __repr__(self):
    return str(self)





###global attributes that probably will never be chanced

flag=0
self_interaction=True

cut=0.5
c_const=1000.0


###function to create the direct setting object  
def getm():
  m=setting()
  m.usei=False
  m.decompress="classic"

  m.trivial_ladder_n=1
  m.trivial_decompress_activation="linear"
  m.trivial_decompress_init_kernel=t.keras.initializers.TruncatedNormal()
  m.trivial_decompress_init_bias=t.keras.initializers.TruncatedNormal()

  m.sortindex=-1
  m.prenorm=False

  m.graph_init_self=t.keras.initializers.TruncatedNormal()
  m.graph_init_neig=t.keras.initializers.TruncatedNormal()
  m.agraph_init_self=m.graph_init_self
  m.agraph_init_neig=m.graph_init_neig

  m.edges=3#particle net like
  m.edgeactivation="relu"
  m.edgeactivationfinal=m.edgeactivation
  m.edgeusebias=False
  m.edgeconcat=False

  m.gq_activation="relu"
  m.gq_init_kernel=t.keras.initializers.TruncatedNormal()
  m.gq_init_bias=t.keras.initializers.Zeros()
  m.gq_usebias=False
  m.gq_batchnorm=False

  m.shallcomplex=not True
  m.complexsteps=3 

  m.gqa_activation=m.gq_activation
  m.gqa_init_kernel=m.gq_init_kernel
  m.gqa_init_bias=m.gq_init_bias
  m.gqa_usebias=m.gq_usebias
  m.gqa_batchnorm=m.gq_batchnorm

  m.shallacomplex=m.shallcomplex
  m.complexasteps=m.complexsteps

  m.shallredense=False
  m.redenseladder=[8,6]
  m.redenseactivation="relu"
  m.redenseinit=tf.keras.initializers.Identity()

  m.compression_init=tf.keras.initializers.Identity()

  m.mdense_activation="relu"
  m.mdense_init_kernel=tf.keras.initializers.Identity()
  m.mdense_init_bias=tf.keras.initializers.Zeros()
  m.mdense_usebias=True
  m.mdense_batchnorm=False



  return m













