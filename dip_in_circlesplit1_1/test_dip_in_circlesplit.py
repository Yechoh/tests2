from simple_test_env2 import *
import random
import matplotlib.pyplot as plt
import itertools
from fractions import Fraction
from constants import *

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
        #circlesplit([1,1],[Fraction(1, 1), Fraction(1, 1)],0,1)
        print("tests done; set TEST to False")

# functions

def test():
    results=[]
    logparts=2
    while(True):
        cart=itertools.product(range(2),repeat=2**logparts)
        for parts in cart:
            if any(parts):
                totalodds=[Fraction(0,1)]*(2**logparts)
                for spliti in range(0,2**(logparts-1)):
                    odds=[Fraction(1,1)]*(2**logparts)
                    low=spliti
                    high=spliti + 2 ** (logparts - 1)
                    odds=circlesplit(parts,odds,low,high)
                    for i in range(len(totalodds)):
                        totalodds[i]+=odds[i]
                n_vars=sum(parts)
                totalodds=[odd/(2**(logparts-1)) for odd in totalodds]
                results.append(totalodds)
                print(parts,totalodds)
                for i in range(len(totalodds)):
                    if totalodds[i]<Fraction(1,2*n_vars):
                        print("done")
                        print(totalodds,i)
                        env.save("test", results)
                        return
        logparts+=1

def circlesplit(parts,odds,low,high):
    c=sum(parts[low:high])
    if c!=0:
        for i in itertools.chain(range(0,low),range(high,len(parts))):
            if parts[i]:
                odds[i]/=2
        middle=(high-low)/2
        newodds=split(parts[low:high],odds[low:high],middle)
        for i in range(high-low):
            odds[low+i]=newodds[i]
    c=sum(parts[:low]+parts[high:])
    if c!=0:
        for i in range(low,high):
            if parts[i]:
                odds[i]/=2
        middle=(low+len(parts)-high)/2
        newodds=split(parts[:low]+parts[high:],odds[:low]+odds[high:],middle)
        for i in range(low):
            odds[i]=newodds[i]
        for i in range(len(parts)-high):
            odds[high+i]=newodds[low+i]
    return odds

def split(parts,odds,spliti):
    if len(parts)>1:
        c=sum(parts[:spliti])
        if c!=0:
            for i in range(spliti,len(parts)):
                if parts[i]:
                    odds[i]/=2
            middle=spliti/2
            newodds=split(parts[:spliti],odds[:spliti],middle)
            for i in range(spliti):
                odds[i]=newodds[i]
        c=sum(parts[spliti:])
        if c!=0:
            for i in range(spliti):
                if parts[i]:
                    odds[i]/=2
            middle=spliti/2
            newodds=split(parts[spliti:],odds[spliti:],middle)
            for i in range(spliti):
                odds[spliti+i]=newodds[i]
    return odds

main()