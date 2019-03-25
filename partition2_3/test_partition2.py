from z3 import *
from simple_test_env2 import *
import random
import time
from collections import namedtuple
import matplotlib.pyplot as plt
from constants import *

# change these things to your liking
env=Simple_test_env("partition2_3")
AREA=(0,120)
INRANGE=(20,23)
PARTSIZE=10
EXHAUSTIVE = True
TESTS = 100 #only relevant if exhaustive == False
GENERATE= True
TEST = True

# functions

def range_constraint_input():
    env.save("range_constraint_input", INRANGE)

def input():
    if EXHAUSTIVE:
        input_exhaustive()
    else:
        input_mc()

def input_exhaustive():
    env.save("input_exhaustive", [(i,i+PARTSIZE) for i in range(fst(INRANGE)-PARTSIZE+1,snd(INRANGE))])

def input_mc():
    input = []
    for i in range(TESTS):
        low=random.randrange(fst(INRANGE)-PARTSIZE+1,snd(INRANGE))
        input.append((low,low+PARTSIZE))
    env.save("input_mc", input)

def inrange(a, b, var):
    return And(var >= a, var < b)

def get_input(x):
    if EXHAUSTIVE:
        input=env.load("input_exhaustive")
    else:
        input=env.load("input_mc")
    return input,[inrange(low,high, x) for low,high in input]

def get_constraints(x):
    low,high = env.load("range_constraint_input")
    return (low,high), inrange(low,high, x)

def int_partition_test():
    results = []
    x = Int('x')
    constraints, smtconstraints = get_constraints(x)
    parts, smtparts = get_input(x)
    for part, smtpart in zip(parts,smtparts):
        s = Solver()
        s.reset()
        s.set('smt.arith.random_initial_value', True)
        s.add(smtconstraints)
        s.add(smtpart)
        m2 = read_model(s, [("int", "x", x)])
        m2 = m2[0][-1]
        results.append(m2)
    env.save("test",results)

def read_model(s,vars):
    if s.check() == sat:
        m=s.model()
        newvars=[]
        for vtype,vname,var in vars:
            if m[var]==None:
                newvars.append((vtype,vname,None))
            elif vtype=="int":
                newvars.append((vtype,vname,m[var].as_long()))
            elif vtype=="bool":
                newvars.append((vtype,vname,m[var].is_true()))
        return newvars
    else:
        newvars=[]
        for vtype,vname,var in vars:
            newvars.append((vtype,vname,None))
        return newvars

def autolabel(rects):
    offset =  0.5
    for rect in rects[::2]:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()*offset, height,
                '{}'.format(int(height)), ha='center', va='bottom')

def plot():
    data = env.load("test")
    print(data)
    rects=plt.bar(range(fst(INRANGE)-PARTSIZE+1,snd(INRANGE)), data)
    #autolabel(rects)
    plt.xlabel("part index")
    plt.ylabel("returned value")
    plt.savefig(env.name + "/testplot")
    plt.show()

def plot_amounts():
    data = env.load("test")
    amounts=[0]*(INRANGE[1]-INRANGE[0])
    for e in data:
        amounts[e-INRANGE[0]]+=1
    plt.bar(range(*INRANGE),amounts)
    plt.xlabel("value")
    plt.ylabel("number of times returned")
    plt.savefig(env.name + "/testplot_amounts")
    plt.show()

def main():
    if GENERATE:
        range_constraint_input()
        input()
        print("input done; set GENERATE to False")
    if TEST:
        int_partition_test()
        print("tests done; set TEST to False")
    plot()
    plot_amounts()

main()






