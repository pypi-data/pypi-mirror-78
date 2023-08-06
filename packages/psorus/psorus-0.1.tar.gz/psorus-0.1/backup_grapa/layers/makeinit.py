import os
from os.path import isfile


with open("__init__.py","w") as f:

  for q in os.listdir("."):
    if not isfile(q):continue
    if "_" in q:continue
    if "makeinit.py" in q:continue
    if not ".py" in q:continue

    q=q.replace(".py","")

    f.write("import grapa.layers."+q+"\n")




print("done")


