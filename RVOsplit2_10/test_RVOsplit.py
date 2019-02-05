from z3 import *
from simple_test_env2 import *
import random
from collections import namedtuple
import matplotlib.pyplot as plt
import itertools
from constants import *
import time


# change these things to your liking:
env = Simple_test_env("RVOsplit2_10")
LOW = 0; HIGH = 100
INRANGES=[(0,5),(45,50)]
TESTS = 100000
KEEP_SPLITTING=True
TEST = True

def main():
    if TEST:
        test()
        print("tests done; set TEST to False")
    plot()

# functions

def valid(part):
    if part==[]:
        return False
    for (low,high) in part:
        if low!=high:
            for (low2,high2) in INRANGES:
                if low <= high2 and low2 <= high:
                    return True
    return False

def validsam(a):
    for (low,high) in INRANGES:
        if low<=a<high:
            return True
    return False

def cutcircle(part,i,j):
    if i>j: i,j=j,i
    [left1,right1]=cutat(part,i)
    [left2,right2]=cutat(right1,j-i)
    return [right2+left1,left2]

def cutat(part,i):
    #print((part,i))
    if len(part)==1:
        [(low,high)]=part
        return [[(low,i+low)],[(i+low,high)]]
    else:
        [(low1,high1),(low2,high2)]=part
        if i<high1-low1:
            return [[(low1,i+low1)],[(i+low1,high1),(low2,high2)]]
        else:
            i-=high1-low1
            return [[(low1,high1),(low2,i+low2)],[(i+low2,high2)]]

def middle(part):
    if len(part)==1:
        [(low, high)] = part
        i=(high-low)/2
        return i,i+low
    else:
        [(low1, high1), (low2, high2)] = part
        i=(high1-low1+high2-low2)/2
        if i<high1-low1:
            return i,i+low1
        else:
            return i,i-high1+low1+low2

def sample(part):
    if len(part)==1:
        [(low, high)] = part
        i=random.randrange(0,high-low)
        return i,i+low
    else:
        [(low1, high1), (low2, high2)] = part
        i=random.randrange(0,high1-low1+high2-low2)
        if i<high1-low1:
            return i,i+low1
        else:
            return i,i-high1+low1+low2

def test():
    results=[]
    for _ in range(TESTS):
        r=RVOsplit()
        if r is not None:
            results.append(r)
    env.save("test", results)

def RVOsplit():
    sam=random.randrange(LOW,HIGH)
    if validsam(sam):
        pass#print((sam, 0)); return sam
    i=random.randrange(0,HIGH-LOW)
    j=(i+(HIGH-LOW)/2)%(HIGH-LOW)
    parts=cutcircle([(LOW,HIGH)],i,j)
    iters=1
    return keep_splitting(parts,iters,True)

def double(part,iters):
    if iters==1:
        return [(LOW,HIGH)]
    if len(part)==1:
        newpart = []
        [(low,high)]=part
        halfsize=(high-low)/2
        newlow=low-halfsize
        if newlow<LOW:
            newpart.append((newlow+HIGH-LOW,HIGH))
            newlow=LOW
        newhigh=high+halfsize
        if newhigh>HIGH:
            newpart.append((newlow,HIGH))
            newpart.append((LOW,newhigh-HIGH+LOW))
        else:
            newpart.append((newlow,newhigh))
        return newpart
    else:
        [(low1, high1), (low2, high2)] = part
        halfsize = (high1 - low1 + high2 - low2) / 2
        newlow=low1-halfsize
        newhigh=high2+halfsize
        return [(newlow,high1),(low2,newhigh)]

def opposite(part,i):
    if len(part)==1:
        [(low,high)]=part
        return (i+(high-low)/2)%(high-low)
    else:
        [(low1, high1), (low2, high2)] = part
        size = (high1 - low1 + high2 - low2)
        return (i+size/2)%size

def keep_splitting(parts,iters,again):
    while(True):
        parts=[part for part in parts if valid(part)]
        random.shuffle(parts)
        newparts=[]
        for part in parts:
            i,a=sample(part)
            if validsam(a):
                if not again:
                    print("got m")
                    print part
                    print((a,iters)); return a
                else:
                    print("again")
                    print(part)
                    newpart=double(part,iters)
                    print(newpart)
                    i,a=sample(newpart)
                    if validsam(a):
                        print((a, iters,1)); return a
                    i, a = sample(newpart)
                    if validsam(a):
                        print((a, iters, 2));return a
                    return keep_splitting([newpart],iters+1,True)
            i,a=middle(part)
            #print(i)
            newparts+=cutat(part,i)
        iters+=1
        parts=newparts


def plot():
    data = env.load("test")
    amounts = [0]*100
    for d in data:
        amounts[d]+=1
    print(amounts)
    plt.bar(range(100),amounts)
    plt.xlabel("returned value")
    plt.ylabel("amount")
    plt.savefig(env.name + "/testplot")
    plt.show()


main()