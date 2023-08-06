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
from tensorflow.keras.layers import Layer,Dense,Activation
from tensorflow.keras.layers import BatchNormalization as BatchNorm
import sys
def R(self,x,c_const=1000.0,cut=0.5):
  return K.relu(c_const*(x-cut)+1)-K.relu(c_const*(x-c_const))
def doand(x,mode="prod",c_const=1000.0,cut=0.5):
  if mode=="and":
    ret=R(K.prod(x,axis=-1),c_const=c_const,cut=cut)
  if mode=="prod":
    ret=K.prod(x,axis=-1)
  if mode=="or":
    ret=R(K.sum(x,axis=-1),c_const=c_const,cut=cut)
  if mode=="sum":
    ret=K.sum(x,axis=-1)
  return ret
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
  return array_ops.reshape(mat1_rsh * mat2_rsh, [-1,m1 * m2, n1 * n2])
def kron_b2(mat1, mat2):
  """Computes the Kronecker product two matrices, assuming batchdim(mat2)=1."""
  m2, n2 = mat2.get_shape().as_list()[1:]
  mat2_rsh = array_ops.reshape(mat2, [-1,1, m2, 1, n2])
def kron_bb(mat1, mat2):
  """Computes the Kronecker product two matrices, assuming batchdim(mat1/2)=1."""
  mat1_rsh = array_ops.reshape(mat1, [-1, m1, 1, n1, 1])
  mat2_rsh = array_ops.reshape(mat2, [-1, 1, m2, 1, n2])
def kron_b1fx1(mat1, mat2):
  f1, m1, n1 = mat1.get_shape().as_list()[1:]
  mat1_rsh = array_ops.reshape(mat1, [-1,f1,m1, 1, n1, 1])
  return array_ops.reshape(mat1_rsh * mat2_rsh, [-1,f1,m1 * m2, n1 * n2])
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
def metrik_init(shape,dtype=None):
  rel=np.zeros(shape)
  if len(rel)>=4:
    rel[4,4]=1.0
  if len(rel)>=5:
    rel[5,5]=1.0
  return K.constant(rel,dtype=dtype)
def phieta_init(shape,dtype=None):
    rel[4,0]=1.0
    rel[5,0]=1.0

class gpre4(Layer):#just like gpre2, but with flag at 0
  def __init__(self,gs=20,numericC=10000,**kwargs):
    self.gs=gs
    self.numericC=numericC

    super(gpre4,self).__init__(input_shape=(gs,4))#fixed dimension, since specialised layer

  def get_config(self):
    mi={"gs":self.gs,"numericC":self.numericC}
    th=super(gpre4,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gpre4(**config)
  
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


    ret=K.concatenate((iszero,deta,dphi),axis=-1)#adding iszero for numerical reasons
   
    #print(ret.shape,x.shape)
    #exit() 

    return ret

    
  def compute_output_shape(self,input_shape):
    shape=list(input_shape)
    assert len(shape)==3
    assert shape[-1]==4
    assert shape[-2]==self.gs
    shape[-1]=3#?
    return tuple(shape)


















class gcomextractdiag(Layer):#shall take a 5d layer (?,gs,gs,c,c) and take out the diagonal part in gs,gs, resulting in (?,gs,c,c) 
  def __init__(self,gs=20,c=2,**kwargs):
    self.gs=gs
    self.c=c
    super(gcomextractdiag,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                           shape=(self.param,self.c*self.c),
    #                           initializer=self.initializer,
    #                           trainable=self.trainable)


    self.built=True


  def call(self,x):
    x=x[0]#params

    parts=[]
    for i in range(self.gs):
      ac=x[:,i,i,:self.c,:self.c]
      ac=K.reshape(ac,(-1,1,self.c,self.c))
      parts.append(ac)
  
    ret=K.concatenate(parts,axis=1)
    
    return ret


    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==5
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.gs
    assert g_shape[3]==self.c
    assert g_shape[4]==self.c
    return tuple([g_shape[0],self.gs,self.c,self.c])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c}
    th=super(gcomextractdiag,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomextractdiag(**config)


















class gaddzeros(Layer):
  def __init__(self,inn=20,out=30,param=40,**kwargs):
    assert out>=inn
    self.inn=inn
    self.out=out
    self.param=param
    super(gaddzeros,self).__init__(**kwargs)

  def get_config(self):
    mi={"inn":self.inn,"out":self.out,"param":self.param}
    th=super(gaddzeros,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gaddzeros(**config)
  
  def build(self, input_shape):

    self.built=True

  def call(self,x):
    x=x[0]
    if self.inn==self.out:
      return x
    #print("x",x.shape)
    zero1=K.zeros_like(x[:,0,:])
    #print("zero1",zero1.shape)
    zero1=K.reshape(zero1,(-1,1,x.shape[2]))
    #print("zero1",zero1.shape)
    zerolis=[]
    for i in range(self.out-self.inn):
      zerolis.append(zero1)
    zeros=K.concatenate(zerolis,axis=-2)
    #print("zeros",zeros.shape)
    #print(zeros.shape)

    #exit()

    return K.concatenate((x,zeros),axis=-2)
   

 
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==3
    assert pshape[-1]==self.param
    assert pshape[-2]==self.inn
    pshape[-2]=self.out
    return tuple(pshape)


















class gkeepmatcut(Layer):
  def __init__(self,gs=30,param=40,dimension=0,**kwargs):
    self.gs=gs
    self.param=param
    self.dimension=dimension
    super(gkeepmatcut,self).__init__(input_shape=(gs,gs*(dimension+1)+param))


  def build(self, input_shape):

    self.built=True


  def call(self,x):
    
    return x[:,:self.gs,:self.gs]

    
  def compute_output_shape(self,input_shape):
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.gs*(self.dimension+1)+self.param
    return tuple([input_shape[0],self.gs,self.gs])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"dimension":self.dimension}
    th=super(gkeepmatcut,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gkeepmatcut(**config)


















class gcomfullyconnected(Layer):#shall take a 3d parameter layer (?,gs,param) and output a fully connected graph of type (?,gs,gs) 
  def __init__(self,gs=20,param=30,**kwargs):
    #c=2
    #mode="min"
    assert gs>0 and param>0
    self.gs=gs
    self.param=param
    super(gcomfullyconnected,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                           shape=(self.param,self.c*self.c),
    #                           initializer=self.initializer,
    #                           trainable=self.trainable)


    self.built=True


  def call(self,x):
    x=x[0]#params  (?,gs,param)
     
    s=x[:,0,0]
    s=K.reshape(s,(-1,1,1))
    s*=0.0
    s+=1.0

    ret=[]
    for i in range(self.gs):
      toa=[]
      for j in range(self.gs):
         toa.append(s)
      ret.append(K.concatenate(toa,axis=1))
    ret=K.concatenate(ret,axis=2)

    return ret 




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==3
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.param
    return tuple([g_shape[0],self.gs,self.gs])

  def get_config(self):
    mi={"gs":self.gs,"param":self.param}
    th=super(gcomfullyconnected,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomfullyconnected(**config)


















class gliam(Layer):#not anymore using keepconst, also not setting the diagonal to zero
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
  def __init__(self,gs=20,param=40,a=10,iterations=1,alinearity=[-1.0,1.0],kernel_initializer='glorot_uniform',self_initializer=None,neig_initializer=None,learnable=True,**kwargs):
    if self_initializer==None:
      self.self_initializer=kernel_initializer
    else:
      self.self_initializer=self_initializer
    if neig_initializer==None:
      self.neig_initializer=kernel_initializer
    else:
      self.neig_initializer=neig_initializer

    self.gs=gs
    self.param=param
    self.a=a
    self.iterations=iterations
    self.activate=False
    if len(alinearity)==2:
      self.activate=True
      self.activation=alinearity
    else:
      self.activation=[]
    self.learnable=learnable

    super(gliam,self).__init__(**kwargs)

  
  def build(self, input_shape):
    self.neigintact=self.add_weight(name='neigthbourinteraction',#Matrix N
                                shape=(self.param,self.param),
                                initializer=self.neig_initializer,
                                trainable=self.learnable)
    self.selfintact=self.add_weight(name='selfinteraction',#Matrix S
                                shape=(self.param,self.param),
                                initializer=self.self_initializer,
                                trainable=self.learnable)

    self.built=True

  def call(self,x):
    mat=x[0]#Matrix A
    val=x[1]

    eye=K.eye(self.gs)
 
    p1=kron(eye,self.selfintact)
    p2=kron_b1fx1(mat,self.neigintact)

    p=p1+p2


 

    v=K.reshape(val,(-1,self.gs*self.param))
    p=K.reshape(p,(-1,self.gs*self.param,self.gs*self.param))


    p=t.linalg.inv(p)#invert the matrix p, is only truly the inverse of glm if activate=False

    #print("p",p.shape,"v",v.shape)
    #exit()
    #does not yet work, how to define products with 2 batch dimensions
    #a bit inelegant if you ask me   

    for i in range(self.iterations):
      v=K.batch_dot(p,v)
      if self.activate:
        v=self.advrelu(v,self.activation)
    #print("v",v.shape,"a",self.a,"gs",self.gs,"param",self.param)
    #exit()
 
    ret=K.reshape(v,(-1,self.a,self.gs,self.param))#keine Ahnung ob richtig rum #doch scheint zu passen

    return ret




    #    v=K.reshape(val,(-1,self.a,self.gs*self.param))
    #    #p=K.reshape(p,(-1,self.gs*self.param,self.gs*self.param))
    #
    #    #print("p",p.shape,"v",v.shape)
    #    #exit()
    #    #does not yet work, how to define products with 2 batch dimensions
    #    #a bit inelegant if you ask me   
    #
    #    vs=[]
    #    for j in range(self.a):
    #      av=v[:,j,:]
    #      ap=p[:,j,:,:]
    #      for i in range(self.iterations):
    #        av=K.batch_dot(ap,av)
    #        if self.activate:
    #          av=self.advrelu(av,self.activation)
    #      av=K.reshape(av,(-1,1,self.gs*self.param))
    #      vs.append(av)
    #    v=K.concatenate(vs,axis=1)
    #    #print("v",v.shape,"a",self.a,"gs",self.gs,"param",self.param)
    #    #exit()
    # 
    #    ret=K.reshape(v,(-1,self.a,self.gs,self.param))#keine Ahnung ob richtig rum #doch scheint zu passen
    #
    #    return ret






    
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==4
    assert pshape[-1]==self.gs
    assert pshape[-2]==self.gs
    assert pshape[-3]==self.a

    shape=list(input_shape[1])
    assert len(shape)==4
    assert shape[-1]==self.param
    assert shape[-2]==self.gs
    assert shape[-3]==self.a

    return tuple(shape)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"a":self.a,"iterations":self.iterations,"alinearity":self.activation,"self_initializer":self.self_initializer,"neig_initializer":self.neig_initializer,"learnable":self.learnable}
    th=super(gliam,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gliam(**config)















class gsym(Layer):
  def __init__(self,gs=20,**kwargs):
    self.gs=gs
    super(gsym,self).__init__(**kwargs)

  def get_config(self):
    mi={"gs":self.gs}
    th=super(gsym,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gsym(**config)
  
  def build(self, input_shape):

    self.built=True

  def call(self,x):
    x=x[0]
    xp=K.permute_dimensions(x,(0,2,1))
    
    s=x+xp
    s=K.relu(5*s)-K.relu(5*s-1)    
    
    return s
   

 
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==3
    assert pshape[-1]==self.gs
    assert pshape[-2]==self.gs
    return tuple(pshape)


















class glam(Layer):#not anymore using keepconst, also not setting the diagonal to zero
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
  def __init__(self,gs=20,param=40,a=10,iterations=1,alinearity=[-1.0,1.0],kernel_initializer='glorot_uniform',self_initializer=None,neig_initializer=None,learnable=True,**kwargs):
    if self_initializer==None:
      self.self_initializer=kernel_initializer
    else:
      self.self_initializer=self_initializer
    if neig_initializer==None:
      self.neig_initializer=kernel_initializer
    else:
      self.neig_initializer=neig_initializer

    self.gs=gs
    self.param=param
    self.a=a
    self.iterations=iterations
    self.activate=False
    if len(alinearity)==2:
      self.activate=True
      self.activation=alinearity
    else:
      self.activation=[]
    self.learnable=learnable

    super(glam,self).__init__(**kwargs)

  
  def build(self, input_shape):
    self.neigintact=self.add_weight(name='neigthbourinteraction',#Matrix N
                                shape=(self.param,self.param),
                                initializer=self.neig_initializer,
                                trainable=self.learnable)
    self.selfintact=self.add_weight(name='selfinteraction',#Matrix S
                                shape=(self.param,self.param),
                                initializer=self.self_initializer,
                                trainable=self.learnable)

    self.built=True

  def call(self,x):
    mat=x[0]#Matrix A
    val=x[1]

    eye=K.eye(self.gs)
 
    p1=kron(eye,self.selfintact)
    p2=kron_b1fx1(mat,self.neigintact)

    p=p1+p2


 

    v=K.reshape(val,(-1,self.gs*self.param))
    p=K.reshape(p,(-1,self.gs*self.param,self.gs*self.param))

    #print("p",p.shape,"v",v.shape)
    #exit()
    #does not yet work, how to define products with 2 batch dimensions
    #a bit inelegant if you ask me   

    for i in range(self.iterations):
      v=K.batch_dot(p,v)
      if self.activate:
        v=self.advrelu(v,self.activation)
    #print("v",v.shape,"a",self.a,"gs",self.gs,"param",self.param)
    #exit()
 
    ret=K.reshape(v,(-1,self.a,self.gs,self.param))#keine Ahnung ob richtig rum #doch scheint zu passen

    return ret




    #    v=K.reshape(val,(-1,self.a,self.gs*self.param))
    #    #p=K.reshape(p,(-1,self.gs*self.param,self.gs*self.param))
    #
    #    #print("p",p.shape,"v",v.shape)
    #    #exit()
    #    #does not yet work, how to define products with 2 batch dimensions
    #    #a bit inelegant if you ask me   
    #
    #    vs=[]
    #    for j in range(self.a):
    #      av=v[:,j,:]
    #      ap=p[:,j,:,:]
    #      for i in range(self.iterations):
    #        av=K.batch_dot(ap,av)
    #        if self.activate:
    #          av=self.advrelu(av,self.activation)
    #      av=K.reshape(av,(-1,1,self.gs*self.param))
    #      vs.append(av)
    #    v=K.concatenate(vs,axis=1)
    #    #print("v",v.shape,"a",self.a,"gs",self.gs,"param",self.param)
    #    #exit()
    # 
    #    ret=K.reshape(v,(-1,self.a,self.gs,self.param))#keine Ahnung ob richtig rum #doch scheint zu passen
    #
    #    return ret






    
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==4
    assert pshape[-1]==self.gs
    assert pshape[-2]==self.gs
    assert pshape[-3]==self.a

    shape=list(input_shape[1])
    assert len(shape)==4
    assert shape[-1]==self.param
    assert shape[-2]==self.gs
    assert shape[-3]==self.a

    return tuple(shape)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"a":self.a,"iterations":self.iterations,"alinearity":self.activation,"self_initializer":self.self_initializer,"neig_initializer":self.neig_initializer,"learnable":self.learnable}
    th=super(glam,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return glam(**config)















class gbuilder(Layer):
  def __init__(self,gs=30,param=10,free=30,**kwargs):
    self.gs=gs
    self.param=param
    self.free=free
    super(gbuilder,self).__init__(input_shape=(gs,param+param))

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"free":self.free}
    th=super(gbuilder,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gbuilder(**config)


  def getmetrik(self):
    ret=np.zeros((self.param*2,self.param*2))
    ret[4,4]=ret[5,5]=1.0
    return ret  
  def fromdistsq(self,dsq):
    return K.exp(-dsq)

  def build(self, input_shape):

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
    #print(x.shape)
    metrik=K.constant(self.getmetrik())
    xt=K.permute_dimensions(x,(0,2,1))
    
    
    ca=K.constant(self.getmata(self.gs))
    cb=K.constant(self.getmatb(self.gs))



    #print(ca.shape,cb.shape)
  
    ma=K.dot(xt,ca)
    mb=K.dot(xt,cb)

    #print(ma.shape,mb.shape)

    ds=ma-mb#?,20,900
    dst=K.permute_dimensions(ds,(0,2,1))#?,900,20
    dsm=K.dot(dst,metrik)#?,900,20
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
    
    parax=x[:,:,self.param:]#please note, that this layer is build to read two times the same data: first the one for the distance generation, and afterwards the one for node data, also note, that glbuilder does not do this, but instead works on the same dataset
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
    
    return K.concatenate((basegraph,parax,zeros))

    
  def compute_output_shape(self,input_shape):
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    return tuple([input_shape[0],self.gs,self.gs+self.param+self.free])    




















class gcomgraphand(Layer):#is capable of running "and" operations on (?,gs,gs,c,c,n=2) graphs, resulting in (?,gs,gs,c,c) 
  def __init__(self,gs=20,c=2,n=2,mode="prod",cut=0.5,c_const=1000.0,**kwargs):
    self.gs=gs
    self.c=c
    self.n=n
    self.mode=mode
    self.cut=cut
    self.c_const=c_const
    super(gcomgraphand,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                           shape=(self.param,self.c*self.c),
    #                           initializer=self.initializer,
    #                           trainable=self.trainable)


    self.built=True

  def call(self,x):
    x=x[0]

    ret=doand(x,mode=self.mode,c_const=self.c_const,cut=self.cut)

    return ret 
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==6
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.gs
    assert g_shape[3]==self.c
    assert g_shape[4]==self.c
    assert g_shape[5]==self.n
    return tuple([g_shape[0],self.gs,self.gs,self.c,self.c])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c,"n":self.n,"mode":self.mode,"cut":self.cut,"c_const":self.c_const}
    th=super(gcomgraphand,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomgraphand(**config)


















class gcomdensediverge(Layer):#shall take a 3d layer (?,gs,param) and output a 4d layer (?,gs,c,paramo)
  def __init__(self,gs=20,param=30,paramo=40,c=2,initializer="glorot_uniform",trainable=True,**kwargs):
    #c=2
    #mode="min"
    self.gs=gs
    self.param=param
    self.paramo=paramo
    self.c=c
    self.initializer=initializer
    self.trainable=trainable
    super(gcomdensediverge,self).__init__(**kwargs)

  def build(self, input_shape):

    self.trafo=self.add_weight(name="trafo",
                               shape=(self.param,self.paramo*self.c),
                               initializer=self.initializer,
                               trainable=self.trainable)


    self.built=True


  def call(self,x):
    x=x[0]#params

    #shall take a 3d feature vector of shape (-1,gs,param), and transform it using trafo into (-1,gs,c,paramo)

    #print("x",x.shape)

    #xi=K.reshape(x,(-1,self.gs,self.ags*self.param))
    #print("xi",xi.shape)

    xt=K.dot(x,self.trafo)
    #print("xt",xt.shape)

    xp=K.reshape(xt,(-1,self.gs,self.c,self.paramo))
    
    #print("xp",xp.shape)

    #exit()

    return xp

    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==3
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.param
    return tuple([g_shape[0],self.gs,self.c,self.paramo])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c,"param":self.param,"paramo":self.paramo,"initializer":self.initializer,"trainable":self.trainable}
    th=super(gcomdensediverge,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomdensediverge(**config)


















class gremoveparam(Layer):
  def __init__(self,gs=50,inn=30,out=20,**kwargs):
    assert inn>=out
    self.gs=gs
    self.inn=inn
    self.out=out
    super(gremoveparam,self).__init__(**kwargs)


  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]
    return x[:,:self.gs,:self.out] 
 

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[-1]==self.inn
    assert input_shape[-2]==self.gs
    return tuple([input_shape[0],self.gs,self.out])    

  def get_config(self):
    mi={"inn":self.inn,"gs":self.gs,"out":self.out}
    th=super(gremoveparam,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gremoveparam(**config)


















class gcomgraphand2(Layer):#is capable of running "and" operations on two (?,c*gs,c*gs) graphs, resulting in (?,c*gs,c*gs) 
  def __init__(self,gs=20,c=2,mode="prod",cut=0.5,c_const=1000.0,**kwargs):
    self.gs=gs
    self.c=c
    self.mode=mode
    self.cut=cut
    self.c_const=c_const
    super(gcomgraphand2,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                           shape=(self.param,self.c*self.c),
    #                           initializer=self.initializer,
    #                           trainable=self.trainable)


    self.built=True

  def call(self,q):
    y=q[1]
    x=q[0]

    x=K.reshape(x,(-1,self.gs*self.c,self.gs*self.c,1))
    y=K.reshape(y,(-1,self.gs*self.c,self.gs*self.c,1))

    q=K.concatenate((x,y),axis=-1)

    ret=doand(q,mode=self.mode,c_const=self.c_const,cut=self.cut)
    
    return ret

    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    g_shape2=input_shape[1]
    assert len(g_shape)==3
    assert g_shape[1]==self.gs*self.c
    assert g_shape[2]==self.gs*self.c
    assert g_shape2[1]==self.gs*self.c
    assert g_shape2[2]==self.gs*self.c
    return tuple([g_shape[0],self.gs*self.c,self.gs*self.c])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c,"mode":self.mode,"cut":self.cut,"c_const":self.c_const}
    th=super(gcomgraphand2,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomgraphand2(**config)


















class glom(Layer):#not anymore using keepconst, also not setting the diagonal to zero
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
  def __init__(self,gs=20,param=40,iterations=1,alinearity=[-1.0,1.0],kernel_initializer='glorot_uniform',self_initializer=None,neig_initializer=None,learnable=True,**kwargs):
    if self_initializer==None:
      self.self_initializer=kernel_initializer
    else:
      self.self_initializer=self_initializer
    if neig_initializer==None:
      self.neig_initializer=kernel_initializer
    else:
      self.neig_initializer=neig_initializer

    self.gs=gs
    self.param=param
    self.iterations=iterations
    self.activate=False
    if len(alinearity)==2:
      self.activate=True
      self.activation=alinearity
    else:
      self.activation=[]
    self.learnable=learnable

    super(glom,self).__init__(**kwargs)

  
  def build(self, input_shape):
    self.neigintact=self.add_weight(name='neigthbourinteraction',#Matrix N
                                shape=(self.param,self.param),
                                initializer=self.neig_initializer,
                                trainable=self.learnable)
    self.selfintact=self.add_weight(name='selfinteraction',#Matrix S
                                shape=(self.param,self.param),
                                initializer=self.self_initializer,
                                trainable=self.learnable)

    self.built=True



  def tp(A,B):
    #A has shape (param,param), B has shape (?,gs,gs), should return (?,gs,gs,param,param)
    return K.zeros((1,self.gs,self.gs,self.param,self.param))#does not do what is intended
    
    





  def call(self,x):
    mat=x[0]#Matrix A
    val=x[1]
   
    N=self.neigintact
    S=self.selfintact
    
    print("N",N.shape)
    print("S",S.shape)
    
    
    t1=self.tp(S,K.eye(self.gs))

    print("t1",t1.shape)



    exit()

 
    for i in range(self.iterations):
      weignei=K.batch_dot(mat,val)#Neighbours of the current nodes
      
      parta=K.dot(weignei,self.neigintact)#Neighbour part
      partb=K.dot(val,self.selfintact)#Self Interaction Part
      val=parta+partb

      if self.activate:
        val=self.advrelu(val,self.activation)

    return val


    
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==3
    assert pshape[-1]==self.gs
    assert pshape[-2]==self.gs

    shape=list(input_shape[1])
    assert len(shape)==3
    assert shape[-1]==self.param
    assert shape[-2]==self.gs

    return tuple(shape)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"iterations":self.iterations,"alinearity":self.activation,"self_initializer":self.self_initializer,"neig_initializer":self.neig_initializer,"learnable":self.learnable}
    th=super(glom,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return glom(**config)















class gcomgraphcutter(Layer):#takes a reordered gs*gs graph, and cuts it in pieces of c, which get pooled by a given rule
  def __init__(self,gs=20,c=2,mode="mean",cut=0.5,c_const=1000,**kwargs):
    #c=2
    #mode="min"
    assert gs % c==0#assume there is an equal splitting
    self.gs=gs
    self.c=c
    self.ogs=int(self.gs/self.c)
    self.mode=mode
    self.cut=cut
    self.c_const=c_const
    super(gcomgraphcutter,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                            shape=(self.param*self.c,self.paramo),
    #                            initializer=self.metrik_init,#ignores metrik_init completely
    #                            trainable=self.learnable,
    #                            regularizer=None)



    self.built=True


  def call(self,x):
    A=x[0]#adjacency matrix
 


    Ar=K.reshape(A,(-1,self.ogs,self.c,self.ogs,self.c))
    #print("Ar",Ar.shape)

    if self.mode=="mean":
      Am=K.mean(Ar,axis=(2,4))
    if self.mode=="min":
      Am=K.min(Ar,axis=(2,4))
    if self.mode=="max":
      Am=K.max(Ar,axis=(2,4))

    #print("Am",Am.shape)
    
    C=self.c_const
    cut=self.cut
    
    Ar=K.relu(1+C*(Am-cut))-K.relu(C*(Am-cut))
    

    #print("Ar",Ar.shape)


    #exit()


    return Ar



    exit()

    

    
  def compute_output_shape(self,input_shape):
    grap_shape=input_shape[0]
    assert len(grap_shape)==3
    assert grap_shape[1]==self.gs
    assert grap_shape[2]==self.gs
    return tuple([grap_shape[0],self.ogs,self.ogs])

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"c":self.c,"metrik_init":self.metrik_init,"learnable":self.learnable,"paramo":self.paramo,"mode":self.mode,"cut":self.cut,"c_const":self.c_const}
    th=super(gcomgraphcutter,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomgraphcutter(**config)


















class gltk(Layer):
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
  def __init__(self,gs=20,param=40,keepconst=10,iterations=10,alinearity=[-1.0,1.0],kernel_initializer='glorot_uniform',**kwargs):
    self.kernel_initializer=kernel_initializer
    self.gs=gs
    self.param=param
    self.keepconst=keepconst
    self.makezerolmat=K.constant(self.genmakezerolmat(gs))
    self.iterations=iterations
    self.activate=False
    if len(alinearity)==2:
      self.activate=True
      self.activation=alinearity#most general form of continous activation: const,x,const
    else:
      self.activation=[]

    super(gltk,self).__init__(**kwargs)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"keepconst":self.keepconst,"iterations":self.iterations,"alinearity":self.activation,"kernel_initializer":self.kernel_initializer}
    th=super(gltk,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gltk(**config)
  
  def build(self, input_shape):
    self.neigintact=self.add_weight(name='neigthbourinteraction',
                                shape=(self.param,self.param-self.keepconst,),
                                initializer=self.kernel_initializer,
                                trainable=True)
    self.selfintact=self.add_weight(name='selfinteraction',
                                shape=(self.param,self.param-self.keepconst,),
                                initializer=self.kernel_initializer,
                                trainable=True)

    self.built=True

  def genmakezerolmat(self,n):
    ret=np.zeros((n,n))+1.0
    for i in range(n):
      ret[i,i]=0.0
    return ret

  def call(self,x):
    #print("!",x[0].shape,x[1].shape)
    mat=x[0]
    val=x[1]
    con=val[:,:,:self.keepconst]
    var=val[:,:,self.keepconst:]
    mat0=mat*self.makezerolmat
    
    tra=trace(mat)
    sumtra=K.sum(mat,axis=-1)
    msumtra=K.mean(sumtra,axis=-1)

    #print("tra",tra.shape)
    #print("sumtra",sumtra.shape)

    #exit()

    # print(mat0.shape,val.shape)
    # val=K.permute_dimensions(val,(1,0,2))
    # print(mat0.shape,val.shape)
    # mat0=K.permute_dimensions(mat0,(1,0,2))
    # val =K.permute_dimensions(val ,(1,2,0))
    # print(mat0.shape,val.shape)

    # weignei=K.dot(mat0,val)
    # weignei=K.dot(val,mat0)
    for i in range(self.iterations):
      weignei=K.batch_dot(mat0,val)
      
      # print("---",weignei.shape)
      # return K.sum(K.sum(weignei,axis=-1),axis=-1)
      # exit()
      
      # print(weignei.shape)
      
      
      parta=K.dot(weignei,self.neigintact)
      partb=K.dot(val,self.selfintact)
      # print(parta.shape,tra.shape)

      # print(parta.shape)
      
      # exit()
      var=parta+partb

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


















class gfeat(Layer):
  def __init__(self,gs=20,param=40,**kwargs):
    self.gs=gs
    self.param=param
    super(gfeat,self).__init__(input_shape=(gs,param))

  def get_config(self):
    mi={"gs":self.gs,"param":self.param}
    th=super(gfeat,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gfeat(**config)

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    return x[:,:,self.gs:self.gs+self.param]
    

    
  def compute_output_shape(self,input_shape):
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.gs+self.param
    return tuple([input_shape[0],self.gs,self.param])    




















class gpoolgrowth(Layer):
  def __init__(self,inn=20,out=30,param=40,kernel_initializer="glorot_uniform",**kwargs):
    self.inn=inn
    self.out=out
    self.param=param
    self.kernel_initializer=kernel_initializer
    super(gpoolgrowth,self).__init__(**kwargs)

  def get_config(self):
    mi={"inn":self.inn,"out":self.out,"param":self.param}
    th=super(gpoolgrowth,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gpoolgrowth(**config)
  
  def build(self, input_shape):

    self.inc=self.add_weight(name='inc',
                                shape=(self.param,self.param*(self.out-self.inn)),
                                initializer=self.kernel_initializer,
                                trainable=True)
    self.built=True

  def call(self,x):
    s=x[0]
    add=x[1]

    
    fa=K.dot(s,self.inc)
    fr=K.reshape(fa,(-1,self.out-self.inn,self.param))
    r=K.conatenate((add,fr),axis=-2)
    
    return r
    
     

 
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    xshape=list(input_shape[1])
    assert len(pshape)==2
    assert len(xshape)==3
    assert pshape[-1]==self.param
    assert xshape[-1]==self.param
    assert xshape[-2]==self.inn
    ret=[pshape[0],self.out,self.out]
    return tuple(ret)


















class gltknd(Layer):
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
  def __init__(self,gs=20,param=40,keepconst=10,iterations=1,alinearity=[-1.0,1.0],kernel_initializer='glorot_uniform',self_initializer=None,neig_initializer=None,learnable=True,**kwargs):
    if self_initializer==None:
      self.self_initializer=kernel_initializer
    else:
      self.self_initializer=self_initializer
    if neig_initializer==None:
      self.neig_initializer=kernel_initializer
    else:
      self.neig_initializer=neig_initializer

    self.gs=gs
    self.param=param
    self.keepconst=keepconst
    self.makezerolmat=K.constant(self.genmakezerolmat(gs))
    self.iterations=iterations
    self.activate=False
    if len(alinearity)==2:
      self.activate=True
      self.activation=alinearity#most general form of continous activation: const,x,const
    else:
      self.activation=[]
    self.learnable=learnable

    super(gltknd,self).__init__(**kwargs)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"keepconst":self.keepconst,"iterations":self.iterations,"alinearity":self.activation,"self_initializer":self.self_initializer,"neig_initializer":self.neig_initializer,"learnable":self.learnable}
    th=super(gltknd,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gltknd(**config)
  
  def build(self, input_shape):
    self.neigintact=self.add_weight(name='neigthbourinteraction',
                                shape=(self.param,self.param-self.keepconst,),
                                initializer=self.neig_initializer,
                                trainable=self.learnable)
    self.selfintact=self.add_weight(name='selfinteraction',
                                shape=(self.param,self.param-self.keepconst,),
                                initializer=self.self_initializer,
                                trainable=self.learnable)

    self.built=True

  def genmakezerolmat(self,n):
    ret=np.zeros((n,n))+1.0
    for i in range(n):
      ret[i,i]=0.0
    return ret

  def call(self,x):
    #print("!",x[0].shape,x[1].shape)
    mat=x[0]
    val=x[1]
    con=val[:,:,:self.keepconst]
    var=val[:,:,self.keepconst:]
    mat0=mat*self.makezerolmat
    
    tra=trace(mat)
    sumtra=K.sum(mat,axis=-1)
    msumtra=K.mean(sumtra,axis=-1)

    #print("tra",tra.shape)
    #print("sumtra",sumtra.shape)

    #exit()

    # print(mat0.shape,val.shape)
    # val=K.permute_dimensions(val,(1,0,2))
    # print(mat0.shape,val.shape)
    # mat0=K.permute_dimensions(mat0,(1,0,2))
    # val =K.permute_dimensions(val ,(1,2,0))
    # print(mat0.shape,val.shape)

    # weignei=K.dot(mat0,val)
    # weignei=K.dot(val,mat0)
    for i in range(self.iterations):
      weignei=K.batch_dot(mat0,val)
      
      # print("---",weignei.shape)
      # return K.sum(K.sum(weignei,axis=-1),axis=-1)
      # exit()
      
      # print(weignei.shape)
      
      
      parta=K.dot(weignei,self.neigintact)
      partb=K.dot(val,self.selfintact)
      # print(parta.shape,tra.shape)

      # print(parta.shape)
      
      # exit()
      var=parta+partb

      #var=K.permute_dimensions(var,(1,2,0))
      
      # return tra
      
      #var/=msumtra
      #var=K.permute_dimensions(var,(2,0,1))

      if self.activate:
        var=self.advrelu(var,self.activation)


      val=K.concatenate((con,var),axis=-1)

      # return K.sum(K.sum(val,axis=-1),axis=-1)
      # print("###",K.eval(val))
      
      
      # print(parta.shape,partb.shape,var.shape,val.shape)
    
    
    # exit()
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


















class gpre2(Layer):
  def __init__(self,gs=20,numericC=10000,**kwargs):
    self.gs=gs
    self.numericC=numericC

    super(gpre2,self).__init__(input_shape=(gs,4))#fixed dimension, since specialised layer

  def get_config(self):
    mi={"gs":self.gs,"numericC":self.numericC}
    th=super(gpre2,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gpre2(**config)
  
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
    phi=iszero*t.math.atan2(p2,p1)
    #phi=iszero*t.math.acos(p3/(p+0.0000001))

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

    ret=K.concatenate((deta,dphi,lpt,lE,ppt,pE,dR,iszero),axis=-1)#adding iszero for numerical reasons
   
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


















class gaddbias(Layer):
  def __init__(self,gs=20,param=40,metrik_init="glorot_uniform",learnable=True,**kwargs):
    self.gs=gs
    self.param=param
    self.metrik_init=metrik_init
    self.learnable=learnable
    super(gaddbias,self).__init__(**kwargs)

  def build(self, input_shape):

    self.bias=self.add_weight(name="bias",
                                shape=(self.gs,self.param),
                                initializer=self.metrik_init,#ignores metrik_init completely
                                trainable=self.learnable,
                                regularizer=None)

#    self.metrik=self.add_weight(name="metrik",
#                                shape=(self.param,1),
#                                initializer=keras.initializers.ones(),#ignores metrik_init completely
#                                trainable=not self.learnable,
#                                regularizer=None)


    self.built=True


  def call(self,x):
    x=x[0]
 
    #print("x",x.shape)
    #print("bias",self.bias.shape)
 
    ret=K.bias_add(x=x,bias=self.bias)
    #print("ret",ret.shape) 

    return ret

    exit()

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.gs,self.param])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"metrik_init":self.metrik_init,"learnable":self.learnable}
    th=super(gaddbias,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gaddbias(**config)


















class gcomdex(Layer):#creates ordering by last param (returns indices)
  def __init__(self,gs=20,param=40,**kwargs):
    self.gs=gs
    self.param=param
    super(gcomdex,self).__init__(**kwargs)

  def build(self, input_shape):


    self.built=True


  def call(self,x):
    x=x[0]
 
    values=x[:,:,-1]#K.reshape(K.dot(x,self.metrik),(-1,self.gs))

    _,valueorder=t.math.top_k(values,k=self.gs)

    valueorder=K.cast(valueorder,"float32")

    return valueorder

    

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.gs])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param}
    th=super(gcomdex,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomdex(**config)


















class gtlbuilder(Layer):
  def __init__(self,gs=30,param=10,free=30,**kwargs):
    self.gs=gs
    self.param=param
    self.free=free
    super(gtlbuilder,self).__init__(input_shape=(gs,gs+gs+param))

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"free":self.free}
    th=super(gtlbuilder,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gtlbuilder(**config)


  def getmetrik(self):
    return [[1],[1]]
  def fromdistsq(self,dsq):
    return K.exp(-dsq)

  def build(self, input_shape):
    self.metrik=self.add_weight(name="weight",
                                shape=(2,1),
                                initializer=keras.initializers.Ones(),
                                trainable=True)
    self.built=True

  def call(self,x):
    #print(x.shape)
   
    gs=self.gs 
    mata=x[:,:gs,:gs]
    matb=x[:,:gs,gs:gs+gs]
    data=x[:,:gs,gs+gs:]

    mata=K.reshape(mata,(-1,gs,gs,1))
    matb=K.reshape(matb,(-1,gs,gs,1))
     
    mat=K.concatenate((mata,matb),axis=-1)
    metrik=self.metrik
    
    dsq=K.reshape(K.dot(mat,metrik),(-1,gs,gs))
    
    basegraph=self.fromdistsq(dsq)
    
    
     
    #print(metrik.shape,xm.shape,xt.shape,dsq.shape)
    #print(basegraph.shape)
    
    parax=x[:,:,self.gs+self.gs:]#please note, that this layer is build to read two times the same data: first the one for the distance generation, and afterwards the one for node data, also note, that glbuilder does not do this, but instead works on the same dataset
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
    
    return K.concatenate((basegraph,parax,zeros))

    
  def compute_output_shape(self,input_shape):
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.gs+self.gs+self.param
    return tuple([input_shape[0],self.gs,self.gs+self.param+self.free])    




















class gcomgraphcombinations(Layer):#shall take a 4d layer (?,gs,c,c) and output a corresponding combination assamble (?,gs,gs,c,c,2) (c,c of all combinations of gs) 
  def __init__(self,gs=20,c=2,**kwargs):
    self.gs=gs
    self.c=c
    super(gcomgraphcombinations,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                           shape=(self.param,self.c*self.c),
    #                           initializer=self.initializer,
    #                           trainable=self.trainable)


    self.built=True


  def call(self,x):
    x=x[0]#params

    parts=[]
    for i in range(self.gs):
      ac=x[:,i,:self.c,:self.c]
      ac=K.reshape(ac,(-1,1,1,self.c,self.c,1))
      parts.append(ac)

    ret=[]
    for x in range(self.gs):
      toc=[]
      for y in range(self.gs):
        ac=K.concatenate((parts[x],parts[y]),axis=-1)
        toc.append(ac)
      ret.append(K.concatenate(toc,axis=2))
    ret=K.concatenate(ret,axis=1)

    return ret
    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==4
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.c
    assert g_shape[3]==self.c
    return tuple([g_shape[0],self.gs,self.gs,self.c,self.c,2])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c}
    th=super(gcomgraphcombinations,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomgraphcombinations(**config)


















class gltrivmlp(Layer):
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
  def __init__(self,gs=20,param=40,keepconst=10,iterations=10,alinearity=[-1.0,1.0],initializer='glorot_uniform',i1=30,i2=20,mlpact=K.relu,momentum=0.99,k=16,**kwargs):
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



    if len(alinearity)==2:
      self.activate=True
      self.activation=alinearity#most general form of continous activation: const,x,const
    else:
      self.activation=[]

    super(gltrivmlp,self).__init__(**kwargs)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"keepconst":self.keepconst,"iterations":self.iterations,"alinearity":self.activation,"initializer":self.initializer,"i1":self.i1,"i2":self.i2,"mlpact":self.mlpact,"momentum":self.momentum,"k":self.k}
    th=super(gltrivmlp,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gltrivmlp(**config)

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

    #print("q",q.shape)
    #exit()

    return q[:,:,:self.param-self.keepconst]
    return K.dot(q,self.tmat)


  def build(self, input_shape):
    self.tmat=self.add_weight(name='tmat',
                                shape=(2*self.param,self.param-self.keepconst,),
                                initializer=self.initializer,
                                trainable=False)
    
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

      postmlp=premlp[:,:,:self.param-self.keepconst]
      #postmlp=self.mlp(premlp)
      
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
      #resmat=K.permute_dimensions(presmat,(1,2,0,3))

      print("resmat",resmat.shape)

      #exit()


      summ=K.sum(resmat,axis=-1)#/msumtra

      print("summ",summ.shape)


      #print("summ",summ.shape)

      #print("pre",summ.shape)
      summ/=self.k
      #print("post",summ.shape)

      #exit()
     

      #print("permuted from",summ.shape) 
      
      #var=K.permute_dimensions(summ,(2,0,1))

      var=K.permute_dimensions(summ,(0,2,1))#hopefully implemented this into the resmat permute, nope, not diffbar

      #print("permuted to",var.shape)


      print("var",var.shape)
      #print("con",con.shape)

      #exit()

      if self.activate:
        var=self.advrelu(var,self.activation)


      val=K.concatenate((con,var),axis=-1)

      #print("concatting",con.shape,var.shape,"=>",val.shape)
      #print("val",val.shape)       

      continue

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


















class gcomdiagraph(Layer):
  def __init__(self,gs=20,c=2,**kwargs):
    #c=2
    #mode="min"
    assert gs % c==0#assume there is an equal splitting
    self.gs=gs
    self.c=c
    self.ogs=int(self.gs/self.c)
    super(gcomdiagraph,self).__init__(**kwargs)

  def build(self, input_shape):




    self.built=True


  def call(self,x):
    A=x[0]#reordered matrix gs*gs

    #shall take A and take the ogs diagonal c*c matrices, and concat them   

    graphs=[]

    ogs=self.ogs
    c=self.c

    for i in range(ogs):
      start=i*c
      end=(i+1)*c
      amat=A[:,start:end,start:end]
      amat=K.reshape(amat,(-1,1,c,c))
      graphs.append(amat)
    

    ret=K.concatenate(graphs,axis=1)

    return ret


    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==3
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.gs
    return tuple([g_shape[0],self.ogs,self.c,self.c])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c}
    th=super(gcomdiagraph,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomdiagraph(**config)


















class gcomreopool(Layer):
  def __init__(self,gs=20,param=40,**kwargs):
    #c=2
    #mode="min"
    self.gs=gs
    self.param=param
    super(gcomreopool,self).__init__(**kwargs)

  def build(self, input_shape):



    self.built=True


  def call(self,x):
    A=x[0]#adjacency matrix
    x=x[1]#parameters
 
    #print("x",x.shape)
    #print("A",A.shape) 

    #print("trafo",self.trafo.shape)


    #currently just uses the last value as sorting param
    values=x[:,:,-1]#K.reshape(K.dot(x,self.metrik),(-1,self.gs))
    #print("values",values.shape)

    _,valueorder=t.math.top_k(values,k=self.gs)
    #print("valueorder",valueorder.shape)

    #valueorder=t.argsort(values,axis=-1)
    #print("valueorder",valueorder.shape)

    xg=t.gather(params=x,indices=valueorder,axis=1,batch_dims=1)
    #print("xg",xg.shape)

    #exit()

    #xs=K.reshape(xg,(-1,self.ogs,self.param*self.c))
    #print("xs",xs.shape)


    #traf=K.dot(xs,self.trafo)
    #print("traf",traf.shape)



    At1=t.gather(params=A,indices=valueorder,axis=1,batch_dims=1)
    At2=t.gather(params=At1,indices=valueorder,axis=2,batch_dims=1)

    return At2,xg



    exit()

    

    
  def compute_output_shape(self,input_shape):
    grap_shape=input_shape[0]
    input_shape=input_shape[1]
    assert len(input_shape)==3
    assert len(grap_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    assert grap_shape[1]==self.gs
    assert grap_shape[2]==self.gs
    return tuple([grap_shape[0],self.gs,self.gs]),tuple([input_shape[0],self.gs,self.param])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param}
    th=super(gcomreopool,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomreopool(**config)


















class gcomdepoollg(Layer):#produces just one nonconstant graph additionally to gcomdepool
  def __init__(self,gs=20,param=40,paramo=40,c=2,metrik_init="glorot_uniform",graph_init=keras.initializers.Identity(),learnable=True,**kwargs):
    self.gs=gs
    self.param=param
    self.metrik_init=metrik_init
    self.graph_init=graph_init
    self.c=c
    self.ogs=int(self.gs*self.c)
    self.learnable=learnable
    self.paramo=paramo
    super(gcomdepoollg,self).__init__(**kwargs)

  def build(self, input_shape):

    self.trafo=self.add_weight(name="trafo",
                                shape=(self.param,self.paramo*self.c),
                                initializer=self.metrik_init,
                                trainable=self.learnable,
                                regularizer=None)

    #self.graph=self.add_weight(name="graph",
    #                            shape=(self.c,self.c),
    #                            initializer=self.graph_init,
    #                            trainable=self.learnable,
    #                            regularizer=None)

    self.graphtraf=self.add_weight(name="graphtraf",
                                shape=(self.param*self.gs,self.c*self.c),
                                initializer=self.graph_init,
                                trainable=self.learnable,
                                regularizer=None)

    self.built=True


  def call(self,x):
    x=x[0]
 
    #print("x",x.shape)
    

    #print("trafo",self.trafo.shape)

    #print("trafo",self.trafo.shape)

    traf=K.dot(x,self.trafo)
    #print("traf",traf.shape)


    ret=K.reshape(traf,(-1,self.ogs,self.paramo))
    #print("ret",ret.shape)



    xf=K.reshape(x,(-1,self.gs*self.param))
    preg=K.dot(xf,self.graphtraf)
    #print("preg",preg.shape)
  
    grap=K.reshape(preg,(-1,self.c,self.c)) 
    #print("grap",grap.shape)




 
    return ret,grap

    #exit()

  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.ogs,self.paramo]),tuple([input_shape[0],self.c,self.c])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"c":self.c,"metrik_init":self.metrik_init,"graph_init":self.graph_init,"learnable":self.learnable,"paramo":self.paramo}
    th=super(gcomdepoollg,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomdepoollg(**config)


















class gcomgraphfrom2param(Layer):#shall take a 5d layer (?,gs,gs,param,n=2) and output a set of corresponding graphs of type (?,gs,gs,c,c) 
  def __init__(self,gs=20,param=30,c=2,n=2,initializer="glorot_uniform",trainable=True,**kwargs):
    #c=2
    #mode="min"
    self.gs=gs
    self.param=param
    self.c=c
    self.n=n
    self.initializer=initializer
    self.trainable=trainable
    super(gcomgraphfrom2param,self).__init__(**kwargs)

  def build(self, input_shape):

    self.trafo=self.add_weight(name="trafo",
                               shape=(self.param*self.n,self.c*self.c),
                               initializer=self.initializer,
                               trainable=self.trainable)


    self.built=True


  def call(self,x):
    x=x[0]#params

    #shall take a 5d feature vector of shape (-1,gs,gs,param,n=2), and transform it using trafo into (-1,gs,gs,c,c)

    #print("x",x.shape)

    #xi=K.reshape(x,(-1,self.gs,self.ags*self.param))
    #print("xi",xi.shape)

    xr=K.reshape(x,(-1,self.gs,self.gs,self.param*self.n))


    xt=K.dot(xr,self.trafo)
    #print("xt",xt.shape)

    A=K.reshape(xt,(-1,self.gs,self.gs,self.c,self.c))
    
    #print("xp",xp.shape)

    #exit()

    return A

    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==5
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.gs
    assert g_shape[3]==self.param
    assert g_shape[4]==self.n
    return tuple([g_shape[0],self.gs,self.gs,self.c,self.c])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c,"param":self.param,"initializer":self.initializer,"trainable":self.trainable,"n":self.n}
    th=super(gcomgraphfrom2param,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomgraphfrom2param(**config)


















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


















class glim(Layer):#not anymore using keepconst, also not setting the diagonal to zero
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
  def __init__(self,gs=20,param=40,iterations=1,alinearity=[-1.0,1.0],kernel_initializer='glorot_uniform',self_initializer=None,neig_initializer=None,learnable=True,**kwargs):
    if self_initializer==None:
      self.self_initializer=kernel_initializer
    else:
      self.self_initializer=self_initializer
    if neig_initializer==None:
      self.neig_initializer=kernel_initializer
    else:
      self.neig_initializer=neig_initializer

    self.gs=gs
    self.param=param
    self.iterations=iterations
    self.activate=False
    if len(alinearity)==2:
      self.activate=True
      self.activation=alinearity
    else:
      self.activation=[]
    self.learnable=learnable

    super(glim,self).__init__(**kwargs)

  
  def build(self, input_shape):
    self.neigintact=self.add_weight(name='neigthbourinteraction',#Matrix N
                                shape=(self.param,self.param),
                                initializer=self.neig_initializer,
                                trainable=self.learnable)
    self.selfintact=self.add_weight(name='selfinteraction',#Matrix S
                                shape=(self.param,self.param),
                                initializer=self.self_initializer,
                                trainable=self.learnable)

    self.built=True

  def call(self,x):
    mat=x[0]#Matrix A
    val=x[1]

    eye=K.eye(self.gs)
 
    p1=kron(eye,self.selfintact)
    p2=kron_b1(mat,self.neigintact)
    p=p1+p2

    p=t.linalg.inv(p)#invert the matrix p, is only truly the inverse of glm if activate=False

      
    v=K.reshape(val,(-1,self.gs*self.param))

    
    for i in range(self.iterations):
      v=K.batch_dot(p,v)
      if self.activate:
        v=self.advrelu(v,self.activation)
  
    ret=K.reshape(v,(-1,self.gs,self.param))#keine Ahnung ob richtig rum #doch scheint zu passen

    return ret


    
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==3
    assert pshape[-1]==self.gs
    assert pshape[-2]==self.gs

    shape=list(input_shape[1])
    assert len(shape)==3
    assert shape[-1]==self.param
    assert shape[-2]==self.gs

    return tuple(shape)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"iterations":self.iterations,"alinearity":self.activation,"self_initializer":self.self_initializer,"neig_initializer":self.neig_initializer,"learnable":self.learnable}
    th=super(glim,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return glim(**config)















class gl(Layer):
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
  def __init__(self,graphmax=20,graphvar=40,keepconst=10,iterations=1,alinearity=[-1.0,1.0],kernel_initializer='glorot_uniform',**kwargs):
    self.kernel_initializer=kernel_initializer
    self.graphmax=graphmax
    self.graphvar=graphvar
    self.keepconst=keepconst
    self.makezerolmat=K.constant(self.genmakezerolmat(graphmax))
    self.iterations=iterations
    self.activate=False
    if len(alinearity)==2:
      self.activate=True
      self.activation=alinearity#most general form of continous activation: const,x,const
    else:
      self.activation=[]

    super(gl,self).__init__(input_shape=(graphmax,graphmax+graphvar))

  def get_config(self):
    mi={"graphmax":self.graphmax,"graphvar":self.graphvar,"keepconst":self.keepconst,"iterations":self.iterations,"alinearity":self.activation,"kernel_initializer":self.kernel_initializer}
    th=super(gl,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gl(**config)
  
  def build(self, input_shape):
    self.neigintact=self.add_weight(name='neigthbourinteraction',
                                shape=(self.graphvar,self.graphvar-self.keepconst,),
                                initializer=self.kernel_initializer,
                                trainable=True)
    self.selfintact=self.add_weight(name='selfinteraction',
                                shape=(self.graphvar,self.graphvar-self.keepconst,),
                                initializer=self.kernel_initializer,
                                trainable=True)

    self.built=True

  def genmakezerolmat(self,n):
    ret=np.zeros((n,n))+1.0
    for i in range(n):
      ret[i,i]=0.0
    return ret

  def call(self,x):
    # print("!",x.shape)
    mat=x[:,:,:self.graphmax]
    val=x[:,:,self.graphmax:]
    con=val[:,:,:self.keepconst]
    var=val[:,:,self.keepconst:]
    mat0=mat*self.makezerolmat
    
    tra=trace(mat)
    # print(mat0.shape,val.shape)
    # val=K.permute_dimensions(val,(1,0,2))
    # print(mat0.shape,val.shape)
    # mat0=K.permute_dimensions(mat0,(1,0,2))
    # val =K.permute_dimensions(val ,(1,2,0))
    # print(mat0.shape,val.shape)

    # weignei=K.dot(mat0,val)
    # weignei=K.dot(val,mat0)
    for i in range(self.iterations):
      weignei=K.batch_dot(mat0,val)
      
      # print("---",weignei.shape)
      # return K.sum(K.sum(weignei,axis=-1),axis=-1)
      # exit()
      
      # print(weignei.shape)
      
      
      parta=K.dot(weignei,self.neigintact)
      partb=K.dot(val,self.selfintact)
      # print(parta.shape,tra.shape)

      # print(parta.shape)
      
      # exit()
      var=parta+partb

      var=K.permute_dimensions(var,(1,2,0))
      
      # return tra
      
      var/=tra
      var=K.permute_dimensions(var,(2,0,1))


      if self.activate:
        val=self.advrelu(val,self.activation)


      val=K.concatenate((con,var),axis=-1)

      # return K.sum(K.sum(val,axis=-1),axis=-1)
      # print("###",K.eval(val))
      
      
      # print(parta.shape,partb.shape,var.shape,val.shape)
    
    
    # exit()
    return K.concatenate((mat,val),axis=-1)
    
    # print("call")
    # # print(x.shape)
    # m=((K.dot(K.pow(x,2),self.kernel)))
    # # print("!",m.shape)
    # E=((K.dot(x,K.constant(np.array([[1.0],[0.0],[0.0],[0.0]])))))
    # px=((K.dot(x,K.constant(np.array([[0.0],[1.0],[0.0],[0.0]])))))
    # py=((K.dot(x,K.constant(np.array([[0.0],[0.0],[1.0],[0.0]])))))
    # pt=K.sqrt(K.square(px)+K.square(py))

    return x#K.constant([1,1])#K.concatenate((m,pt),axis=-1)#still missing: matrix*E+ matrix*abstand(vektor, ich)

    
  def compute_output_shape(self,input_shape):
    # return tuple([input_shape[0],40,60])
    # return tuple([input_shape[0]])
    # return tuple(input_shape)
    shape=list(input_shape)
    assert len(shape)==3
    assert shape[-1]==self.graphmax+self.graphvar
    assert shape[-2]==self.graphmax
    #shape[-1]=self.graphmax+self.graphvar#this layer should not chance the size of the network, so this line becomes kinda useless
    # shape[-2]=self.graphmax
    return tuple(shape)
    # return tuple([15,2])
    # return tuple(K.constant([1,1]).shape)
    
#    assert len(shape)==2
    # assert shape[-1]==4
    # shape[-1]=2
    # return tuple(shape)


















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


















class gchooseparam(Layer):
  def __init__(self,gs=50,param=30,q=[0,3],**kwargs):
    self.gs=gs
    self.param=param
    self.q=q
    super(gchooseparam,self).__init__(**kwargs)


  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]

    parts=[]
    for q in self.q:
      ac=K.reshape(x[:,:self.gs,q],(-1,self.gs,1))
      parts.append(ac)

    ret=K.concatenate(parts,axis=-1)   

 

    return ret

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[-1]==self.param
    assert input_shape[-2]==self.gs
    return tuple([input_shape[0],self.gs,len(self.q)])    

  def get_config(self):
    mi={"param":self.param,"gs":self.gs,"q":self.q}
    th=super(gchooseparam,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gchooseparam(**config)


















class gfromparam(Layer):
  def __init__(self,gs=1,param=40,**kwargs):
    self.gs=gs
    self.param=param
    super(gfromparam,self).__init__(**kwargs)

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]

    return K.reshape(x,(-1,self.gs,self.param))

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==2
    assert input_shape[1]==self.gs*self.param
    return tuple([input_shape[0],self.gs,self.param])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param}
    th=super(gfromparam,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gfromparam(**config)


















class glkeep(Layer):
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
  def __init__(self,graphmax=20,graphvar=40,keepconst=10,iterations=1,alinearity=[-1.0,1.0],kernel_initializer='glorot_uniform',dimension=0,**kwargs):
    self.kernel_initializer=kernel_initializer
    self.graphmax=graphmax
    self.graphvar=graphvar
    self.keepconst=keepconst
    self.makezerolmat=K.constant(self.genmakezerolmat(graphmax))
    self.iterations=iterations
    self.dimension=dimension
    self.activate=False
    if len(alinearity)==2:
      self.activate=True
      self.activation=alinearity#most general form of continous activation: const,x,const
    else:
      self.activation=[]

    super(glkeep,self).__init__(input_shape=(graphmax,graphmax*(dimension+1)+graphvar))

  def get_config(self):
    mi={"graphmax":self.graphmax,"graphvar":self.graphvar,"keepconst":self.keepconst,"iterations":self.iterations,"alinearity":self.activation,"kernel_initializer":self.kernel_initializer,"dimension":self.dimension}
    th=super(glkeep,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return glkeep(**config)
  
  def build(self, input_shape):
    self.neigintact=self.add_weight(name='neighborinteraction',
                                shape=(self.graphvar,self.graphvar-self.keepconst,),
                                initializer=self.kernel_initializer,
                                trainable=True)
    self.selfintact=self.add_weight(name='selfinteraction',
                                shape=(self.graphvar,self.graphvar-self.keepconst,),
                                initializer=self.kernel_initializer,
                                trainable=True)

    self.built=True

  def genmakezerolmat(self,n):
    ret=np.zeros((n,n))+1.0
    for i in range(n):
      ret[i,i]=0.0
    return ret

  def call(self,x):
    # print("!",x.shape)
    mat=x[:,:,:self.graphmax]
    rmat=x[:,:,self.graphmax:self.graphmax*(self.dimension+1)]
    val=x[:,:,self.graphmax*(self.dimension+1):]
    con=val[:,:,:self.keepconst]
    var=val[:,:,self.keepconst:]
    mat0=mat*self.makezerolmat
    
    tra=trace(mat)
    # print(mat0.shape,val.shape)
    # val=K.permute_dimensions(val,(1,0,2))
    # print(mat0.shape,val.shape)
    # mat0=K.permute_dimensions(mat0,(1,0,2))
    # val =K.permute_dimensions(val ,(1,2,0))
    # print(mat0.shape,val.shape)

    # weignei=K.dot(mat0,val)
    # weignei=K.dot(val,mat0)
    for i in range(self.iterations):
      weignei=K.batch_dot(mat0,val)
      
      # print("---",weignei.shape)
      # return K.sum(K.sum(weignei,axis=-1),axis=-1)
      # exit()
      
      # print(weignei.shape)
      
      
      parta=K.dot(weignei,self.neigintact)
      partb=K.dot(val,self.selfintact)
      # print(parta.shape,tra.shape)

      # print(parta.shape)
      
      # exit()
      var=parta+partb

      var=K.permute_dimensions(var,(1,2,0))
      
      # return tra
      
      var/=tra
      var=K.permute_dimensions(var,(2,0,1))


      if self.activate:
        val=self.advrelu(val,self.activation)


      val=K.concatenate((con,var),axis=-1)

      # return K.sum(K.sum(val,axis=-1),axis=-1)
      # print("###",K.eval(val))
      
      
      # print(parta.shape,partb.shape,var.shape,val.shape)
    
    
    # exit()
    return K.concatenate((mat,rmat,val),axis=-1)
    
    # print("call")
    # # print(x.shape)
    # m=((K.dot(K.pow(x,2),self.kernel)))
    # # print("!",m.shape)
    # E=((K.dot(x,K.constant(np.array([[1.0],[0.0],[0.0],[0.0]])))))
    # px=((K.dot(x,K.constant(np.array([[0.0],[1.0],[0.0],[0.0]])))))
    # py=((K.dot(x,K.constant(np.array([[0.0],[0.0],[1.0],[0.0]])))))
    # pt=K.sqrt(K.square(px)+K.square(py))

    return x#K.constant([1,1])#K.concatenate((m,pt),axis=-1)#still missing: matrix*E+ matrix*abstand(vektor, ich)

    
  def compute_output_shape(self,input_shape):
    # return tuple([input_shape[0],40,60])
    # return tuple([input_shape[0]])
    # return tuple(input_shape)
    shape=list(input_shape)
    assert len(shape)==3
    assert shape[-1]==self.graphmax*(self.dimension+1)+self.graphvar
    assert shape[-2]==self.graphmax
    #shape[-1]=self.graphmax+self.graphvar#this layer should not chance the size of the network, so this line becomes kinda useless
    # shape[-2]=self.graphmax
    return tuple(shape)
    # return tuple([15,2])
    # return tuple(K.constant([1,1]).shape)
    
#    assert len(shape)==2
    # assert shape[-1]==4
    # shape[-1]=2
    # return tuple(shape)


















class gcomdensemerge(Layer):
  def __init__(self,gs=20,param=30,paramo=40,ags=10,initializer="glorot_uniform",trainable=True,**kwargs):
    #c=2
    #mode="min"
    self.gs=gs
    self.param=param
    self.paramo=paramo
    self.ags=ags
    self.initializer=initializer
    self.trainable=trainable
    super(gcomdensemerge,self).__init__(**kwargs)

  def build(self, input_shape):

    self.trafo=self.add_weight(name="trafo",
                               shape=(self.ags*self.param,self.paramo),
                               initializer=self.initializer,
                               trainable=self.trainable)


    self.built=True


  def call(self,x):
    x=x[0]#params

    #shall take a 4d feature vector of shape (-1,gs,ags,param), and transform it using trafo into (-1,gs,paramo)

    #print("x",x.shape)

    xi=K.reshape(x,(-1,self.gs,self.ags*self.param))
    #print("xi",xi.shape)

    xt=K.dot(xi,self.trafo)
    #print("xt",xt.shape)


    return xt

    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==4
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.ags
    assert g_shape[3]==self.param
    return tuple([g_shape[0],self.gs,self.paramo])

  def get_config(self):
    mi={"gs":self.gs,"ags":self.ags,"param":self.param,"paramo":self.paramo,"initializer":self.initializer,"trainable":self.trainable}
    th=super(gcomdensemerge,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomdensemerge(**config)























class gshuffle(Layer):#shuffles the param
  def __init__(self,gs=20,param=40,seed=None,**kwargs):
    self.gs=gs
    self.param=param
    self.seed=seed
    super(gshuffle,self).__init__(input_shape=(gs,param))

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]

    x=K.reshape(x,(-1,self.gs,self.param))

    x=K.permute_dimensions(x,(2,0,1))#can only shuffle the first dimension 

    x=t.random.shuffle(x,seed=self.seed)
    
    x=K.permute_dimensions(x,(1,2,0))#dispermute

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
    mi={"gs":self.gs,"param":self.param,"seed":self.seed}
    th=super(gshuffle,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gshuffle(**config)


















class gcutparam(Layer):#takes in a param list, and splits it up into two differnt kind of params
  def __init__(self,gs=20,param1=20,param2=20,**kwargs):
    self.gs=gs
    self.param1=param1
    self.param2=param2
    super(gcutparam,self).__init__(**kwargs)


  def get_config(self):
    mi={"gs":self.gs,"param1":self.param1,"param2":self.param2}
    th=super(gcutparam,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcutparam(**config)

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]
    
    x1=x[:,:,:self.param1]
    x2=x[:,:,self.param1:]

 
    x1=K.reshape(x1,(-1,self.gs,self.param1))
    x2=K.reshape(x2,(-1,self.gs,self.param2))#to keep the shape   

 
    return x1,x2

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param1+self.param2
    return tuple([input_shape[0],self.gs,self.param1]),tuple([input_shape[0],self.gs,self.param2])    




















class glcreate(Layer):
  def __init__(self,gs=20,param=40,**kwargs):
    self.gs=gs
    self.param=param

    super(glcreate,self).__init__(**kwargs)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param}
    th=super(glcreate,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return glcreate(**config)
  
  def build(self, input_shape):

    self.built=True

  def call(self,x):
    #print("!",x[0].shape,x[1].shape)
    mat=x[0]
    val=x[1]
    wei=K.batch_dot(mat,val)
      
    ret=K.concatenate((val,wei),axis=-1)

    
    return ret


    
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==3
    assert pshape[-1]==self.gs
    assert pshape[-2]==self.gs

    shape=list(input_shape[1])
    assert len(shape)==3
    assert shape[-1]==self.param
    assert shape[-2]==self.gs

    return tuple([shape[0],self.gs,self.param*2])


















class gcomdepool(Layer):
  def __init__(self,gs=20,param=40,paramo=40,c=2,metrik_init="glorot_uniform",learnable=True,**kwargs):
    self.gs=gs
    self.param=param
    self.metrik_init=metrik_init
    self.c=c
    self.ogs=int(self.gs*self.c)
    self.learnable=learnable
    self.paramo=paramo
    super(gcomdepool,self).__init__(**kwargs)

  def build(self, input_shape):

    self.trafo=self.add_weight(name="trafo",
                                shape=(self.param,self.paramo*self.c),
                                initializer=self.metrik_init,#ignores metrik_init completely
                                trainable=self.learnable,
                                regularizer=None)

#    self.metrik=self.add_weight(name="metrik",
#                                shape=(self.param,1),
#                                initializer=keras.initializers.ones(),#ignores metrik_init completely
#                                trainable=not self.learnable,
#                                regularizer=None)


    self.built=True


  def call(self,x):
    x=x[0]
 
    print("x",x.shape)
    

    print("trafo",self.trafo.shape)


    traf=K.dot(x,self.trafo)
    print("traf",traf.shape)


    ret=K.reshape(traf,(-1,self.ogs,self.paramo))
    print("ret",ret.shape)
    
    return ret

    exit()

  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.ogs,self.paramo])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"c":self.c,"metrik_init":self.metrik_init,"learnable":self.learnable,"paramo":self.paramo}
    th=super(gcomdepool,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomdepool(**config)


















class gcomparastract(Layer):
  def __init__(self,gs=20,param=30,c=2,**kwargs):
    #c=2
    #mode="min"
    assert gs % c==0#assume there is an equal splitting
    self.gs=gs
    self.param=param
    self.c=c
    self.ogs=int(self.gs/self.c)
    super(gcomparastract,self).__init__(**kwargs)

  def build(self, input_shape):




    self.built=True


  def call(self,x):
    x=x[0]#reordered params gs*param

    #shall take x and take out the ogs c*param features, and concat them   

    feats=[]

    ogs=self.ogs
    c=self.c

    for i in range(ogs):
      start=i*c
      end=(i+1)*c
      amat=x[:,start:end,:self.param]
      amat=K.reshape(amat,(-1,1,c,self.param))
      feats.append(amat)
    

    ret=K.concatenate(feats,axis=1)

    return ret


    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==3
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.param
    return tuple([g_shape[0],self.ogs,self.c,self.param])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c,"param":self.param}
    th=super(gcomparastract,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomparastract(**config)


















class gcompoolmerge(Layer):
  def __init__(self,gs=20,param=30,mode="max",ags=10,**kwargs):
    #c=2
    #mode="min"
    self.gs=gs
    self.param=param
    self.mode=mode
    self.ags=ags
    super(gcompoolmerge,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                           shape=(self.ags*self.param,self.paramo),
    #                           initializer=self.initializer,
    #                           trainable=self.trainable)


    self.built=True


  def call(self,x):
    x=x[0]#params

    #shall take a 4d feature vector of shape (-1,gs,ags,param), and transform it using mode pooling into (-1,gs,paramo)

    print("x",x.shape)

    if self.mode=="max":
      ret=K.max(x,axis=2)
    if self.mode=="min":
      ret=K.min(x,axis=2)
    if self.mode=="mean":
      ret=K.mean(x,axis=2)
    
    #print("ret",ret.shape)

    #exit()

    return ret
    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==4
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.ags
    assert g_shape[3]==self.param
    return tuple([g_shape[0],self.gs,self.param])

  def get_config(self):
    mi={"gs":self.gs,"ags":self.ags,"param":self.param,"mode":self.mode}
    th=super(gcompoolmerge,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcompoolmerge(**config)


















class gfeatkeep(Layer):
  def __init__(self,gs=20,param=40,dimension=0,**kwargs):
    self.gs=gs
    self.param=param
    self.dimension=dimension
    super(gfeatkeep,self).__init__(input_shape=(gs,gs*(dimension+1)+param))

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"dimension":self.dimension}
    th=super(gfeatkeep,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gfeatkeep(**config)

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    return x[:,:,-self.param:]
    

    
  def compute_output_shape(self,input_shape):

    #print("called output of gfeatkeep for is=",input_shape)
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.gs*(self.dimension+1)+self.param
    return tuple([input_shape[0],self.gs,self.param])    




















class gcomdepoolplus(Layer):#simply produces a constant graph additionally to gcomdepool
  def __init__(self,gs=20,param=40,paramo=40,c=2,metrik_init="glorot_uniform",graph_init=keras.initializers.Identity(),learnable=True,**kwargs):
    self.gs=gs
    self.param=param
    self.metrik_init=metrik_init
    self.graph_init=graph_init
    self.c=c
    self.ogs=int(self.gs*self.c)
    self.learnable=learnable
    self.paramo=paramo
    super(gcomdepoolplus,self).__init__(**kwargs)

  def build(self, input_shape):

    self.trafo=self.add_weight(name="trafo",
                                shape=(self.param,self.paramo*self.c),
                                initializer=self.metrik_init,
                                trainable=self.learnable,
                                regularizer=None)

    self.graph=self.add_weight(name="graph",
                                shape=(self.c,self.c),
                                initializer=self.graph_init,
                                trainable=self.learnable,
                                regularizer=None)


    self.built=True


  def call(self,x):
    x=x[0]
 
    #print("x",x.shape)
    

    #print("trafo",self.trafo.shape)


    traf=K.dot(x,self.trafo)
    #print("traf",traf.shape)


    ret=K.reshape(traf,(-1,self.ogs,self.paramo))
    #print("ret",ret.shape)
    
    return ret,self.graph

    #exit()

  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.ogs,self.paramo]),tuple([self.c,self.c])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"c":self.c,"metrik_init":self.metrik_init,"graph_init":self.graph_init,"learnable":self.learnable,"paramo":self.paramo}
    th=super(gcomdepoolplus,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomdepoolplus(**config)


















class gkeepcutter(Layer):
  def __init__(self,inn=30,param=40,out=20,dimension=0,**kwargs):
    assert inn>=out
    self.inn=inn
    self.param=param
    self.out=out
    self.dimension=dimension
    super(gkeepcutter,self).__init__(input_shape=(inn,inn*(dimension+1)+param))


  def build(self, input_shape):

    self.built=True


  def call(self,x):
    
    x=x[:,:self.out,:]
    mainmat=x[:,:,:self.out]
    otmats=[]
    for i in range(self.dimension):
      otmats.append(x[:,:,self.inn*(i+1):self.inn*(i+1)+self.out])
    params=x[:,:,-self.param:]
    
    otmats.insert(0,mainmat)
    otmats.append(params)

    return K.concatenate(otmats,axis=-1)

    
  def compute_output_shape(self,input_shape):
    assert len(input_shape)==3
    assert input_shape[1]==self.inn
    assert input_shape[2]==self.inn*(self.dimension+1)+self.param
    return tuple([input_shape[0],self.out,self.out*(self.dimension+1)+self.param])    

  def get_config(self):
    mi={"inn":self.inn,"param":self.param,"out":self.out,"dimension":self.dimension}
    th=super(gkeepcutter,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gkeepcutter(**config)


















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




















class gortho(Layer):#multiplies all elements with one orthogonal matrix
  def __init__(self,gs=20,param=40,seed=None,**kwargs):
    self.gs=gs
    self.param=param
    self.seed=seed
    super(gortho,self).__init__(input_shape=(gs,param))

  def build(self, input_shape):

    self.trafo=self.add_weight(name='orthogonal_trafo',#Matrix N
                               shape=(self.param,self.param),
                               initializer=keras.initializers.Orthogonal(seed=self.seed),
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
    mi={"gs":self.gs,"param":self.param,"seed":self.seed}
    th=super(gortho,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gortho(**config)


















class gvaluation(Layer):
  def __init__(self,gs=20,param=40,metrik_init="glorot_uniform",learnable=True,**kwargs):
    self.gs=gs
    self.param=param
    self.metrik_init=metrik_init
    self.learnable=learnable
    super(gvaluation,self).__init__(**kwargs)

  def build(self, input_shape):


    self.metrik=self.add_weight(name="metrik",
                                shape=(self.param,1),
                                initializer=self.metrik_init,#ignores metrik_init completely
                                trainable=self.learnable,
                                regularizer=None)


    self.built=True


  def call(self,x):
    x=x[0]
 
    #print("x",x.shape)
    
    xp=K.permute_dimensions(x,(0,2,1))
    #print("xp",xp.shape)

    #print("metrik",self.metrik.shape)


    #currently just uses the last value as sorting param
    values=K.reshape(K.dot(x,self.metrik),(-1,self.gs))
    #print("values",values.shape)

    vr=K.reshape(values,(-1,self.gs,1))
    #print("vr",vr.shape)

    ret=K.concatenate((x,vr))
    #print("ret",ret.shape)

    return ret

    exit()

    _,valueorder=t.math.top_k(values,k=self.gs)
    print("valueorder",valueorder.shape)

    xg=t.gather(params=x,indices=valueorder,axis=1,batch_dims=1)
    print("xg",xg.shape)

    xs=K.reshape(xg,(-1,self.ogs,self.param*self.c))
    print("xs",xs.shape)


    traf=K.dot(xs,self.trafo)
    print("traf",traf.shape)

    return traf



    exit()

    

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.gs,self.param+1])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"metrik_init":self.metrik_init,"learnable":self.learnable}
    th=super(gvaluation,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gvaluation(**config)


















class gcomparamcombinations(Layer):#shall take a 3d layer (?,gs,param) and output a corresponding combination assemble (?,gs,gs,param,2) (param of all combinations of gs) 
  def __init__(self,gs=20,param=30,**kwargs):
    self.gs=gs
    self.param=param
    super(gcomparamcombinations,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                           shape=(self.param,self.c*self.c),
    #                           initializer=self.initializer,
    #                           trainable=self.trainable)


    self.built=True


  def call(self,x):
    x=x[0]#params

    parts=[]
    for i in range(self.gs):
      ac=x[:,i,:self.param]
      ac=K.reshape(ac,(-1,1,1,self.param,1))
      parts.append(ac)

    ret=[]
    for x in range(self.gs):
      toc=[]
      for y in range(self.gs):
        ac=K.concatenate((parts[x],parts[y]),axis=-1)
        toc.append(ac)
      ret.append(K.concatenate(toc,axis=2))
    ret=K.concatenate(ret,axis=1)

    return ret
    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==3
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.param
    return tuple([g_shape[0],self.gs,self.gs,self.param,2])

  def get_config(self):
    mi={"gs":self.gs,"param":self.param}
    th=super(gcomparamcombinations,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomparamcombinations(**config)


















class ggoparam(Layer):
  def __init__(self,gs=1,param=40,**kwargs):
    self.gs=gs
    self.param=param
    super(ggoparam,self).__init__(**kwargs)

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]

    return K.reshape(x,(-1,self.gs*self.param))

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.gs*self.param])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param}
    th=super(ggoparam,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return ggoparam(**config)


















class gcomgraphfromparam(Layer):#shall take a 3d layer (?,gs,param) and output a corresponding graph of type (?,gs,c,c) 
  def __init__(self,gs=20,param=30,c=2,initializer="glorot_uniform",trainable=True,**kwargs):
    #c=2
    #mode="min"
    self.gs=gs
    self.param=param
    self.c=c
    self.initializer=initializer
    self.trainable=trainable
    super(gcomgraphfromparam,self).__init__(**kwargs)

  def build(self, input_shape):

    self.trafo=self.add_weight(name="trafo",
                               shape=(self.param,self.c*self.c),
                               initializer=self.initializer,
                               trainable=self.trainable)


    self.built=True


  def call(self,x):
    x=x[0]#params

    #shall take a 3d feature vector of shape (-1,gs,param), and transform it using trafo into (-1,gs,c,paramo)

    #print("x",x.shape)

    #xi=K.reshape(x,(-1,self.gs,self.ags*self.param))
    #print("xi",xi.shape)

    xt=K.dot(x,self.trafo)
    #print("xt",xt.shape)

    A=K.reshape(xt,(-1,self.gs,self.c,self.c))
    
    #print("xp",xp.shape)

    #exit()

    return A

    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==3
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.param
    return tuple([g_shape[0],self.gs,self.c,self.c])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c,"param":self.param,"initializer":self.initializer,"trainable":self.trainable}
    th=super(gcomgraphfromparam,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomgraphfromparam(**config)


















class gbrokengrowth(Layer):
  def __init__(self,inn=20,out=30,param=40,kernel_initializer="glorot_uniform",**kwargs):
    self.inn=inn
    self.out=out
    self.param=param
    self.kernel_initializer=kernel_initializer
    super(gbrokengrowth,self).__init__(**kwargs)

  def get_config(self):
    mi={"inn":self.inn,"out":self.out,"param":self.param}
    th=super(gbrokengrowth,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gbrokengrowth(**config)
  
  def build(self, input_shape):

    self.inc=self.add_weight(name='inc',
                                shape=(self.param*self.inn,self.param*(self.out-self.inn)),
                                initializer=self.kernel_initializer,
                                trainable=True)
    self.built=True

  def call(self,x):
    x=x[0]
    
    f=K.reshape(x,(-1,self.param*self.inn))
    fa=K.dot(f,self.inc)
    r=K.concatenate((f,fa),axis=-1)
    
    return K.reshape(r,(-1,self.out,self.param))
    
     

 
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==3
    assert pshape[-1]==self.param
    assert pshape[-2]==self.inn
    pshape[-2]=self.out
    return tuple(pshape)


















class glm(Layer):#not anymore using keepconst, also not setting the diagonal to zero
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
  def __init__(self,gs=20,param=40,iterations=1,alinearity=[-1.0,1.0],kernel_initializer='glorot_uniform',self_initializer=None,neig_initializer=None,learnable=True,**kwargs):
    if self_initializer==None:
      self.self_initializer=kernel_initializer
    else:
      self.self_initializer=self_initializer
    if neig_initializer==None:
      self.neig_initializer=kernel_initializer
    else:
      self.neig_initializer=neig_initializer

    self.gs=gs
    self.param=param
    self.iterations=iterations
    self.activate=False
    if len(alinearity)==2:
      self.activate=True
      self.activation=alinearity
    else:
      self.activation=[]
    self.learnable=learnable

    super(glm,self).__init__(**kwargs)

  
  def build(self, input_shape):
    self.neigintact=self.add_weight(name='neigthbourinteraction',#Matrix N
                                shape=(self.param,self.param),
                                initializer=self.neig_initializer,
                                trainable=self.learnable)
    self.selfintact=self.add_weight(name='selfinteraction',#Matrix S
                                shape=(self.param,self.param),
                                initializer=self.self_initializer,
                                trainable=self.learnable)

    self.built=True

  def call(self,x):
    mat=x[0]#Matrix A
    val=x[1]

    eye=K.eye(self.gs)
 
    p1=kron(eye,self.selfintact)
    p2=kron_b1(mat,self.neigintact)
    p=p1+p2

      
    v=K.reshape(val,(-1,self.gs*self.param))

    
    for i in range(self.iterations):
      v=K.batch_dot(p,v)
      if self.activate:
        v=self.advrelu(v,self.activation)
  
    ret=K.reshape(v,(-1,self.gs,self.param))#keine Ahnung ob richtig rum #doch scheint zu passen

    return ret


    
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==3
    assert pshape[-1]==self.gs
    assert pshape[-2]==self.gs

    shape=list(input_shape[1])
    assert len(shape)==3
    assert shape[-1]==self.param
    assert shape[-2]==self.gs

    return tuple(shape)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"iterations":self.iterations,"alinearity":self.activation,"self_initializer":self.self_initializer,"neig_initializer":self.neig_initializer,"learnable":self.learnable}
    th=super(glm,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return glm(**config)















class gcutter(Layer):
  def __init__(self,inn=30,param=40,out=20,**kwargs):
    assert inn>=out
    self.inn=inn
    self.param=param
    self.out=out
    super(gcutter,self).__init__(**kwargs)


  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]
 
    return x[:,:self.out,:self.param]

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[-1]==self.param
    assert input_shape[-2]==self.inn
    return tuple([input_shape[0],self.out,self.param])    

  def get_config(self):
    mi={"inn":self.inn,"param":self.param,"out":self.out}
    th=super(gcutter,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcutter(**config)


















class glacreate(Layer):
  def __init__(self,gs=20,param=40,a=2,**kwargs):
    self.gs=gs
    self.param=param
    self.a=a

    super(glacreate,self).__init__(**kwargs)

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"a":self.a}
    th=super(glacreate,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return glacreate(**config)
  
  def build(self, input_shape):

    self.built=True

  def call(self,x):
    #print("!",x[0].shape,x[1].shape)
    mat=x[0]
    val=x[1]

    rmat=K.reshape(mat,(-1,self.gs,self.gs))
    rval=K.reshape(val,(-1,self.gs,self.param))
    
    rwei=K.batch_dot(rmat,rval)
    wei=K.reshape(rwei,(-1,self.a,self.gs,self.param)) 



    ret=K.concatenate((val,wei),axis=-1)

    
    return ret


    
  def compute_output_shape(self,input_shape):
    pshape=list(input_shape[0])
    assert len(pshape)==4
    assert pshape[-3]==self.a
    assert pshape[-1]==self.gs
    assert pshape[-2]==self.gs

    shape=list(input_shape[1])
    assert len(shape)==4
    assert shape[-3]==self.a
    assert shape[-1]==self.param
    assert shape[-2]==self.gs

    return tuple([shape[0],self.a,self.gs,self.param*2])


















class gcomjpool(Layer):
  def __init__(self,gs=20,param=40,paramo=40,c=2,metrik_init="glorot_uniform",learnable=True,**kwargs):
    assert gs % c==0#assume there is an equal splitting
    self.gs=gs
    self.param=param
    self.metrik_init=metrik_init
    self.c=c
    self.ogs=int(self.gs/self.c)
    self.learnable=learnable
    self.paramo=paramo
    super(gcomjpool,self).__init__(**kwargs)

  def build(self, input_shape):

    self.trafo=self.add_weight(name="trafo",
                                shape=(self.param*self.c,self.paramo),
                                initializer=self.metrik_init,#ignores metrik_init completely
                                trainable=self.learnable,
                                regularizer=None)



    self.built=True


  def call(self,x):
    x=x[0]
    valueorder=x[1] 

    valueorder=K.cast(valueorder,"int32")

    xg=t.gather(params=x,indices=valueorder,axis=1,batch_dims=1)
    xs=K.reshape(xg,(-1,self.ogs,self.param*self.c))
    traf=K.dot(xs,self.trafo)
    return traf

    

    
  def compute_output_shape(self,input_shape):
    v_shape=input_shape[1]
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    assert len(v_shape)==2
    assert v_shape[-1]==self.gs
    

    return tuple([input_shape[0],self.ogs,self.paramo])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"c":self.c,"metrik_init":self.metrik_init,"learnable":self.learnable,"paramo":self.paramo}
    th=super(gcomjpool,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomjpool(**config)


















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


















class gssort(Layer):
  def __init__(self,gs=20,param=40,index=-1,**kwargs):
    self.gs=gs
    self.param=param
    self.index=index
    super(gssort,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                            shape=(self.param*self.c,self.paramo),
    #                            initializer=self.metrik_init,#ignores metrik_init completely
    #                            trainable=self.learnable,
    #                            regularizer=None)

    #self.metrik=self.add_weight(name="metrik",
    #                            shape=(self.param,1),
    #                            initializer=keras.initializers.ones(),#ignores metrik_init completely
    #                            trainable=not self.learnable,
    #                            regularizer=None)


    self.built=True


  def call(self,x):
    x=x[0]
 
    #print("x",x.shape)
    



    #currently just uses the index value as sorting param
    values=x[:,:,self.index]#K.reshape(K.dot(x,self.metrik),(-1,self.gs))
    #print("values",values.shape)

    _,valueorder=t.math.top_k(values,k=self.gs)
    #print("valueorder",valueorder.shape)

    #valueorder=t.argsort(values,axis=-1)
    #print("valueorder",valueorder.shape)

    xg=t.gather(params=x,indices=valueorder,axis=1,batch_dims=1)
    print("xg",xg.shape)

    return xg

    #exit()

    #xs=K.reshape(xg,(-1,self.ogs,self.param*self.c))
    #print("xs",xs.shape)


    #traf=K.dot(xs,self.trafo)
    #print("traf",traf.shape)

    #return traf



    exit()

    

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.gs,self.param])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"index":self.index}
    th=super(gssort,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gssort(**config)


















class gcomgraphlevel(Layer):#takes a (?,gs,gs,c,c) and converts it into (?,c*gs,c*gs)
  def __init__(self,gs=20,c=2,**kwargs):
    self.gs=gs
    self.c=c
    super(gcomgraphlevel,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                           shape=(self.param,self.c*self.c),
    #                           initializer=self.initializer,
    #                           trainable=self.trainable)


    self.built=True

  #def R(self,x):
  #  return K.relu(self.c_const*(x-self.cut)+1)-K.relu(self.c_const*(x-self.c_const))
  def call(self,x):
    x=x[0]
    #print("x",x.shape)
    #exit()
    xp=K.permute_dimensions(x,(0,1,3,2,4))

    ret=K.reshape(xp,(-1,self.gs*self.c,self.gs*self.c))
    

    return ret

    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==5
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.gs
    assert g_shape[3]==self.c
    assert g_shape[4]==self.c
    return tuple([g_shape[0],self.gs*self.c,self.gs*self.c])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c}
    th=super(gcomgraphlevel,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomgraphlevel(**config)


















class gadd1(Layer):#used to simply train gltk on glmp data
  def __init__(self,gs=20,**kwargs):
    self.gs=gs
    super(gadd1,self).__init__(**kwargs)

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]
    return x+K.eye(self.gs)
    

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.gs
    return tuple([input_shape[0],self.gs,self.gs])    

  def get_config(self):
    mi={"gs":self.gs}
    th=super(gadd1,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gadd1(**config)


















class gecutter(Layer):#like gcutter, but leaves only the last elements
  def __init__(self,inn=30,param=40,out=20,**kwargs):
    assert inn>=out
    self.inn=inn
    self.param=param
    self.out=out
    super(gecutter,self).__init__(**kwargs)


  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]
 
    return x[:,-self.out:,:self.param]

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[-1]==self.param
    assert input_shape[-2]==self.inn
    return tuple([input_shape[0],self.out,self.param])    

  def get_config(self):
    mi={"inn":self.inn,"param":self.param,"out":self.out}
    th=super(gecutter,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gecutter(**config)


















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


















class gcompool(Layer):
  def __init__(self,gs=20,param=40,paramo=40,c=2,metrik_init="glorot_uniform",learnable=True,**kwargs):
    assert gs % c==0#assume there is an equal splitting
    self.gs=gs
    self.param=param
    self.metrik_init=metrik_init
    self.c=c
    self.ogs=int(self.gs/self.c)
    self.learnable=learnable
    self.paramo=paramo
    super(gcompool,self).__init__(**kwargs)

  def build(self, input_shape):

    self.trafo=self.add_weight(name="trafo",
                                shape=(self.param*self.c,self.paramo),
                                initializer=self.metrik_init,#ignores metrik_init completely
                                trainable=self.learnable,
                                regularizer=None)

#    self.metrik=self.add_weight(name="metrik",
#                                shape=(self.param,1),
#                                initializer=keras.initializers.ones(),#ignores metrik_init completely
#                                trainable=not self.learnable,
#                                regularizer=None)


    self.built=True


  def call(self,x):
    x=x[0]
 
    print("x",x.shape)
    

    print("trafo",self.trafo.shape)


    #currently just uses the last value as sorting param
    values=x[:,:,-1]#K.reshape(K.dot(x,self.metrik),(-1,self.gs))
    print("values",values.shape)

    _,valueorder=t.math.top_k(values,k=self.gs)
    print("valueorder",valueorder.shape)

    #valueorder=t.argsort(values,axis=-1)
    #print("valueorder",valueorder.shape)

    xg=t.gather(params=x,indices=valueorder,axis=1,batch_dims=1)
    print("xg",xg.shape)

    #exit()

    xs=K.reshape(xg,(-1,self.ogs,self.param*self.c))
    print("xs",xs.shape)


    traf=K.dot(xs,self.trafo)
    print("traf",traf.shape)

    return traf



    exit()

    

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.ogs,self.paramo])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"c":self.c,"metrik_init":self.metrik_init,"learnable":self.learnable,"paramo":self.paramo}
    th=super(gcompool,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcompool(**config)


















class ghealparam(Layer):#takes in a splittet param list (created by gcutparam), and merges them again
  def __init__(self,gs=20,param1=20,param2=20,**kwargs):
    self.gs=gs
    self.param1=param1
    self.param2=param2
    super(ghealparam,self).__init__(**kwargs)

  def get_config(self):
    mi={"gs":self.gs,"param1":self.param1,"param2":self.param2}
    th=super(ghealparam,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return ghealparam(**config)

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x1=x[0]
    x2=x[1]
   
    r=K.concatenate((x1,x2),axis=-1)

 
    
    return r

    
  def compute_output_shape(self,input_shape):
    assert len(input_shape)==2
    i1=input_shape[0]
    i2=input_shape[1]
    assert len(i1)==3
    assert len(i2)==3
    assert i1[1]==self.gs
    assert i2[1]==self.gs
    assert i1[2]==self.param1
    assert i2[2]==self.param2
    return tuple([input_shape[0],self.gs,self.param1+self.param2])    




















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


















class gcomgraphrepeat(Layer):#repeats a (?,gs,gs) into (?,c*gs,c*gs)
  def __init__(self,gs=20,c=2,**kwargs):
    self.gs=gs
    self.c=c
    super(gcomgraphrepeat,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                           shape=(self.param,self.c*self.c),
    #                           initializer=self.initializer,
    #                           trainable=self.trainable)


    self.built=True

  #def R(self,x):
  #  return K.relu(self.c_const*(x-self.cut)+1)-K.relu(self.c_const*(x-self.c_const))
  def call(self,x):
    x=x[0]


    one=K.ones(shape=(self.c,self.c)) 
    
    ret=kron_b1(x,one)
    
 

    return ret

    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==3
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.gs
    return tuple([g_shape[0],self.gs*self.c,self.gs*self.c])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c}
    th=super(gcomgraphrepeat,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomgraphrepeat(**config)


















class gkeepbuilder(Layer):
  def __init__(self,gs=30,param=10,free=30,learnable=True,dimension=0,use0=False,**kwargs):
    self.gs=gs
    self.param=param
    self.free=free
    self.learnable=True
    self.dimension=dimension
    self.use0=use0
    super(gkeepbuilder,self).__init__(input_shape=(gs,(gs*(dimension+1))+param))

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"free":self.free,"learnable":self.learnable,"dimension":self.dimension,"use0":self.use0}
    th=super(gkeepbuilder,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gkeepbuilder(**config)


  def fromdistsq(self,dsq):
    return K.exp(-dsq)

  def build(self, input_shape):
    if self.use0:
      self.metrik=self.add_weight(name="weight",
                                shape=(self.dimension+1,1),
                                initializer=keras.initializers.Ones(),
                                trainable=self.learnable)
    else:
      self.metrik=self.add_weight(name="weight",
                                shape=(self.dimension,1),
                                initializer=keras.initializers.Ones(),
                                trainable=self.learnable)
    self.built=True
  def lisshape(self,x):
    ret=[]
    for e in x:
      ret.append(e.shape)
    return ret
  def call(self,x):
    #print(x.shape)
   
    gs=self.gs 
    mats=[]
    for i in range(self.dimension+1):
      amat=(x[:,:gs,gs*i:gs*(i+1)])
      amat=K.reshape(amat,(-1,gs,gs,1))
      mats.append(amat)
    data=x[:,:gs,gs*(self.dimension+1):]

    mat0=mats[0]
    if self.use0:
      mat=K.concatenate(mats,axis=-1)
    else:
      mat=K.concatenate(mats[1:],axis=-1)
    metrik=self.metrik


    
    dsq=K.dot(mat,metrik)
    
    basegraph=self.fromdistsq(dsq)
    #mats.insert(0,basegraph)
    mats[0]=basegraph
    pregraph=K.concatenate(mats,axis=2)
    basegraph=K.reshape(pregraph,(-1,gs,gs*(self.dimension+1))) 
     
    #print(metrik.shape,xm.shape,xt.shape,dsq.shape)
    #print(basegraph.shape)
    
    parax=data
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
    #print("!!!", K.concatenate((basegraph,parax,zeros)).shape,basegraph.shape,pregraph.shape,parax.shape,zeros.shape,self.lisshape(mats)) 
    return K.concatenate((basegraph,parax,zeros))

    
  def compute_output_shape(self,input_shape):
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.gs*(1+self.dimension)+self.param
    return tuple([input_shape[0],input_shape[1],input_shape[2]+self.free])    




















class gtbuilder(Layer):
  def __init__(self,gs=30,param=10,free=30,**kwargs):
    self.gs=gs
    self.param=param
    self.free=free
    super(gtbuilder,self).__init__(input_shape=(gs,gs+gs+param))

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"free":self.free}
    th=super(gtbuilder,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gtbuilder(**config)


  def getmetrik(self):
    return [[1],[1]]
  def fromdistsq(self,dsq):
    return K.exp(-dsq)

  def build(self, input_shape):

    self.built=True

  def call(self,x):
    #print(x.shape)
   
    gs=self.gs 
    mata=x[:,:gs,:gs]
    matb=x[:,:gs,gs:gs+gs]
    data=x[:,:gs,gs+gs:]

    mata=K.reshape(mata,(-1,gs,gs,1))
    matb=K.reshape(matb,(-1,gs,gs,1))
     
    mat=K.concatenate((mata,matb),axis=-1)
    metrik=K.constant(self.getmetrik())
    
    dsq=K.reshape(K.dot(mat,metrik),(-1,gs,gs))
    
    basegraph=self.fromdistsq(dsq)
    
    
     
    #print(metrik.shape,xm.shape,xt.shape,dsq.shape)
    #print(basegraph.shape)
    
    parax=x[:,:,self.gs+self.gs:]#please note, that this layer is build to read two times the same data: first the one for the distance generation, and afterwards the one for node data, also note, that glbuilder does not do this, but instead works on the same dataset
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
    
    return K.concatenate((basegraph,parax,zeros))

    
  def compute_output_shape(self,input_shape):
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.gs+self.gs+self.param
    return tuple([input_shape[0],self.gs,self.gs+self.param+self.free])    




















class gpool(Layer):
  def __init__(self,gs=20,param=40,mode="max",**kwargs):
    self.gs=gs
    self.param=param
    self.mode=mode
    super(gpool,self).__init__(input_shape=(gs,param))

  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]
    if self.mode=="max":
      return K.max(x,axis=-1)
    if self.mode=="mean":
      return K.mean(x,axis=-1)
    if self.mode=="sum":
      return K.sum(x,axis=-1)

    

    
  def compute_output_shape(self,input_shape):
    print("inputting",input_shape,"param",self.param)
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    return tuple([input_shape[0],self.gs])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"mode":self.mode}
    th=super(gpool,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gpool(**config)


















class gmultiply(Layer):
  def __init__(self,gs=30,param=40,c=2,**kwargs):
    self.gs=gs
    self.param=param
    self.c=c
    super(gmultiply,self).__init__(**kwargs)


  def build(self, input_shape):

    self.built=True


  def call(self,x):
    x=x[0]
   



    l=[]
    for i in range(self.c):
      l.append(x)

    #print("l",l,len(l),self.c)
    #exit()




    q=K.concatenate(l,axis=-1)
    #print("q",q.shape)
    #exit()
    ret=K.reshape(q,(-1,self.gs*self.c,self.param))
    return ret
 
    
    exit() 



    return x

    
  def compute_output_shape(self,input_shape):
    input_shape=input_shape[0]
    assert len(input_shape)==3
    assert input_shape[-1]==self.param
    assert input_shape[-2]==self.gs
    return tuple([input_shape[0],self.gs*self.c,self.param])    

  def get_config(self):
    mi={"ga":self.gs,"param":self.param,"c":self.c}
    th=super(gmultiply,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gmultiply(**config)


















class gcomgpool(Layer):
  def __init__(self,gs=20,param=40,paramo=40,c=2,metrik_init="glorot_uniform",learnable=True,mode="mean",cut=0.5,c_const=1000,**kwargs):
    #c=2
    #mode="min"
    assert gs % c==0#assume there is an equal splitting
    self.gs=gs
    self.param=param
    self.metrik_init=metrik_init
    self.c=c
    self.ogs=int(self.gs/self.c)
    self.learnable=learnable
    self.paramo=paramo
    self.mode=mode
    self.cut=cut
    self.c_const=c_const
    super(gcomgpool,self).__init__(**kwargs)

  def build(self, input_shape):

    self.trafo=self.add_weight(name="trafo",
                                shape=(self.param*self.c,self.paramo),
                                initializer=self.metrik_init,#ignores metrik_init completely
                                trainable=self.learnable,
                                regularizer=None)

#    self.metrik=self.add_weight(name="metrik",
#                                shape=(self.param,1),
#                                initializer=keras.initializers.ones(),#ignores metrik_init completely
#                                trainable=not self.learnable,
#                                regularizer=None)


    self.built=True


  def call(self,x):
    A=x[0]#adjacency matrix
    x=x[1]#parameters
 
    #print("x",x.shape)
    #print("A",A.shape) 

    #print("trafo",self.trafo.shape)


    #currently just uses the last value as sorting param
    values=x[:,:,-1]#K.reshape(K.dot(x,self.metrik),(-1,self.gs))
    #print("values",values.shape)

    _,valueorder=t.math.top_k(values,k=self.gs)
    #print("valueorder",valueorder.shape)

    #valueorder=t.argsort(values,axis=-1)
    #print("valueorder",valueorder.shape)

    xg=t.gather(params=x,indices=valueorder,axis=1,batch_dims=1)
    #print("xg",xg.shape)

    #exit()

    xs=K.reshape(xg,(-1,self.ogs,self.param*self.c))
    #print("xs",xs.shape)


    traf=K.dot(xs,self.trafo)
    #print("traf",traf.shape)



    At1=t.gather(params=A,indices=valueorder,axis=1,batch_dims=1)
    At2=t.gather(params=At1,indices=valueorder,axis=2,batch_dims=1)

    #print("At1",At1.shape,"At2",At2.shape)


    Ar=K.reshape(At2,(-1,self.ogs,self.c,self.ogs,self.c))
    #print("Ar",Ar.shape)

    if self.mode=="mean":
      Am=K.mean(Ar,axis=(2,4))
    if self.mode=="min":
      Am=K.min(Ar,axis=(2,4))
    if self.mode=="max":
      Am=K.max(Ar,axis=(2,4))

    #print("Am",Am.shape)
    
    C=self.c_const
    cut=self.cut
    
    Ar=K.relu(1+C*(Am-cut))-K.relu(C*(Am-cut))
    

    #print("Ar",Ar.shape)


    #exit()


    return Ar,traf



    exit()

    

    
  def compute_output_shape(self,input_shape):
    grap_shape=input_shape[0]
    input_shape=input_shape[1]
    assert len(input_shape)==3
    assert len(grap_shape)==3
    assert input_shape[1]==self.gs
    assert input_shape[2]==self.param
    assert grap_shape[1]==self.gs
    assert grap_shape[2]==self.gs
    return tuple([grap_shape[0],self.ogs,self.ogs]),tuple([input_shape[0],self.ogs,self.paramo])    

  def get_config(self):
    mi={"gs":self.gs,"param":self.param,"c":self.c,"metrik_init":self.metrik_init,"learnable":self.learnable,"paramo":self.paramo,"mode":self.mode,"cut":self.cut,"c_const":self.c_const}
    th=super(gcomgpool,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomgpool(**config)


















class gmake1graph(Layer):
  def __init__(self,**kwargs):
    super(gmake1graph,self).__init__(**kwargs)

  def get_config(self):
    mi={}
    th=super(gmake1graph,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gmake1graph(**config)
  
  def build(self, input_shape):

    self.built=True

  def call(self,x):
    x=x[0]

    xs=x.shape
    par=1
    for i in range(1,len(xs)):
      par*=xs[i]


    x=K.reshape(x,[-1,par])[:,0]*0+1
    x=K.reshape(x,[-1,1,1])


    return x


 
  def compute_output_shape(self,input_shape):
    shape=list(input_shape[0])
    assert len(shape)>1
    return tuple([shape[0],1,1])


















class gcomparamlevel(Layer):#takes a (?,gs,c,param) and converts it into (?,c*gs,param)
  def __init__(self,gs=20,c=2,param=30,**kwargs):
    self.gs=gs
    self.c=c
    self.param=param
    super(gcomparamlevel,self).__init__(**kwargs)

  def build(self, input_shape):

    #self.trafo=self.add_weight(name="trafo",
    #                           shape=(self.param,self.c*self.c),
    #                           initializer=self.initializer,
    #                           trainable=self.trainable)


    self.built=True

  #def R(self,x):
  #  return K.relu(self.c_const*(x-self.cut)+1)-K.relu(self.c_const*(x-self.c_const))
  def call(self,x):
    x=x[0]


    ret=K.reshape(x,(-1,self.gs*self.c,self.param))
    

    return ret

    
    




    
  def compute_output_shape(self,input_shape):
    g_shape=input_shape[0]
    assert len(g_shape)==4
    assert g_shape[1]==self.gs
    assert g_shape[2]==self.c
    assert g_shape[3]==self.param
    return tuple([g_shape[0],self.gs*self.c,self.param])

  def get_config(self):
    mi={"gs":self.gs,"c":self.c,"param":self.param}
    th=super(gcomparamlevel,self).get_config()
    th.update(mi)
    return th
  def from_config(config):
    return gcomparamlevel(**config)

















