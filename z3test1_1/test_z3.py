from simple_test_env2 import *
import matplotlib.pyplot as plt
from z3 import *
from collections import *

# change these things to your liking:
env = Simple_test_env("z3test1_1")
TESTS = 100
TEST = True

def main():
    if TEST:
        test()
        print("tests done; set TEST to False")
    plot()

#description:
"""
asks Z3 an integer value with no constraints
"""

#functions
def test():
    results=[]
    x=Int('x')
    #y = Int('y')
    for test in range(TESTS):
        s = Solver()
        s.reset()
        s.set('smt.arith.random_initial_value', True)
        s.add(And(x>=20,x<100))
        s.check()
        m = s.model()
        results.append(m[x].as_long())
    env.save("test",results)

def plot():
    data = env.load("test")
    print(Counter(data))

main()