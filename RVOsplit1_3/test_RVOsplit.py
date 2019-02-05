from z3 import *
from simple_test_env2 import *
import random
from collections import namedtuple
import matplotlib.pyplot as plt
import itertools
from constants import *


# change these things to your liking:
env = Simple_test_env("RVOsplit1_3")
AREA = (0,100)
SPLITS = 1000
KEEP_SPLITTING=False
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
        cut=random.randrange(AREA[0]+1,AREA[1])
        b=random.randrange(0,2)
        if b:
            a=random.randrange(AREA[0],cut)
        else:
            a=random.randrange(cut,AREA[1])
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