import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense, Activation
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace




def metrik_init(shape,dtype=None):
  rel=np.zeros(shape)
  if len(rel)>=4:
    rel[4,4]=1.0
  if len(rel)>=5:
    rel[5,5]=1.0
  return K.constant(rel,dtype=dtype)


class glbuilder(Layer):
  def __init__(self,gs=30,param=40,free=0,metrik_initializer=metrik_init,**kwargs):#param:old parameternumber, free: new parameters initialised to 0
    self.gs=gs
    self.param=param
    self.free=free
    self.metrik_initializer=metrik_initializer
    super(glbuilder,self).__init__(input_shape=(gs,param))
  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"free":self.free}
    th=super(glbuilder,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return glbuilder(**config)
  def getmetrik(self):
    ret=np.zeros((self.param*2,self.param*2))
    ret[4,4]=ret[5,5]=1.0
    return ret  
  def fromdistsq(self,dsq):
    return K.exp(-dsq)

  def getmata(self,n):
    ret=np.zeros((n,n*n))
    for i in range(n*n):
      ret[int(math.floor(i/n)),i]=1
    return ret
  def getmatb(self,n):
    ret=np.zeros((n,n*n))
    for i in range(n*n):
      ret[i % n,i]=1
    return ret





  def build(self, input_shape):

    self.metrik=self.add_weight(name='metrik',
                                shape=(self.param,self.param),
                                initializer=self.metrik_initializer,
                                trainable=True)



    self.built=True


  def call(self,x):
    #print(x.shape)

    xt=K.permute_dimensions(x,(0,2,1))


    ca=K.constant(self.getmata(self.gs))
    cb=K.constant(self.getmatb(self.gs))



    #print(ca.shape,cb.shape)

    ma=K.dot(xt,ca)
    mb=K.dot(xt,cb)

    #print(ma.shape,mb.shape)

    ds=ma-mb#?,20,900
    dst=K.permute_dimensions(ds,(0,2,1))#?,900,20
    dsm=K.dot(dst,self.metrik)#?,900,20
    dsa=K.batch_dot(dsm,ds)


    #print(ds.shape,dst.shape,dsm.shape,dsa.shape)

    dsl=t.linalg.diag_part(dsa)

    dsq=K.reshape(dsl,(-1,self.gs,self.gs))


    #print(dsl.shape,dsq.shape)

    #exit()



    #dd4=t.linalg.diag_part(d4)

    #dd4=d4[:,:,1]


    #dsq=K.reshape(dd4,(-1,d,d))

    #print(delta.shape,deltat.shape,metrik.shape,deltatm.shape,d4.shape,dd4.shape,dsq.shape)


    #exit()



    basegraph=self.fromdistsq(dsq)
    
    #print(metrik.shape,xm.shape,xt.shape,dsq.shape)
    #print(basegraph.shape)
    
    parax=x[:,:,:self.param]
    #print(parax.shape)
    
    if self.free==0:return K.concatenate((basegraph,parax),axis=-1) 
    zero1=K.zeros_like(x[:,:,0])
    zero1=K.reshape(zero1,(-1,x.shape[1],1))
    #print("!",zero1.shape)
    zerolis=[]
    for i in range(self.free):
      zerolis.append(zero1)
    zeros=K.concatenate(zerolis,axis=-1)
    #print(zeros.shape)
    
    return K.concatenate((basegraph,parax,zeros),axis=-1)

    
  def compute_output_shape(self,input_shape):
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    return tuple([input_shape[0],self.gs,self.gs+self.param+self.free])    















