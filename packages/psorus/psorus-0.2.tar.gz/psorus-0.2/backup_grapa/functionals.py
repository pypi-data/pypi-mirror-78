import numpy as np
from numpy.random import randint as rndi
from numpy.random import random as rnd

from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer,Dense,Activation,Flatten,Dropout,Input,Concatenate,Dropout,Reshape,BatchNormalization,Conv2D
import tensorflow.keras as keras# as k
import tensorflow as t
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.optimizers import Adam,SGD,RMSprop
from tensorflow.keras.utils import plot_model

###import all the "migth be used" special layers

from grapa.layers import *

objects={"gbuilder":gbuilder,"gtbuilder":gtbuilder,"glbuilder":glbuilder,"gtlbuilder":gtlbuilder,"gcutter":gcutter,"gpool":gpool,"gfeat":gfeat,"gl":gl,"gkeepbuilder":gkeepbuilder,"glkeep":glkeep,"gfeatkeep":gfeatkeep,"gkeepcutter":gkeepcutter,"gkeepmatcut":gkeepmatcut,"gtopk":gtopk,"gltk":gltk,"gltknd":gltknd,"gpre1":gpre1,"gpre2":gpre2,"gpre3":gpre3,"gpre4":gpre4,"gpre5":gpre5,"glmlp":glmlp,"gltrivmlp":gltrivmlp,"gadd1":gadd1,"gaddzeros":gaddzeros,"gsym":gsym,"gbrokengrowth":gbrokengrowth,"gpoolgrowth":gpoolgrowth,"gremoveparam":gremoveparam,"gcompool":gcompool,"gcomdepool":gcomdepool,"gvaluation":gvaluation,"ggoparam":ggoparam,"gfromparam":gfromparam,"gaddbias":gaddbias,"gssort":gssort,"glm":glm,"glom":glom,"glim":glim,"ggraphstract":ggraphstract,"gmake1graph":gmake1graph,"gcomdepoolplus":gcomdepoolplus,"gcomdex":gcomdex,"gcomjpool":gcomjpool,"gcomgpool":gcomgpool,"gchooseparam":gchooseparam,"gcomdepoollg":gcomdepoollg,"gcomdiagraph":gcomdiagraph,"gcomreopool":gcomreopool,"gcomparastract":gcomparastract,"glam":glam,"gcomdensemerge":gcomdensemerge,"gcompoolmerge":gcompoolmerge,"gcomgraphcutter":gcomgraphcutter,"gcomdensediverge":gcomdensediverge,"gcomgraphfromparam":gcomgraphfromparam,"gcomgraphcombinations":gcomgraphcombinations,"gcomgraphand":gcomgraphand,"gcomgraphrepeat":gcomgraphrepeat,"gcomgraphlevel":gcomgraphlevel,"gcomgraphand2":gcomgraphand2,"gcomparamlevel":gcomparamlevel,"gliam":gliam,"gcomfullyconnected":gcomfullyconnected,"gcomparamcombinations":gcomparamcombinations,"gcomgraphfrom2param":gcomgraphfrom2param,"gcomextractdiag":gcomextractdiag,"gmultiply":gmultiply,"dedge":dedge,"dexpand":dexpand,"dnarrow":dnarrow,"dtorb":dtorb,"dreflag":dreflag,"dtcreate":dtcreate,"dtdestroy":dtdestroy,"glcreate":glcreate,"glacreate":glacreate,"gshuffle":gshuffle,"gortho":gortho,"gperm":gperm,"gpartinorm":gpartinorm,"gcutparam":gcutparam,"ghealparam":ghealparam,"gecutter":gecutter}


from constants import *








def multidense(g,m,q):
  '''runs just a list of Dense Layers (defined by m.mdense* and by the parameter q, which gives width and number of Layers) on the last axis of the input data'''
  for d in q:
    g.X=Dense(d,activation="linear",kernel_initializer=m.mdense_init_kernel,bias_initializer=m.mdense_init_bias,use_bias=m.mdense_usebias)(g.X)
    if m.mdense_batchnorm:g.X=BatchNormalization()(g.X)
    if m.mdense_activation!="linear":g.X=Activation(m.mdense_activation)(g.X)
    g.s.param=d
  return g




def norm(g,scale=True):
  """normalises a network on the last axis, scale decides if there is a learnable multiplicative factor"""
  g.X=BatchNormalization(axis=-1,scale=scale)(g.X)
  return g

def prep(g,m):#preparation handler, return g and input
  """runs my standart preparation on an Input which it defines itself and also returns"""
  inp=Input(shape=(g.s.gs,4))
  feat0=gpre5(gs=g.s.gs)(inp)
  if m.prenorm:norm(g,scale=False)
  g.X=feat0
  g.s.param=4
  return g,inp

def gq(g,m,steps=4):
  """function to work with alternative Input format (here Dense Layer on concat(self_values, neigbour_values)), migth be extended to use Convolutions. Defined by m.gq*"""
  shape0=g.X.shape
  g.X=glcreate(gs=g.s.gs,param=g.s.param)([g.A,g.X])
  for d in denseladder(c=2,n=steps,truestart=True)[::-1]:
    g.X=Dense(int(d*g.s.param),activation="linear",kernel_initializer=m.gq_init_kernel,bias_initializer=m.gq_init_bias,use_bias=m.gq_usebias)(g.X)
    if m.gq_batchnorm:g.X=BatchNormalization()(g.X)
    if m.gq_activation!="linear":g.X=Activation(m.gq_activation)(g.X)
  return g
def gaq(g,m,a,steps=4):
  """like gq but to work on a bit more abstract data (defined by m.gaq*)"""
  shape0=g.X.shape
  g.X=glacreate(gs=g.s.gs,a=a,param=g.s.param)([g.A,g.X])
  for d in denseladder(c=2,n=steps,truestart=True)[::-1]:
    g.X=Dense(int(d*g.s.param),activation="linear",kernel_initializer=m.gqa_init_kernel,bias_initializer=m.gqa_init_bias,use_bias=m.gqa_usebias)(g.X)
    if m.gqa_batchnorm:g.X=BatchNormalization()(g.X)
    if m.gqa_activation!="linear":g.X=Activation(m.gqa_activation)(g.X)
  return g

def gnl(g,m,alin=[],iterations=1,repeat=1,usei=False):
  """a function to just add some graph update functionality without relearning the graph, defined by m.graph*. Can use usei to use inverted Graph update layers instead of the normal ones (to make invertibility easier). Also understands alin (iarities) as a vector"""
  if m.shallcomplex:
    return gq(g,m,steps=m.complexsteps)
  if usei:
    g.X=glim(gs=g.s.gs,param=g.s.param,iterations=iterations,alinearity=alin,self_initializer=m.graph_init_self,neig_initializer=m.graph_init_neig)([g.A,g.X])
  else:
    g.X=glm(gs=g.s.gs,param=g.s.param,iterations=iterations,alinearity=alin,self_initializer=m.graph_init_self,neig_initializer=m.graph_init_self)([g.A,g.X])
  if repeat>1:return gnl(g,alin=alin,iterations=iterations,repeat=repeat-1,usei=usei)
  return g
def learngraph(g,free=0,k=4):
  """just learns a graph (g.A) as a function of the parameters (g.X). Can also add new parameters to g.X (with free) and you can specify how many connections each node should have (k), mainly used by gll"""
  mat,feat=gtopk(gs=g.s.gs,param=g.s.param,free=free,flag=flag,self_interaction=self_interaction,k=k)([g.X])
  g.A=mat
  g.s.param+=free
  g.X=feat
  return g
def gll(g,m,free=0,alin=[],iterations=1,repeat=1,subrepeat=1,usei=False,k=4):
  """gnl + learngraph"""
  g=learngraph(g,free=free,k=k)
  g=gnl(g,m,alin=alin,iterations=iterations,repeat=subrepeat,usei=usei)
  if repeat>1:return gll(g,free=free,alin=alin,iterations=iterations,repeat=repeat-1,usei=usei)
  return g

def ganl(A,X,gs,a,param,m,iterations=1,alin=[],usei=False):
  """gnl but on more abstract graphs, should probably not be used directly unless you unstand what the difference is"""
  if not m.shallacomplex:
    if usei:
      return gliam(gs=gs,a=a,param=param,iterations=iterations,alinearity=alin,self_initializer=m.agraph_init_self,neig_initializer=m.agraph_init_neig)([A,X])
    else:
      return glam(gs=gs,a=a,param=param,iterations=iterations,alinearity=alin,self_initializer=m.agraph_init_self,neig_initializer=m.agraph_init_neig)([A,X])
  else:
    ag=grap(state(gs=gs,param=param))
    ag.X=X
    ag.A=A
    ag=gaq(ag,m,a=a,steps=m.complexasteps)
    return ag.X
def abstr(g,c,alin=[],iterations=1,repeat=1,multiglam=1,pmode="max",gmode="mean"):
  """uses (multiglam) glam to abstract a graph into a factor c smaller graph
  uses pooling to go from c size subgraphs to 1 size dots
  does not chance param at all
  uses (pmode) param pooling mode
  uses (gmode) graph pooling mode"""
  graph,feat1=gcomreopool(gs=g.s.gs,param=g.s.param)([g.A,g.X])#reorder by last param
  graphs=gcomdiagraph(gs=g.s.gs,c=c)([graph])#diagonal graphs
  feats1=gcomparastract(gs=g.s.gs,param=g.s.param,c=c)([feat1])#abstract 3d parameters into 4d ones
  g.s.gs=int(g.s.gs/c)
  for i in range(multiglam):feats1=ganl(graphs,feats1,gs=c,a=g.s.gs,param=g.s.param,iterations=iterations,alin=alin)#run sub graph actions
  feat1=gcompoolmerge(gs=g.s.gs,ags=c,param=g.s.param,mode=pmode)([feats1])  
  graph=gcomgraphcutter(gs=g.s.gs*c,c=c,mode=gmode,cut=cut,c_const=c_const)([graph])#goes from big graph to small graph
  g.A=graph
  g.X=feat1
  if repeat>1:return gabstr(g,c,alin=alin,iterations=iterations,repeat=repeat-1,multiglam=multiglam,pmode=pmode,gmode=gmode)
  return g

def compress(g,m,c,addparam):
  """little brother of abstr, the main difference is, that this does not keep any information of the graph, so you have to retrain it, if you want to do graph actions afterwards"""
  g.X=gcompool(gs=g.s.gs,param=g.s.param,paramo=g.s.param+addparam,c=c,metrik_init=m.compression_init)([g.X])
  g.A=None
  g.s.gs=int(g.s.gs/c)
  g.s.param+=addparam
  return g




def graphatbottleneck(g,m,shallfp=True):
  """handles the bottleneck transformations for a pure graph ae, return g, compressed, new input, shallfp=True=>convert vector in matrix (with gfromparam), can use redense to add a couple dense layers around the bottleneck (defined by m.redense*)"""
  comp=ggoparam(gs=g.s.gs,param=g.s.param)([g.X])
  if m.shallredense:
    for e in m.redenseladder:
      comp=Dense(e,activation=m.redenseactivation,kernel_initializer=m.redenseinit)(comp)
    inn2=Input(m.redenseladder[-1])
    use=inn2
    for i in range(len(m.redenseladder)-1,-1,-1):
      use=Dense(m.redenseladder[i],activation=m.redenseactivation,kernel_initializer=m.redenseinit)(use)
    use=Dense(g.s.gs*g.s.param,activation=m.redenseactivation,kernel_initializer=m.redenseinit)(use)
  else:
    inn2=Input(g.s.gs*g.s.param)
    use=inn2

  if shallfp:
    taef1=gfromparam(gs=g.s.gs,param=g.s.param)([use])
  else:
    taef1=inn2
  g.X=taef1
  g.A=None
  return g,comp,inn2


def denseladder(c,n=3,truestart=False):
  """helper function that generates a list of Dense sizes going from 1 to c in n steps (excluding 1 and c), c can be a list, than returns a list of lists"""
  if type(c)==list:
    ret=[]
    for ac in c:
      ret.append(denseladder(ac,n=n,truestart=truestart))
    return ret

  if truestart:n-=1

  ret=[]
  if truestart:ret.append(1)
  fact=1.0
  mul=c**(1/(n+1))
  for i in range(n):
    fact*=mul
    ret.append(fact)
  return ret

def divtriv(g,c,m,shallgp=True,addDense=[[]],activation=None):
  """trivial graph diverger by a factor of c (does not chance param at all)
  requiregp=True: require ggoparam at the start
  addDense: intermediate Dense Layers, sizes between 1 and c useful"""



  param=g.X
  if shallgp:param=ggoparam(gs=g.s.gs,param=g.s.param)([param])
  for d in addDense[0]:param=Dense(int(d*g.s.gs*g.s.param),activation=activation,kernel_initializer=m.trivial_decompress_init_kernel,bias_initializer=m.trivial_decompress_init_bias)(param)
  g.s.gs*=c[0]#actually not completely the same as magic 29, since there was a param mistake
  param=Dense(g.s.gs*g.s.param,activation,kernel_initializer=m.trivial_decompress_init_kernel,bias_initializer=m.trivial_decompress_init_bias)(param)
  g.X=gfromparam(gs=g.s.gs,param=g.s.param)([param])
  c=c[1:]
  if len(addDense)>0:
    addDense=addDense[1:]
  if len(c)>0:
    return divtriv(g,c,shallgp=False,addDense=addDense)
  return g

def divccll(g,c):
  """easy diverger: diverge by copy"""
  g.X=gmultiply(gs=g.s.gs,param=g.s.param,c=c)([g.X])
  g.A=None
  g.s.gs*=c
  return g





def divpar(g,c,usei=False,alin=[],iterations=1,repeat=1,multiglam=1,amode2="prod"):
  """A parameter like graph diverger by a factor of c (also does not chance param at all)"""

  #print("par on",g.A,g.X,g.s.gs,g.s.param,c)
  #exit()

  #amode2 : and operation modus for graphand2
  park0=gcomfullyconnected(gs=g.s.gs,param=g.s.param)([g.X])#generate initial fully connected graph
  taef1s=gcomdensediverge(gs=g.s.gs,param=g.s.param,paramo=g.s.param,c=c)([g.X])#list of param to list of list of param
  park1=gcomparamcombinations(gs=g.s.gs,param=g.s.param)([g.X])#all possible combinations of parameters
  park2=gcomgraphfrom2param(gs=g.s.gs,param=g.s.param,c=c)([park1])#make each combination into a graph
  park4=gcomgraphlevel(gs=g.s.gs,c=c)([park2])#make matrix of graphs into one graph
  park5=gcomgraphrepeat(gs=g.s.gs,c=c)([park0])#better:scale up park0 by replacing each 1/0 by a 1/0 c*c Matrix
  park6=gcomgraphand2(gs=g.s.gs,c=c,mode=amode2)([park4,park5])#merge the graphs (new graphs, with old graph)
  parkd=gcomextractdiag(gs=g.s.gs,c=c)([park2])#extract the needed matrices for glam from the combination generators

  #if usei:
  #  for i in range(multiglam):taef1s=gliam(gs=c,param=g.s.param,a=g.s.gs,alinearity=alin,iterations=iterations)([parkd,taef1s])#does the subnode graph actions
  #else: 
  #  for i in range(multiglam):taef1s=glam(gs=c,param=g.s.param,a=g.s.gs,alinearity=alin,iterations=iterations)([parkd,taef1s])#does the subnode graph actions
  for i in range(multiglam):taef1s=ganl(parkd,taef1s,gs=c,param=g.s.param,a=g.s.gs,alin=alin,iterations=iterations,usei=usei)

  taef2=gcomparamlevel(gs=g.s.gs,c=c,param=g.s.param)([taef1s])
  g.s.gs*=c
  g.X=taef2
  g.A=park6
  if repeat>1:return divpar(g,c,alin=alin,usei=usei,iterations=iterations,repeat=repeat,multiglam=multiglam,amode2=amode2)
  return g

def divcla(g,c,m,repeat=1):
  """classic graph abstractor, also does not chance the paramsize, just goes from one param to c params, and has one learnable matrix (which is const between the elements). Works by usual parameter divergence, and then by abstracting the graphs, with the constant learnable one"""
  feat0,nmat=gcomdepoolplus(gs=g.s.gs,param=g.s.param,paramo=g.s.param,c=c,metrik_init=keras.initializers.Identity())([g.X])
  rmat=ggraphstract(in1=g.s.gs,in2=c)([g.A,nmat])
  g.A=rmat
  g.X=feat0
  g.s.gs*=c
  if repeat>1:return divcla(g,c,repeat=repeat-1)
  return g
def divcla2(g,c,m,repeat=1):
  """even more simple divcla, the main difference is, that this ignores graphs completely"""
  feat0=gcomdepool(gs=g.s.gs,param=g.s.param,paramo=g.s.param,c=c,metrik_init=keras.initializers.Identity())([g.X])
  g.A=None
  g.X=feat0
  g.s.gs*=c
  if repeat>1:return divcla2(g,c,repeat=repeat-1)
  return g

def divgra(g,c,m,usei=False,alin=[],iterations=1,repeat=1,multiglam=1,amode="prod",amode2="prod"):
  """graph like graph diverger by a factor of c (also does not chance param at all)
  amode  : and operation modus for graphand
  amode2 : and operation modus for graphand2"""
  park0=gcomfullyconnected(gs=g.s.gs,param=g.s.param)([g.X])#generate initial fully connected graph
  taef1s=gcomdensediverge(gs=g.s.gs,param=g.s.param,paramo=g.s.param,c=c)([g.X])#list of param to list of list of param  
  park1=gcomgraphfromparam(gs=g.s.gs,param=g.s.param,c=c)([g.X])#generates graphs from sets of params
  park2=gcomgraphcombinations(gs=g.s.gs,c=c)([park1])#build all combinations of these graphs
  park3=gcomgraphand(gs=g.s.gs,c=c,mode=amode)([park2])#combine graphs
  park4=gcomgraphlevel(gs=g.s.gs,c=c)([park3])#make matrix of graphs into one graph
  park5=gcomgraphrepeat(gs=g.s.gs,c=c)([park0])#better:scale up park0 by replacing each 1/0 by a 1/0 c*c Matrix
  park6=gcomgraphand2(gs=g.s.gs,c=c,mode=amode2)([park4,park5])#merge the graphs (new graphs, with old graph)

  #if usei:
  #  for i in range(multiglam):taef1s=gliam(gs=c,param=g.s.param,a=g.s.gs,alinearity=alin,iterations=iterations)([park1,taef1s])#does the subnode graph actions
  #else:
  for i in range(multiglam):taef1s=ganl(park1,taef1s,gs=c,param=g.s.param,a=g.s.gs,alin=alin,iterations=iterations,usei=usei)
  #  for i in range(multiglam):taef1s=glam(gs=c,param=g.s.param,a=g.s.gs,alinearity=alin,iterations=iterations)([park1,taef1s])#does the subnode graph actions
 
  taef2=gcomparamlevel(gs=g.s.gs,c=c,param=g.s.param)([taef1s])
  g.s.gs*=c
  g.X=taef2
  g.A=park6
  if repeat>1:return divgra(g,c,alin=alin,usei=usei,iterations=iterations,repeat=repeat,multiglam=multiglam,amode=amode,amode2=amode2)
  return g



def remparam(g,nparam):
  """just a simple function to remove overdue parameters"""
  g.X=gremoveparam(gs=g.s.gs,inn=g.s.param,out=nparam)([g.X])
  g.s.param=nparam
  return g


def handlereturn(inn1,raw,com,inn2,decom,shallvae):
  """a nice function to simplify returning values for createbothmodels. Also has some simple size consistency checks
  the variables:
  #inn1  :   initial input Variable
  #raw   :   preconverted input Variable, for comparison sake
  #com   :   compressed Variable
  #inn2  :   input for decoder
  #decom :   decompressed decoder Variable
  #shallvae: shall i thread this like a variational auto encoder? hier just a bodge of an solution"""




  
  if not int(inn1.shape[-1])==4:
    print("returning failed at input1 shape",inn1.shape)
    assert False
  if not int(raw.shape[-1])==int(decom.shape[-1]):
    print("returning failed at comparison shape comparison(1) of",raw.shape,"and",decom.shape)
    assert False
  if len(raw.shape)>2:
    if not int(raw.shape[-2])==int(decom.shape[-2]):
      print("returning failed at comparison shape comparison(2) of",raw.shape,"and",decom.shape)
      assert False
  if not int(com.shape[-1])==int(inn2.shape[-1]):
    print("returning failed at compression shape comparison of",com.shape,"and",inn2.shape)
    assert False

  
  c1=com
  c2=com
  
  if shallvae:
    c1=Dense(int(c1.shape[-1]))(c1)
    c2=Dense(int(c2.shape[-1]))(c2)
    for i in range(100):print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("!!!running variational!!!")
    for i in range(100):print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
  return inn1,raw,c1,c2,[],inn2,decom

def sortparam(g,m):
  """sorts X by one of its parameters (m.sortindex), just removes the graph"""
  g.X=gssort(gs=g.s.gs,param=g.s.param,index=m.sortindex)([g.X])
  g.A=None
  return g 


def subedge(inp,param,m):
  """one particlenet like update step, uses m.edge*"""
  feat1=Conv2D(param,(1,1),use_bias=m.edgeusebias)(inp)
  feat2=BatchNormalization()(feat1)
  feat3=Activation(m.edgeactivation)(feat2)
  return feat3

def edgeconv(inp,gs,k,param,m):
  """one set of particlenet like update steps, thus use m.edge* like subedge. also similar to gq (here the main difference is the dense vs convolutional structure"""
  feat0=dtcreate(gs=gs,k=k,param=param,flag=0)([inp])
  for i in range(m.edges):feat0=subedge(feat0,param,m=m)
  qfeat=dtdestroy(gs=gs,k=k,param=param)([feat0])
  outp=Activation(m.edgeactivationfinal)(qfeat)
  return outp

def ge(g,m,k=4):
  """the upper level managing particlenet like update steps (like edgeconv and subedge, can mostly use m.edgeconcat to decide if you should concat or replace the output (concat:like particlenet, replace:probably better for autoencoder)"""
  nw=edgeconv(g.X,g.s.gs,k=k,param=g.s.param,m=m)
  if m.edgeconcat:
    g.X=Concatenate(axis=-1)([g.X,nw])
    g.s.param*=2
  else:
    g.X=nw
  g.A=None
  return g


def shuffleinp(g,seed=None):
  """shuffles the inputs, cross particle...sadly does not keep the shuffle constant"""
  q=ggoparam(gs=g.s.gs,param=g.s.param)([g.X])
  
  q=gshuffle(gs=1,param=g.s.param*g.s.gs,seed=seed)([q])

  g.X=gfromparam(gs=g.s.gs,param=g.s.param)([q])

  return g

def orthoinp(g,seed=None):
  """like shuffleinp, but uses an orthogonal matrix instead of shuffle, thus constant, but mixes the inputs in a certain way"""
  q=ggoparam(gs=g.s.gs,param=g.s.param)([g.X])
  
  q=gortho(gs=1,param=g.s.param*g.s.gs,seed=seed)([q])

  g.X=gfromparam(gs=g.s.gs,param=g.s.param)([q])

  return g

def perminp(g):
  """like orthoinp, but uses an permutation matrix instead of an orthogonal one. migth require some improvements in gperm.py before it becomes truly useful"""
  q=ggoparam(gs=g.s.gs,param=g.s.param)([g.X])
  
  q=gperm(gs=1,param=g.s.param*g.s.gs)([q])

  g.X=gfromparam(gs=g.s.gs,param=g.s.param)([q])

  return g

def pnorm(g):
  """runs a normation on each particle and feature, ignoring the first one"""
  zw,g.X=gcutparam(gs=g.s.gs,param1=1,param2=g.s.param-1)([g.X])
  g.X=gpartinorm(gs=g.s.gs,param=g.s.param-1)([g.X])
  g.X=ghealparam(gs=g.s.gs,param1=1,param2=g.s.param-1)([zw,g.X])
  return g
  
def prevcut(g,ops=4):
  """cuts in gs, takes only the last ops values"""
  g.X=gecutter(inn=g.s.gs,param=g.s.param,out=ops)([g.X])
  g.s.gs=ops
  return g

def goparam(g,chanceS=True):
  """transforms the 3d (-1,gs,param) data into 2d (-1,gs*param) ones. You can use chanceS to disallow this function to chance the settings"""
  g.X=ggoparam(gs=g.s.gs,param=g.s.param)([g.X])
  if chanceS:
    g.s.param=g.s.gs*g.s.param
    g.s.gs=1
  return g





def decompress(g,m,c):
  """function to run diverge algorithms on the input. You can choose the diverge algorithm with m.decompress (trivial, paramlike,graphlike,classic,classiclg,ccll), c can be a list (multiple divergences) and also handles the bottleneck actions (define a new input, and return it later). Always returns: g,compressed version,new input"""
  if type(c)!=list:c=[c]
  if m.decompress=="trivial":
    ###trivial magic29 decompression
    g,com,inn2=graphatbottleneck(g,shallfp=False,m=m)
    for ac in c:g=divtriv(g,m=m,c=ac,shallgp=False,addDense=denseladder(c=ac,n=m.trivial_ladder_n),activation=m.trivial_decompress_activation)
    return g,com,inn2
  if m.decompress=="paramlike":
    ###parameter like decompression
    g,com,inn2=graphatbottleneck(g,m=m)
    for ac in c:
      g=divpar(g,c=ac,usei=m.usei,m=m)
      g=gnl(g,usei=m.usei,m=m)
    return g,com,inn2
  if m.decompress=="graphlike":
    ###graph like decompression
    g,com,inn2=graphatbottleneck(g,m=m)
    for ac in c:
      g=divgra(g,c=ac,usei=m.usei,m=m)
      g=gnl(g,usei=m.usei,m=m)
    return g,com,inn2
  if m.decompress=="classic":
    ###classic decompression algorithm, with one learnable constant graph abstraction
    g,com,inn2=graphatbottleneck(g,m=m)
    g.A=gcomfullyconnected(gs=g.s.gs,param=g.s.param)([g.X])
    for ac in c:
      g=divcla(g,c=ac,m=m)
      g=gnl(g,usei=m.usei,m=m)
    return g,com,inn2
  if m.decompress=="classiclg":
    ###classic decompression algorithm, with learnable graph actions
    g,com,inn2=graphatbottleneck(g,m=m)
    for ac in c:
      g=divcla2(g,c=ac,m=m)
      g=gll(g,usei=m.usei,m=m)
    return g,com,inn2
  if m.decompress=="ccll":
    ###copy copy learn learn decompression algorithm
    g,com,inn2=graphatbottleneck(g,m=m)
    for ac in c:
      g=divccll(g,c=ac,m=m)
      g=gll(g,usei=m.usei,m=m)
    return g,com,inn2













