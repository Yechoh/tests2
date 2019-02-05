from z3 import *
from simple_test_env2 import *
import random
from collections import namedtuple
import matplotlib.pyplot as plt
import itertools
from constants import *


# change these things to your liking:
env = Simple_test_env("RVOsplit1_2")
AREA = (0,100)
SPLITS = 10000
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
        b=random.randrange(0,2)
        if inpart!=0 and outpart!=0:
            if b:
                a=random.randrange(cut1,cut2)
            else:
                c=random.randrange(outpart)
                a=(c+cut2)%AREA[1]
            results.append(a)
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