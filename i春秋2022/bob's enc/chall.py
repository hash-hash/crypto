from secret import * 
import random

prime =  2141
print len(flag)
flag = map(ord,flag)
flag1 = flag[:21]
flag2 = flag[21:]
row = 64

def add(msg1,msg2):
    return [(x+y)%prime for x,y in zip(msg1,msg2)]

def multi(msg1,msg2):
    out = []
    for l in msg1:
        s = 0
        for x,y in zip(l,msg2):
            s += (x*y)%prime
            s %= prime
        out.append(s)
    return out
def genkey(leng):
    l = [[] for i in range(row)]
    for x in range(row):
        for i in range(leng):
            l[x].append(random.randint(0,511))
    return l

key = genkey(len(flag1))
print key

cipher1 = multi(key,flag1)

print cipher1

cipher2 = multi(key,flag2)

noise = [random.randint(0,6) for i in range(row)]
print add(noise,cipher2)


