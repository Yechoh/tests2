from simple_test_env2 import *
import random
import matplotlib.pyplot as plt


# change these things to your liking:
env = Simple_test_env("RVOinkspot1_1")
LOW = 0; HIGH = 100
INRANGES=[(30,100)]
TESTS = 100000
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

def cutcircle(area,i,j):
    if i>j: i,j=j,i
    [left1,right1]=cutat([area],i)
    [left2,right2]=cutat(right1,j-i)
    return [right2+left1,left2]

def cutat(part,i):
    #print((part,i))
    if len(part)==1:
        [(low,high)]=part
        return [[(low,i+low)],[(i+low,high)]]
    else:
        [(low1,high1),(low2,high2)]=part
        if i<high1-low1:
            return [[(low1,i+low1)],[(i+low1,high1),(low2,high2)]]
        else:
            i-=high1-low1
            return [[(low1,high1),(low2,i+low2)],[(i+low2,high2)]]

def middle(part):
    if len(part)==1:
        [(low, high)] = part
        i=(high-low)/2
        return i,i+low
    else:
        [(low1, high1), (low2, high2)] = part
        i=(high1-low1+high2-low2)/2
        if i<high1-low1:
            return i,i+low1
        else:
            return i,i-high1+low1+low2

def sample(part):
    if len(part)==1:
        [(low, high)] = part
        i=random.randrange(0,high-low)
        return i,i+low
    else:
        [(low1, high1), (low2, high2)] = part
        i=random.randrange(0,high1-low1+high2-low2)
        if i<high1-low1:
            return i,i+low1
        else:
            return i,i-high1+low1+low2

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
        part.append((high,low%(HIGH-LOW)))
        low=LOW
    if high>HIGH:
        part+=[(low,HIGH),(HIGH,high%(HIGH-LOW))]
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
        for i,(low2,high2) in enumerate(part):
            if low2 <= low <= high <= high2:
                part[i]=(low2,low)
                part.append((high,high2))
                break
            if low2 <= high <= high2:
                part[i]=(high,high2)
            if low2 <= low <= high2:
                part[i]=(low2,low)
    return part

def RVOinkspot():
    part=[(LOW,HIGH)]
    while(True):
        i,sam = sample(part)
        print(sam)
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