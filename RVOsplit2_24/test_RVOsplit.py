from z3 import *
from simple_test_env2 import *
import random
from collections import namedtuple
import matplotlib.pyplot as plt
import itertools
from constants import *
import time


# change these things to your liking:
env = Simple_test_env("RVOsplit2_24")
LOW = 0; HIGH = 100
INRANGES=[(0,5),(45,50)]
TESTS = 100000
KEEP_SPLITTING=True
TEST = True
validpartcalls=0

# description
"""
optimized to reduce valid(part) calls
new inranges
"""

def main():
    if TEST:
        test()
        print("tests done; set TEST to False")
    plot()

# functions

def valid(part):
    global validpartcalls
    validpartcalls += 1
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
        print((sam, 0)); return sam
    i=random.randrange(0,HIGH-LOW)
    j=(i+(HIGH-LOW)/2)%(HIGH-LOW)
    parts=cutcircle((LOW,HIGH),i,j)
    iters=1
    while(True):
        parts=[part for part in parts if valid(part)]
        random.shuffle(parts)
        newparts=[]
        for part in parts:
            i,a=sample(part)
            if validsam(a):
                print((a,iters)); return a
        for part in parts:
            i,a=middle(part)
            newparts+=cutat(part,i)
        iters+=1
        parts=newparts


def plot():
    print("validpartcalls", validpartcalls)
    print("av", validpartcalls / TESTS)
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