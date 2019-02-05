from simple_test_env2 import *
import random
import matplotlib.pyplot as plt
import itertools
from fractions import Fraction

# change these things to your liking:
env = Simple_test_env("dip_in_circlesplit1_1")
TEST=True

# description
"""
tests how many parts and values we need in order to find a dip <1/2n
"""

def main():
    if TEST:
        test()
        print("tests done; set TEST to False")

# functions

def test():
    i=16