from z3 import *
from simple_test_env2 import *
import random
from collections import namedtuple
import matplotlib.pyplot as plt
import itertools
from constants import *
import time


# change these things to your liking:
env = Simple_test_env("RVOsplit2_3")
LOW = 0; HIGH = 100
INRANGES=[(0,100)]
TESTS = 5000
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
        return [[(low,i+low)],[(i+low+1,high)]]
    else:
        [(low1,high1),(low2,high2)]=part
        if i<high1-low1:
            return [[(low1,i+low1)],[(i+low1+1,high1)]]
        else:
            i-=high1-low1
            return [[(low2,i+low2)],[(i+low2+1,high2)]]

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

def test():
    results=[]
    for _ in range(TESTS):
        results.append(RVOsplit())
    env.save("test", results)

def RVOsplit():
    i=random.randrange(0,HIGH-LOW)
    a=i+LOW
    if validsam(a):
        pass#print(("\t", a, 0)); return a
    j=random.randrange(0,HIGH-LOW)
    b=j+LOW
    if validsam(b):
        pass#print(("\t",b,0)); return b
    parts=cutcircle((LOW,HIGH),i,j)
    iters=1
    while(True):
        #print(parts)
        #time.sleep(1)
        parts=[part for part in parts if valid(part)]
        random.shuffle(parts)
        newparts=[]
        for part in parts:
            print(("part",part))
            i,a=middle(part)
            print(("middle",i,a))
            if validsam(a):
                print((a,iters)); return a
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