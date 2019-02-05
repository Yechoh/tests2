from simple_test_env2 import *
import random
import matplotlib.pyplot as plt


# change these things to your liking:
env = Simple_test_env("RVOinkspot1_4")
LOW = 0; HIGH = 1000
INRANGES=[(0,5),(45,50)]
TESTS = 100000
TEST = True
validpartcalls=0

def main():
    if TEST:
        test()
        print("tests done; set TEST to False")
    plot()

#description:
"""
used to be optimal only when the rejected sample was in the exact middle of the no solution area. Now when spreading the inkspot, we will spread both sides independently
too many valid(part)-calls. when sampling an invalid in an area, check for each side if there are no sols, and dont check outside of that area.
"""

# functions

def valid(part):
    global validpartcalls
    validpartcalls+=1
    if part==[]:
        return False
    for (low,high) in part:
        if low!=high:
            for (low2,high2) in INRANGES:
                if low <= high2 and low2 <= high:
                    return True
    return False

def validsam(a):
    for (low,high) in INRANGES:
        if low<=a<high:
            return True
    return False

def size(areas):
    size=0
    for (low,high) in areas:
        size+=high-low
    return size

def sample(part):
    j=random.randrange(0,size(part))
    for i,(low,high) in enumerate(part):
        if j < high-low:
            return i,j+low
        j-=high-low

def test():
    results=[]
    for _ in range(TESTS):
        r=RVOinkspot()
        if r is not None:
            results.append(r)
    env.save("test", results)

def find_expart_around(part,i,sam):
    print(("invalid",sam))
    (low,high)=part[i]
    if not valid([(low,sam)]):
        left=low
    else:
        left = 1
        while (not valid([(sam - left, sam + 1)])):
            left = left * 2
            if sam-left<=low:
                break
        left=sam-left/2
    if not valid([(sam,high)]):
        right=high
    else:
        right = 1
        while (not valid([(sam, sam + right + 1)])):
            right = right * 2
            if sam+right+1>=high:
                break
        right=sam+1+right/2
    print((left,right))
    if left==low:
        if right==high:
            del part[i]
        else:
            part[i]=(right,high)
    elif right==high:
        part[i]=(low,left)
    else:
        part[i]=(low,left)
        part.append((right,high))
    return part

def RVOinkspot():
    part=[(LOW,HIGH)]
    while(True):
        print("inranges",part)
        i,sam = sample(part)
        if validsam(sam):
            print(sam)
            return sam
        part=find_expart_around(part,i,sam)

def plot():
    print("validpartcalls",validpartcalls)
    print("av",validpartcalls/TESTS)
    data = env.load("test")
    amounts = [0]*100
    for d in data:
        amounts[d]+=1
    print(amounts)
    plt.bar(range(100),amounts)
    plt.xlabel("returned value")
    plt.ylabel("amount")
    plt.savefig(env.name + "/testplot")
    plt.show()


main()