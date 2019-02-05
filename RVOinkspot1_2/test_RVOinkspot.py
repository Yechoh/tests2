from simple_test_env2 import *
import random
import matplotlib.pyplot as plt


# change these things to your liking:
env = Simple_test_env("RVOinkspot1_2")
LOW = 0; HIGH = 1000
INRANGES=[(0,5),(45,50)]
TESTS = 10000
TEST = True

def main():
    if TEST:
        test()
        print("tests done; set TEST to False")
    plot()

# functions

def valid(part):
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
    i=random.randrange(0,size(part))
    j=i
    for (low,high) in part:
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

def in_circle(low,high):
    part=[]
    if low<LOW:
        part.append((low%(HIGH-LOW),HIGH))
        low=LOW
    if high>HIGH:
        part+=[(low,HIGH),(LOW,high%(HIGH-LOW))]
    else:
        part+=[(low,high)]
    return part


def find_expart_around(sam):
    i=1
    while(True):
        print(in_circle(sam-i,sam+i+1))
        if valid(in_circle(sam-i,sam+i+1)):
            return in_circle(sam-i/2,sam+i/2+1)
        i=i*2

def inranges(part,expart):
    for (low,high) in expart:
        newpart=[]
        for i,(low2,high2) in enumerate(part):
            if low <= high2 and low2 <= high:
                if low <= low2 <= high <= high2:
                    newpart.append((high,high2))
                elif low2 <= low <= high <= high2:
                    newpart.append((low2,low))
                    newpart.append((high,high2))
                elif low2 <= low <= high2 <= high:
                    newpart.append((low2,low))
            else:
                newpart.append((low2, high2))
        part=newpart
    return part

def RVOinkspot():
    part=[(LOW,HIGH)]
    while(True):
        print("inranges",part)
        i,sam = sample(part)
        if validsam(sam):
            print(sam)
            return sam
        expart=find_expart_around(sam)
        part=inranges(part,expart)

def plot():
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