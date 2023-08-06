import os
from os.path import isfile

fold="layers/"
fold="layerfiles/"

exit()

imps=[]
clas=[]




with open("layers.py","w") as f:

  for q in os.listdir(fold):
    if not isfile(fold+q):continue
    if "_" in q:continue
    if "makeinit.py" in q:continue
    if not ".py" in q:continue
    
    with open(fold+q,"r") as ff:
      ac=ff.read()

      ac1=ac[:ac.find("\nclass ")]
      ac2=ac[ac.find("\nclass "):]
      
      imps.append(ac1)
      clas.append(ac2)

  i={}
  for imp in imps:
    for lin in imp.split("\n"):
      if not lin in i.keys():i[lin]=1.0

  for ii in i.keys():
    if not "import" in ii:continue
    if len(ii)==0:continue
    if ii[0]=="#":continue
    f.write(ii+"\n")


  for ii in i.keys():
    if "import" in ii:continue
    if len(ii)==0:continue
    if ii[0]=="#":continue
    f.write(ii+"\n")

 
 
  for cl in clas:
    f.write(cl+"\n\n\n\n")




