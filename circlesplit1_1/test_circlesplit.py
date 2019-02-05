from z3 import *
from simple_test_env2 import *
import random
from collections import namedtuple
import matplotlib.pyplot as plt
import itertools
from constants import *
import time


# change these things to your liking:
env = Simple_test_env("circlesplit1_1")
LOW = 0; HIGH = 1024
VALID=[1,2,3,9,512]
TESTS = 1000
TEST = True

# description
"""
circlesplit
"""

def main():
    if TEST:
        test()
        print("tests done; set TEST to False")
    plot()

# functions

def test():
    results=[]
    for _ in range(TESTS):
        space=[]
        for i in range(1024):
            space.append([i,0])
        for i in VALID:
            space[i][1]=1
        results.append(circlesplit(space))
    env.save("test", results)

def circlesplit(space):
    sam=random.randrange(0,len(space))
    if space[sam][1]:
        return space[sam][0]
    low=random.randrange(0,len(space)/2)
    high=low+len(space)/2
    (left,right)=(space[low:high],space[:low]+space[high:])
    b=random.randrange(0,2)
    if b:
        if any([a[1] for a in left]):
            r=circlesplit(left)
            return r
        else:
            r=circlesplit(right)
            return r
    else:
        if any([a[1] for a in right]):
            r=circlesplit(right)
            return r
        else:
            r = circlesplit(left)
            return r

def plot():
    data = env.load("test")
    amounts = [0]*1024
    for d in data:
        amounts[d]+=1
    print(amounts)
    plt.bar(range(1024),amounts)
    plt.xlabel("returned value")
    plt.ylabel("amount")
    plt.savefig(env.name + "/testplot")
    plt.show()


main()