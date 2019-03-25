from simple_test_env2 import *
import random
import matplotlib.pyplot as plt
from z3 import *

# change these things to your liking:
env = Simple_test_env("truebins2_1")
LOW,HIGH = (20,100)
TESTS = 1000
TEST = True
AMOUNT_OF_BINS = 20
BINS_LOW,BINS_HIGH = (-200,200)
from collections import *


def main():
    if TEST:
        test()
        print("tests done; set TEST to False")
    plot()

#description:
"""
tests TrueBins over an infinite space with a range constraint
"""

#functions
def bins(x):
    binnrs=[random.randrange(BINS_LOW,BINS_HIGH-(AMOUNT_OF_BINS-1)) for _ in range((AMOUNT_OF_BINS-1))]
    for i in range(len(binnrs)):
        binnrs[i]+=i+1
    bins=[x<binnrs[0],x>=binnrs[-1]]
    for i in range(len(binnrs)-1):
        bins.append(And(x>=binnrs[i],x<binnrs[i+1]))
    random.shuffle(bins)
    return Or(bins)

def test():
    results=[]
    x=Int('x')
    for test in range(TESTS):
        print(test)
        s = Solver()
        s.reset()
        s.set('smt.arith.random_initial_value', True)
        s.add(And(x>=LOW,x<HIGH))
        s.add(bins(x))
        s.check()
        #print s
        m = s.model()
        results.append(m[x].as_long())
    env.save("test",results)

def plot():
    data = env.load("test")
    print(Counter(data))
    amounts=[0]*(HIGH-LOW)
    for e in data:
        amounts[e-LOW]+=1
    plt.bar(range(LOW,HIGH), amounts)
    plt.savefig(env.name + "/testplot")
    plt.show()

main()