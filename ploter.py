import numpy as np
import matplotlib.pyplot as plt
cds=np.load("cd.npy")
spds=np.load("spds.npy")
wins=np.load("wins.npy")
winsact=np.load("winsact.npy")
acks=np.load("acks.npy")
merges = np.load("merges.npy")
bfs = [2**n-1 for n in range(3,6)]
print(sum(acks)/len(acks),sum([bfs[w] for w in wins])/len([bfs[w] for w in wins]),sum(winsact)/len(wins))
if 0:
    plt.figure(1)
    plt.bar([q for q in range(len(wins))],[bfs[w] for w in wins],color='C1',alpha=0.5)
    plt.plot(winsact)
    plt.show()
if 0:
    
    plt.figure(2)
    plt.plot(cds)
    plt.show()
if 0:
    plt.figure(3)
    plt.plot(spds)
    plt.show()
if 1:
    plt.figure(4)
    plt.plot(acks)
    plt.show()
