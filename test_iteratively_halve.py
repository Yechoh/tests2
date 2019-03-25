from z3 import *
from simple_test_env2 import *
import random
from collections import namedtuple
import matplotlib.pyplot as plt
import itertools
from constants import *
import time


# change these things to your liking:
env = Simple_test_env("iteratively_halve1_3")
TESTS = 1000
TEST = True
vars= [Int("a"),Int("b"),Int("c"),Int("d")]
domains=[(0,100),(0,100),(0,100),(0,100)]
constraint=(And(Int("a")>=Int("b")-5,Int("a")<=Int("b")+5,Int("b")>=Int("c")-5,Int("b")<=Int("c")+5,Int("c")>=Int("d")-5,Int("c")<=Int("d")+5))

# description
"""
snake4
"""

def main():
    if TEST:
        test()
        print("tests done; set TEST to False")
    plot()

# functions
rejsams=[0]*TESTS
iters=[0]*TESTS
partchecks=[0]*TESTS
testi=0

def test():
    results=[]
    for i in range(TESTS):
        print(i)
        global testi
        r=iteratively_halve(domains)
        testi += 1
        if r is not None:
            results.append(r)
    env.save("test", results)
    env.save("rejsams",rejsams)
    env.save("iters",iters)
    env.save("partchecks",partchecks)
    print(sum(rejsams)/len(rejsams))
    print(sum(iters) / len(iters))
    print(sum(partchecks) / len(partchecks))

def maybe_find_solution(parts,s):
    for _ in range(10):
    partsizes=[0]*len(parts)
    for i,part in enumerate(parts):
        for (low,high) in part:
            partsizes[i]*=high-low
    sample=[random.randrange(0,size) for size in sizes]
    for i in range(len(sample)):
        for part in parts:
            low,high=part[i]
            if sample[i]<high-low:
                sample[i]=low+sample[i]
                break
            else:
                sample[i]-=high-low
    global rejsams
    rejsams[testi]+=1
    s.push()
    for i,sam in enumerate(sample):
        s.add(vars[i]==sam)
    if s.check()==sat:
        s.pop()
        return sample
    s.pop()
    return None


def partition(part):
    domi=random.randrange(0,len(part))
    low,high=part[domi]
    lowdom=low,(low+(high-low)/2)
    highdom=(low+(high-low)/2),high
    lowpart=copy.deepcopy(part)
    lowpart[domi]=lowdom
    highpart=copy.deepcopy(part)
    highpart[domi]=highdom
    return [lowpart,highpart]

def filter_valid(parts,s):
    global partchecks
    newparts=[]
    for part in parts:
        partchecks[testi]+=1
        s.push()
        for index,(low,high) in enumerate(part):
            s.add(And(vars[index]>=low,vars[index]<high))
        a=s.check()
        if a!=unsat:
            newparts.append(part)
        s.pop()
    return newparts

def iteratively_halve(domains):
    parts=[domains]
    s = Solver()
    s.add(constraint)
    while True:
        global iters
        iters[testi]+=1
        sol=maybe_find_solution(parts,s)
        if sol!=None:
            return sol
        newparts=[]
        for part in parts:
            newparts+=partition(part)
        parts=filter_valid(newparts,s)
        #print(parts)

def plot():
    data = env.load("test")
    amounts = [0]*100
    print(data[0])
    for d in data:
        amounts[d[0]]+=1
    print(amounts)
    plt.bar(range(100),amounts)
    plt.xlabel("solution")
    plt.ylabel("number of times returned")
    plt.savefig(env.name + "/testplot")
    plt.show()


main()