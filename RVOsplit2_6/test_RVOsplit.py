from z3 import *
from simple_test_env2 import *
import random
from collections import namedtuple
import matplotlib.pyplot as plt
import itertools
from constants import *
import time


# change these things to your liking:
env = Simple_test_env("RVOsplit2_6")
LOW = 0; HIGH = 100
INRANGES=[(30,100)]#[(0,5),(40,45)]
TESTS = 10000
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

def cutcircle(area,i,j):
    if i>j: i,j=j,i
    [left1,right1]=cutat([area],i)
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
            return [[(low1,i+low1)],[(i+low1,high1)]]
        else:
            i-=high1-low1
            return [[(low2,i+low2)],[(i+low2,high2)]]

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
            i-=high1-low1
            return i,i+low2

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
            i-=high1-low1
            return i,i+low2

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
    parts=cutcircle((LOW,HIGH),i,j)
    iters=1
    while(True):
        parts=[part for part in parts if valid(part)]
        #time.sleep(0.1)
        #print(parts)
        random.shuffle(parts)
        newparts=[]
        for part in parts:
            i,a=sample(part)
            if validsam(a):
                print((a,iters)); return a
            i,a=middle(part)
            newparts+=cutat(part,i)
        iters+=1
        parts=newparts


def plot():
    data = env.load("test")
    amounts = [0]*(HIGH-LOW)
    for d in data:
        amounts[d]+=1
    print(amounts)
    plt.bar(range(LOW,HIGH),amounts)
    plt.xlabel("returned value")
    plt.ylabel("amount")
    plt.savefig(env.name + "/testplot")
    plt.show()


main()