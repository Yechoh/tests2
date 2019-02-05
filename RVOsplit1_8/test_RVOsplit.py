from z3 import *
from simple_test_env2 import *
import random
from collections import namedtuple
import matplotlib.pyplot as plt
import itertools
from constants import *


# change these things to your liking:
env = Simple_test_env("RVOsplit1_8")
AREA = (0,100)
INRANGES=[(0,100)]
SPLITS = 10000
KEEP_SPLITTING=True
TEST = True


def main():
    if TEST:
        test()
        print("tests done; set TEST to False")
    plot()

# functions

def valid(areas):
    for (low,high) in areas:
        if low!=high:
            for (low2,high2) in INRANGES:
                if low <= high2 and low2 <= high:
                    return True
    return False

def size(areas):
    size=0
    for (low,high) in areas:
        size+=high-low
    return size

def at(areas,i):
    for (low,high) in areas:
        if i<(high-low):
            return i+low
        else:
            i-=(high-low)

def cutat(areas,i,j):
    if i>j: j,i=i,j
    [left1,right1]=cutonce(areas,i)
    if i==j:
        return [left1,right1]
    else:
        [left2,right2]=cutonce(right1,j-i)
        return [left2,stitch(left1,right2)]

def stitch(part1,part2):
    return part1+part2

def cutonce(part,i):
    #print(size(part))
    for area_i,(low,high) in enumerate(part):
        if i==0:
            return [part[:area_i],part[area_i:]]
        if i<high-low:
            left,right=(low,i+low),(i+low,high)
            return [part[:area_i]+[left],part[area_i+1:]+[right]]
        i-=(high-low)

def test():
    results=[]
    for _ in range(SPLITS):
        newpart=[AREA]
        while(size(newpart)!=1):
            cut1=random.randrange(1,size(newpart))
            cut2=random.randrange(1,size(newpart))
            validparts=[part for part in cutat(newpart,cut1,cut2) if valid(part)]
            if len(validparts)==1:
                newpart=validparts[0]
            else:
                b=random.randrange(0,2)
                newpart=validparts[b]
            print(newpart)
            print(size(newpart))
        results.append(at(newpart,0))
    env.save("test",results)

def plot():
    data = env.load("test")
    amounts = [0]*(AREA[1]-AREA[0])
    for d in data:
        amounts[d]+=1
    print(amounts)
    plt.bar(range(*AREA),amounts)
    plt.xlabel("returned value")
    plt.ylabel("amount")
    plt.savefig(env.name + "/testplot")
    plt.show()


main()