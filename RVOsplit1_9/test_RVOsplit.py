from z3 import *
from simple_test_env2 import *
import random
from collections import namedtuple
import matplotlib.pyplot as plt
import itertools
from constants import *


# change these things to your liking:
env = Simple_test_env("RVOsplit1_9")
SPACE = (0,100)
INRANGES=[(30,100)]
SPLITS = 1000
KEEP_SPLITTING=True
TEST = True
NR_CUTS = 8

#splits in two parts
#parts consist out of areas, based on the cuts
#areas consist out of one or two subareas, based on if they contain the edge of the variable space or not
#areas are ranges

def main():
    if TEST:
        test()
        print("tests done; set TEST to False")
    plot()

# functions

def valid(part):
    if part==[]:
        return False
    for area in part:
        for (low,high) in area:
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

def cutat(area,cuts):
    cuts.sort()
    part=[]
    lastcut=0
    for cut in cuts:
        i=cut-lastcut
        if i!=0:
            [left,right]=cutonce(area,i)
            part.append(left)
            area=right
            lastcut=cut
    part[0]+=right
    return part

def cutonce(area,i):
    for sub_i,(low,high) in enumerate(area):
        if i==0:
            return [area[:sub_i],area[sub_i:]]
        if i<high-low:
            left,right=(low,i+low),(i+low,high)
            return [area[:sub_i]+[left],area[sub_i+1:]+[right]]
        i-=(high-low)

def divide(areas):
    random.shuffle(areas)
    return [areas[:len(areas)/2],areas[len(areas)/2:]]

def singleton_ranges(area):
    part=[]
    for (low,high) in area:
        part+=[[(i,i+1)] for i in range(low,high)]
    return part

def test():
    results=[]
    for _ in range(SPLITS):
        newpart=[[SPACE]]
        while(True):
            if len(newpart)==1:
                area=newpart[0]
                if size(area)<=NR_CUTS:
                    if size(area)==1:
                        results.append(at(area, 0))
                        print("chosen",at(area,0))
                        break
                    else:
                        newpart=singleton_ranges(area)
                else:
                    cuts=[random.randrange(1,size(area)) for i in range(NR_CUTS)]
                    newpart=cutat(area,cuts)
            parts=divide(newpart)
            print(parts)
            validparts=[part for part in parts if valid(part)]
            if len(validparts)==1:
                newpart=validparts[0]
            else:
                b=random.randrange(0,2)
                newpart=validparts[b]

    env.save("test",results)

def plot():
    data = env.load("test")
    amounts = [0]*(SPACE[1]-SPACE[0])
    for d in data:
        amounts[d]+=1
    print(amounts)
    plt.bar(range(*SPACE),amounts)
    plt.xlabel("returned value")
    plt.ylabel("amount")
    plt.savefig(env.name + "/testplot")
    plt.show()


main()