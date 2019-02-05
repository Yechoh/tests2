from z3 import *
from simple_test_env2 import *
import random
from collections import namedtuple
import matplotlib.pyplot as plt
import itertools
from constants import *


# change these things to your liking:
env = Simple_test_env("choice1_2")
AREA = (-100,100)
INRANGE = (37,82)
EXHAUSTIVE = True
SPLITS = 100 #only relevant if exhaustive == False
GREATER=True #only relevant if exhaustive == True
GENERATE = False
TEST = False

# functions

def range_constraint_input():
    env.save("range_constraint_input", INRANGE)

def split_input():
    if EXHAUSTIVE:
        split_input_exhaustive()
    else:
        split_input_mc()

def split_input_exhaustive():
    env.save("split_input_exhaustive", [(i,GREATER) for i in range(*AREA)])

def split_input_mc():
    input = []
    for i in range(SPLITS):
        input.append((random.randrange(AREA),random.randrange(0,2)))
    env.save("split_input_mc", input)

def get_splits(x):
    if EXHAUSTIVE:
        splits=env.load("split_input_exhaustive")
    else:
        splits = env.load("split_input_mc")
    return splits, [x>=nr if b else x<nr for (nr,b) in splits]

def get_constraints(x):
    low, high = env.load("range_constraint_input")
    return (low, high), inrange(low, high, x)

def inrange(a, b, var):
    return And(var >= a, var < b)

def int_choice_test():
    results = []
    x = Int('x')
    constraints, smtconstraints = get_constraints(x)
    splits, smtsplits = get_splits(x)
    for split, smtsplit in zip(splits,smtsplits):
        s = Solver()
        s.reset()
        s.set('smt.arith.random_initial_value', True)
        s.add(smtsplit)
        s.add(smtconstraints)
        m2 = read_model(s, [("int", "x", x)])
        m2 = m2[0][-1]
        results.append(m2)
    env.save("test", results)

def read_model(s, vars):
    if s.check() == sat:
        m = s.model()
        newvars = []
        for vtype, vname, var in vars:
            if m[var] == None:
                newvars.append((vtype, vname, None))
            elif vtype == "int":
                newvars.append((vtype, vname, m[var].as_long()))
            elif vtype == "bool":
                newvars.append((vtype, vname, m[var].is_true()))
        return newvars
    else:
        newvars = []
        for vtype, vname, var in vars:
            newvars.append((vtype, vname, None))
        return newvars	

def crop_nones(l):
    for i in range(len(l)):
        if l[i] is not None:
            break
    l=l[i:]
    for j in reversed(range(len(l))):
        if l[j] is not None:
            break
    l=l[:j+1]
    return l,i,j+1

def plot():
    data = env.load("test")
    data,lowest,length = crop_nones(data)
    print(data)
    plt.bar(range(lowest+AREA[0],lowest+length+AREA[0]),data)
    plt.xlabel("split_number")
    plt.ylabel("returned value")
    plt.savefig(env.name+"/testplot")
    plt.show()

def plot_amounts():
    data = env.load("test")
    data, lowest, length = crop_nones(data)
    amounts=[0]*(INRANGE[1]-INRANGE[0])
    for e in data:
        amounts[e-INRANGE[0]]+=1
    plt.bar(range(INRANGE[0],INRANGE[1]),amounts)
    plt.savefig(env.name + "/testplot_amounts")
    plt.show()

def main():
    if GENERATE:
        range_constraint_input()
        split_input()
        print("input done; set GENERATE to False")
    if TEST:
        int_choice_test()
        print("tests done; set TEST to False")
    #plot()
    plot_amounts()

main()