from z3 import *
from simple_test_env2 import *
import random
from collections import namedtuple
import matplotlib.pyplot as plt
import itertools
from constants import *


# change these things to your liking:
env = Simple_test_env("RVOsplit1_5")
AREA = (0,100)
INRANGES=[(30,100)]
SPLITS = 1000
KEEP_SPLITTING=True
TEST = True


def main():
    if TEST:
        test()
        print("tests done; set TEST to False")
    plot()

# functions

def valid((low,high)):
    for (low2,high2) in INRANGES:
        if low <= high2 and low2 <= high:
            return True
    return False

def test():
    results=[]
    for _ in range(SPLITS):
        newarea=AREA
        while(newarea[1]-newarea[0]!=1):
            cut=random.randrange(newarea[0]+1,newarea[1])
            validareas=[area for area in [(newarea[0],cut),(cut,newarea[1])] if valid(area)]
            if len(validareas)==1:
                newarea=validareas[0]
            else:
                b=random.randrange(0,2)
                newarea=validareas[b]
        results.append(newarea[0])
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