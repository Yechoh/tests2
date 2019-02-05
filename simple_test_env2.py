import os.path
import json
import sys
from shutil import copyfile

class Simple_test_env:

    def __init__(self,name):
        print(name)
        self.name=name
        if not os.path.exists(name):
            os.makedirs(name)
        pyfolder,pyname=os.path.split(sys.argv[0])
        f=open(pyfolder+"/"+pyname,"r")
        t=f.readlines()
        f=open(pyfolder+"/"+name+"/"+pyname,"w")
        f.writelines(t)

    def save(self,name,data):
        filepath=self.name+"/"+name
        f=open(filepath+".txt","w")
        json.dump(data,f)
        print(name+" saved")
        
    def load(self,name):
        f=open(self.name+"/"+name+".txt","r")
        data=json.load(f)
        print(name+" loaded")
        return data


