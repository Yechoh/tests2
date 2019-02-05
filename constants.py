from __future__ import print_function
from itertools import tee
import sys

weight=4

def fst(a):
	return a[0]
	
def snd(a):
	return a[1]

def assert_positive_area((low,high)):
    if low<0:
        raise AssertionError("negative area: "+str((low,high)))
    return (low,high)

def assert_nonempty_area((low,high)):
    if low>=high:
        raise "empty area"
    return (low,high)



def debug(expression):
    frame = sys._getframe(1)

    print(expression, '=', repr(eval(expression, frame.f_globals, frame.f_locals)))
	
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


INTBITSIZE=64
CHARBITSIZE=8