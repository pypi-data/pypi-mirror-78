import numpy as np
import math

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense,Activation
from tensorflow.keras.layers import BatchNormalization as BatchNorm
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam,SGD
from tensorflow.linalg import trace





#batch_size=100
#epochs=1000
#verbose=2
#lr=0.001



class glmlp(Layer):
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
  def __init__(self,gs=20,param=40,keepconst=10,iterations=1,alinearity=[-1.0,1.0],initializer='glorot_uniform',i1=30,i2=20,mlpact=K.relu,momentum=0.99,k=16,**kwargs):
    self.initializer=initializer
    self.gs=gs
    self.param=param
    self.keepconst=keepconst
    self.iterations=iterations
    self.activate=False
    self.i1=i1
    self.i2=i2
    self.mlpact=mlpact
    self.momentum=momentum
    self.k=k

    self.batch1=BatchNorm(input_shape=(self.gs*self.gs,i1),trainable=True,momentum=momentum)
    self.batch2=BatchNorm(input_shape=(self.gs*self.gs,i2),trainable=True,momentum=momentum)
    self.batch3=BatchNorm(input_shape=(self.gs*self.gs,self.param-self.keepconst),trainable=True,momentum=momentum)


    if len(alinearity)==2:
      self.activate=True
      self.activation=alinearity#most general form of continous activation: const,x,const
    else:
      self.activation=[]

    super(glmlp,self).__init__(**kwargs)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"keepconst":self.keepconst,"iterations":self.iterations,"alinearity":self.activation,"initializer":self.initializer,"i1":self.i1,"i2":self.i2,"mlpact":self.mlpact,"momentum":self.momentum,"k":self.k}
    th=super(glmlp,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return glmlp(**config)

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



  def mlp(self,q):#does the mlp, should always be build, so that q can be arbitrary dimensional, als long as q.shape[-1]=2*gs, and return.shape=q.shape, with the exception of return.shape[-1]=gs-keepconst,this cannot be (easily) reached thanks to the batch layers
    s1=K.dot(q,self.M1)+self.B1
    s1=self.batch1(s1)
    s1=self.mlpact(s1)
    s2=K.dot(s1,self.M2)+self.B2
    s2=self.batch2(s2)
    s2=self.mlpact(s2)
    s3=K.dot(s2,self.M3)+self.B3
    s3=self.batch3(s3)
    s3=self.mlpact(s3)
    return s3
  
  def build(self, input_shape):
    self.M1=self.add_weight(name='M1',
                                shape=(2*self.param,self.i1,),
                                initializer=self.initializer,
                                trainable=True)
    self.M2=self.add_weight(name='M2',
                                shape=(self.i1,self.i2,),
                                initializer=self.initializer,
                                trainable=True)
    self.M3=self.add_weight(name='M3',
                                shape=(self.i2,self.param-self.keepconst,),
                                initializer=self.initializer,
                                trainable=True)
    self.B1=self.add_weight(name='B1',
                                shape=(self.i1,),
                                initializer=self.initializer,
                                trainable=True)
    self.B2=self.add_weight(name='B2',
                                shape=(self.i2,),
                                initializer=self.initializer,
                                trainable=True)
    self.B3=self.add_weight(name='B3',
                                shape=(self.param-self.keepconst,),
                                initializer=self.initializer,
                                trainable=True)
    
    self.built=True


  def call(self,x):
    #print("!",x[0].shape,x[1].shape)
    mat=x[0]
    val=x[1]
    con=val[:,:,:self.keepconst]
    var=val[:,:,self.keepconst:]
    

    mata=K.constant(self.getmata(self.gs))
    matb=K.constant(self.getmatb(self.gs))

    for i in range(self.iterations):

      #print("val",val.shape)

      valp=K.permute_dimensions(val,(0,2,1))
      
      #print("valp",valp.shape)

      vA=K.dot(valp,mata)
      vB=K.dot(valp,matb)

      #print("vA",vA.shape,"vB",vB.shape)

      feat=K.permute_dimensions(vA,(0,2,1))
      diff=K.permute_dimensions(vB-vA,(0,2,1))
      
      #print("feat",feat.shape,"diff",diff.shape)

      premlp=K.concatenate((feat,diff),axis=-1)

      #print("premlp",premlp.shape)

      postmlp=self.mlp(premlp)
      
      #print("postmlp",postmlp.shape)

      ppmlp=K.permute_dimensions(postmlp,(0,2,1))

      #print("ppmlp",ppmlp.shape)
      
      res=K.reshape(ppmlp,(-1,self.param-self.keepconst,self.gs,self.gs))

      #print("res",res.shape)
      #print("mat",mat.shape)

      resp=K.permute_dimensions(res,(1,0,2,3)) 


      presmat=resp*mat#kinda wondering that this(resp*mat) actually works...tja it actually does not

      #print("presmat",presmat.shape)

      resmat=K.permute_dimensions(presmat,(1,0,2,3))

      #print("resmat",resmat.shape)

      #exit()


      summ=K.sum(resmat,axis=-1)#/msumtra

      #print("summ",summ.shape)


      #print("summ",summ.shape)

      #print("pre",summ.shape)
      summ/=self.k
      #print("post",summ.shape)

      #exit()
     

      #print("permuted from",summ.shape) 
      
      #var=K.permute_dimensions(summ,(2,0,1))
      var=K.permute_dimensions(summ,(0,2,1))

      #print("permuted to",var.shape)


      #print("var",var.shape)
      #print("con",con.shape)



      if self.activate:
        var=self.advrelu(var,self.activation)


      val=K.concatenate((con,var),axis=-1)

      #print("concatting",con.shape,var.shape,"=>",val.shape)
      #print("val",val.shape)       

      continue

      exit()


      weignei=K.batch_dot(mat,val)
      
      var=K.dot(weignei,self.intact)

      var=K.permute_dimensions(var,(1,2,0))
      
      # return tra
      
      var/=msumtra
      var=K.permute_dimensions(var,(2,0,1))

      if self.activate:
        var=self.advrelu(var,self.activation)


      val=K.concatenate((con,var),axis=-1)


      # return K.sum(K.sum(val,axis=-1),axis=-1)
      # print("###",K.eval(val))
      
      
      # print(parta.shape,partb.shape,var.shape,val.shape)
    
    
    # exit()

    #print("returning",val.shape)
    #exit()
 
    return val
    #return K.concatenate((mat,val),axis=-1)
    
    # print("call")
    # # print(x.shape)
    # m=((K.dot(K.pow(x,2),self.kernel)))
    # # print("!",m.shape)
    # E=((K.dot(x,K.constant(np.array([[1.0],[0.0],[0.0],[0.0]])))))
    # px=((K.dot(x,K.constant(np.array([[0.0],[1.0],[0.0],[0.0]])))))
    # py=((K.dot(x,K.constant(np.array([[0.0],[0.0],[1.0],[0.0]])))))
    # pt=K.sqrt(K.square(px)+K.square(py))


    
  def compute_output_shape(self,input_shape):
    # return tuple([input_shape[0],40,60])
    # return tuple([input_shape[0]])
    # return tuple(input_shape)
    pshape=list(input_shape[0])
    assert len(pshape)==3
    assert pshape[-1]==self.gs
    assert pshape[-2]==self.gs

    shape=list(input_shape[1])
    assert len(shape)==3
    assert shape[-1]==self.param
    assert shape[-2]==self.gs
    #shape[-1]=self.graphmax+self.graphvar#this layer should not chance the size of the network, so this line becomes kinda useless
    # shape[-2]=self.graphmax
    return tuple(shape)
    # return tuple([15,2])
    # return tuple(K.constant([1,1]).shape)
    
#    assert len(shape)==2
    # assert shape[-1]==4
    # shape[-1]=2
    # return tuple(shape)













