# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 10:46:00 2022

@author: Zack
"""
import numpy as np, pandas as pd, matplotlib.pyplot as plt


filename='D:/Users/crawf/Desktop/amorphSiO/endDatav5.csv'

file = pd.read_csv(filename, sep=',', header=None)
data=file.to_numpy(dtype='float')

dims=[15.5,15.5,15.5]

data[:,2:]*=dims

type1=[]
type2=[]

for i in range(0,len(data)):
    if data[i,1]==1:
        type1.append([data[i,2:]])
    elif data[i,1]==2:
        type2.append([data[i,2:]])
type1=np.squeeze(np.array(type1))
type2=np.squeeze(np.array(type2))

def distance(a, b, dims):
    A=dims[0]
    B=dims[1]
    C=dims[2]
    dx = abs(a[0] - b[0])
    x = min(dx, abs(A - dx), abs(A + dx), abs(dx - A))
     
    dy = abs(a[1] - b[1])
    y = min(dy, abs(B - dy), abs(B + dy), abs(dy - B))
     
    dz = abs(a[2] - b[2])
    z = min(dz, abs(C - dz), abs(C + dz), abs(dz - C))
 
    return np.sqrt(x**2 + y**2 + z**2)

def spherevol(r):
    return 4/3*np.pi*r**3


def rdf(data1,data2,dims):
    distlist=[]
    for i in range(0,len(data1)):
        for j in range(0,len(data2)):
            distlist.append(distance(data1[i,:],data2[j,:],dims))
    distlist=np.array(distlist)
    return distlist[distlist!=0]

def g(data):
    y=[]
    x=np.linspace(1,(max(data)+0.01),num=5000)
    data=np.sort(data)
    for i in range(0,len(x)):
        vol=spherevol(x[i])
        count=0
        for j in range(0,len(data)):
            if data[j]<x[i]:
                count+=1
            else:
                break
        y.append(count/vol)
    return x,np.array(y)
'''     
def datanorm(data):
    out=[]
    for i in range(0,len(data)):
        out.append((data[i]/spherevol(data[i])))
    return np.array(out)
'''        


SiSi=rdf(type1,type1,dims)
OO=rdf(type2,type2,dims)
SiO=rdf(type1,type2,dims)

ax,ay=g(SiSi)
bx,by=g(OO)
cx,cy=g(SiO)      


plt.close()
fs=18
plt.plot(ax,ay,label=r'Si-Si, peak at {:.2f}$\AA$'.format(ax[np.argmax(ay)]))
plt.plot(bx,by,label=r'O-O, peak at {:.2f}$\AA$'.format(bx[np.argmax(by)]))
plt.plot(cx,cy,label=r'Si-O, peak at {:.2f}$\AA$'.format(cx[np.argmax(cy)]))
plt.legend(loc='upper right')
plt.xlabel(r'Radius ($\AA$)',fontsize=fs)
plt.ylabel(r'$g(r)$',fontsize=fs)

print('Si-Si max:{:.2f}, O-O max:{:.2f}, Si-O max:{:.2f}'.format(ax[np.argmax(ay)],bx[np.argmax(by)], cx[np.argmax(cy)]))


