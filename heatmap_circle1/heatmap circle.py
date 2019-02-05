from simple_test_env2 import *
import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# change these things to your liking:
env=Simple_test_env("heatmap_circle1")
TEST = False
TESTS = 1000000

def main():
    if TEST:
        test()
        print("tests done; set TEST to False")
    plottest()

#description
'''
heatmap of state circle as defined in thesis, when doing RVO rejection sampling
'''

def in_circle(x,y):
    return x*x+y*y<=64*64

def test():
    results=[]
    for i in range(TESTS):
        x=random.randrange(-64,65)
        while True:
            y=random.randrange(-64,65)
            if in_circle(x,y):
                break
        if random.randrange(0,2):
            results.append((x,y))
        else:
            results.append((y,x))
    env.save("test",results)

def plottest():
    import matplotlib.pyplot as plt
    import numpy as np
    data = env.load("test")
    a = [[0 for x in range(129)] for y in range(129)]
    for (x,y) in data:
        a[x+64][y+64]+=1

    # mask some 'bad' data, in your case you would have: data == 0
    a=np.array(a)
    fig, ax = plt.subplots()
    a = np.ma.masked_where(a==0, a)

    cmap = plt.cm.OrRd
    cmap.set_bad(color='black')

    ax.imshow(a, interpolation='none', cmap=cmap)
    plt.axis('off')
    plt.savefig(env.name + "/testplot")
    plt.show()

def plot():
    data = env.load("test")
    a=[[0 for x in range(129)] for y in range(129)]
    for (x,y) in data:
        a[x+64][y+64]+=1
    print(a)
    fig, ax = plt.subplots()
    a=np.ma.masked_where(a==0,a)
    cmap= plt.cm.Greys
    cmap.set_bad(color='red')
    im=ax.imshow([list(range(-64,65)),list(range(-64,65))],a,interpolation=None,cmap=cmap)
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("", rotation=-90, va="bottom")

    '''
    for i in range(129):
        for j in range(129):
            plt.text(j, i, a[i][j],
                           ha="center", va="center", color="w")
    '''


    plt.show()

main()