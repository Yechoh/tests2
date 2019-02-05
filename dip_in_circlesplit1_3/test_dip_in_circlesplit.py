from simple_test_env2 import *
import random
import matplotlib.pyplot as plt
import itertools
from fractions import Fraction
from constants import *

# change these things to your liking:
env = Simple_test_env("dip_in_circlesplit1_3")
TEST=True

# description
"""
tests how many parts and values we need in order to find a dip <1/2n
now when we keep circlesplitting instead of splitting
"""

def main():
    if TEST:
        test()
        print("tests done; set TEST to False")

# functions

def sym_rot_cart_prod(l):
    if l==():
        return [[0,0],[0,1],[1,1]]
    new=[]
    for i in range(len(l)):
        for j in range(i,len(l)):
            new.append(l[i]+l[j])
    return new

def test():
    results=[]
    logparts=1
    cart=()
    while(True):
        cart=sym_rot_cart_prod(cart)
        for parts in cart[:-1]:
            if any(parts):
                totalodds=[Fraction(part) for part in parts]
                totalodds,_=circlesplit(parts,totalodds)
                n_vars=sum(parts)
                results.append([(o.numerator,o.denominator) for o in totalodds])
                for i in range(len(totalodds)):
                    if parts[i] and totalodds[i]<Fraction(1,2*n_vars):
                        print("done")
                        print(parts)
                        print(totalodds,i)
                        env.save("test", results)
                        return
        logparts+=1

lib={}
libi=0

def rotate(l,i):
    return l[i:]+l[:i]

def sym_rot(l):
    max_len=0
    max_len_index=0
    i=0
    while i<len(l):
        for j in range(len(l)):
            if not l[(i+j)%len(l)]:
                break
        i+=j+1
        if j>max_len:
            max_len=j
            max_len_index=i-1
    return tuple(rotate(l,max_len_index))


def circlesplit(ourparts,ourodds,otherparts=[],otherodds=[]):
    global lib,libi
    if len(ourparts)==1:
        return (ourodds,otherodds)
    c=sum(ourparts)
    if c==0:
        return (ourodds,otherodds)
    for i in range(len(otherodds)):
        if otherparts[i]:
            otherodds[i]/=2
    sr_part=sym_rot(ourparts)
    if sr_part in lib:
        totalodds=lib[sr_part]
    else:
        half=len(ourparts)/2
        totalodds = [Fraction(0, 1)] * len(ourparts)
        for spliti in range(0, half):
            low = spliti
            high = spliti + half
            (lefto,righto)=([Fraction(1,1)]*half,[Fraction(1,1)]*half)
            (leftp,rightp)=(ourparts[low:high],ourparts[:low]+ourparts[high:])
            (lefto,righto)=circlesplit(leftp,lefto,rightp,righto)
            (righto,lefto)=circlesplit(rightp,righto,leftp,lefto)
            for i in range(half):
                totalodds[low+i] += lefto[i]
            for i in range(low):
                totalodds[i] += righto[i]
            for i in range(len(ourparts)-high):
                totalodds[high+i] += righto[low+i]
        totalodds = [odd / half for odd in totalodds]
        lib[sr_part]=totalodds
        libi=(libi+1)%60
        if libi==0:
            print(len(lib))
            print(len(ourparts))
            print(ourparts)
    totalodds=[odd*ourodd for odd,ourodd in zip(totalodds,ourodds)]
    return totalodds,otherodds

main()