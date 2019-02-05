from z3 import *
from simple_test_env2 import *
import random
from collections import namedtuple
import matplotlib.pyplot as plt
import itertools
from constants import *


# change these things to your liking:
env = Simple_test_env("RVOsplit1_1")
AREA = (0,100)
SPLITS = 1000
TEST = True

def main():
    if TEST:
        test()
        print("tests done; set TEST to False")
    plot()

# functions

def test():
    results=[]
    for _ in range(SPLITS):
        cut1=random.randrange(*AREA)
        cut2=random.randrange(*AREA)
        if cut1 > cut2: cut1, cut2 = cut2, cut1
        inpart=cut2-cut1
        outpart=cut1-AREA[0]+AREA[1]-cut2
        results.append((inpart,outpart))
    env.save("test",results)

def plot():
    data = env.load("test")
    inparts,outparts=zip(*data)
    print(inparts)
    print(outparts)
    avgin=sum(inparts)/len(inparts)
    avgout=sum(outparts)/len(outparts)
    print(avgin,avgout)

main()