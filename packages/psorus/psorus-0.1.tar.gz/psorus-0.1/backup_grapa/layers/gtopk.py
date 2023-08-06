import numpy as np
import math
import sys

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

def phieta_init(shape,dtype=None):
  rel=np.zeros(shape)
  if len(rel)>=4:
    rel[4,0]=1.0
  if len(rel)>=5:
    rel[5,0]=1.0
  return K.constant(rel,dtype=dtype)


class gtopk(Layer):
  def __init__(self,gs=30,param=20,k=4,free=0,learnable=True,self_interaction=False,metrik_init=keras.initializers.TruncatedNormal(mean=0.0,stddev=0.05),self_interaction_const=100.0,numericalC=10000,emptyconst=100000000.0,flag=7,**kwargs):
    
    print("initilized a new gtopk with gs=",gs)
    self.gs=gs
    self.k=k
    self.param=param
    self.free=free
    self.learnable=learnable
    self.self_interaction=self_interaction
    self.self_interaction_const=self_interaction_const
    self.numericalC=numericalC
    self.metrik_init=metrik_init
    self.flag=flag
    self.emptyconst=emptyconst


    #print(kwargs)
    #print((gs,param))
    #exit()

    super(gtopk,self).__init__(input_shape=(gs,param))

  def get_config(self):
    mi={"gs":self.gs,"k":self.k,"param":self.param,"free":self.free,"self_interaction":self.self_interaction,"self_interaction_const":self.self_interaction_const,"numericalC":self.numericalC,"flag":self.flag,"emptyconst":self.emptyconst}
    th=super(gtopk,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gtopk(**config)
  
  def build(self, input_shape):

    self.metrik=self.add_weight(name="metrik_diag",
                                shape=(self.param,1),
                                initializer=self.metrik_init,#ignores metrik_init completely
                                trainable=self.learnable,
                                regularizer=None)

    self.built=True


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

  def call(self,x):
    x=x[0]

    #print("!x",x.shape)

    gs=self.gs
    k=self.k
    param=self.param
    C=self.numericalC

    #print("gs",gs,"k",k,"param",param,"C",C)


    for i in range(10):t.print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
 
    t.print("calling onetopk",self.metrik, output_stream=sys.stdout)


    #exit()

    mata=K.constant(self.getmata(gs))
    matb=K.constant(self.getmatb(gs))
   
    #print("mata",mata.shape)
    #print("matb",matb.shape) 
    
    xp=K.permute_dimensions(x,(0,2,1))
    #print("xp",xp.shape)

    xa=K.dot(xp,mata)
    xb=K.dot(xp,matb)
    #print("xa",xa.shape,"xb",xb.shape)
    #exit()    

    isval=xa[:,self.flag,:]*xb[:,self.flag,:]

    #return isval,isval
    #print("isval",isval.shape)
    #exit()


    ds=xa-xb
    #print("ds",ds.shape)

    dsp=K.permute_dimensions(ds,(0,2,1))
    #print("dsp",dsp.shape)
    
    dspsq=K.square(dsp)
    #print("dspsq",dspsq.shape)
    #print("self.metrik",self.metrik.shape)
    
    delt=K.dot(dspsq,self.metrik)
    #print("delt",delt.shape)


    delt=K.reshape(delt,(-1,self.gs*self.gs))+(1-isval)*self.emptyconst


    d=K.reshape(delt,(-1,gs,gs))
    #print("d",d.shape)


    #return d,d

    #####no self interactions
    if self.self_interaction==False:
      one=K.eye(gs)
      #print("one",one.shape)
      d+=self.self_interaction_const*one
    #####end no self interactions



    v,_=t.math.top_k(-d,k=k)
    #print("v",v.shape)
    #return v,v
 
    vb=v[:,:,-1]
    #print("vb",vb.shape)

    vbs=K.reshape(vb,(-1,gs,1))
    #print("vbs",vbs.shape)

    
    
    su=d+vbs#plus since top_k(-d)
    #print("su",su.shape)


    #map anything above 0 to 0 and anything below to 1, also map 0 to 1
    #p(-x)=C*d_C(-x)
    #     =d(-C*x)
    #     =1-r(Cx-1)+r(Cx)
    #experimentally:
    #   r(1-Cx)-r(-Cx)

    rel=K.relu(1-C*su)-K.relu(-C*su)
    #print("rel",rel.shape)

    rel=K.relu(rel)-K.relu(rel-1)


    #return rel,rel

    
    dez1=K.reshape(rel,(-1,self.gs*self.gs))
    #print("dez1",dez1.shape)
    dez2=dez1*isval
    #print("dez2",dez2.shape)
    rel=K.reshape(dez2,(-1,self.gs,self.gs))
    print("rel",rel.shape)

    numnei=K.sum(rel,axis=-1)
    print("numnei",numnei.shape)
    factor=self.k/(numnei+0.00000000001)
 
    #return K.concatenate((numnei,factor),axis=-1),factor#,factor#numnei,numnei

    print("factor",factor.shape)
    refactor=K.repeat(factor,self.gs)
    print("refactor",refactor.shape)


    refactor=K.permute_dimensions(refactor,(0,2,1))

    #return refactor,refactor

    rel=rel*refactor 
    print("rel",rel.shape)

    #exit()

    if self.free==0:return rel,x
    zero1=K.zeros_like(x[:,:,0])
    zero1=K.reshape(zero1,(-1,x.shape[1],1))
    #print("!",zero1.shape)
    zerolis=[]
    for i in range(self.free):
      zerolis.append(zero1)
    zeros=K.concatenate(zerolis,axis=-1)
    #print(zeros.shape)

    return rel,K.concatenate((x,zeros),axis=-1)



    



    
  def compute_output_shape(self,input_shape):
    shape=list(input_shape[0])
    #print("inputting",shape,"gs=",self.gs,"sp=",self.param)
    assert len(shape)==3
    assert shape[-1]==self.param
    assert shape[-2]==self.gs

    a1=tuple([shape[0],self.gs,self.gs])
    a2=tuple([shape[0],self.gs,self.param+self.free])

    return a1,a2













