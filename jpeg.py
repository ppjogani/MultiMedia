# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 12:37:14 2013

@author: parin
"""
import numpy as np
import pylab as pl
import sys as s
#import matplotlib.pyplot as plt


def calc_idct(dct, cos, idct, choice):
   for i in range(352/8):
    for j in range(288/8):
        block_R=np.mat(dct[i*8:i*8+8,j*8:j*8+8,0])
        block_G=np.mat(dct[i*8:i*8+8,j*8:j*8+8,1])
        block_B=np.mat(dct[i*8:i*8+8,j*8:j*8+8,2])
        
        block_R[:,0]=block_R[:,0]/1.414
        block_G[:,0]=block_G[:,0]/1.414
        block_B[:,0]=block_B[:,0]/1.414
        block_R[0,:]=block_R[0,:]/1.414
        block_G[0,:]=block_G[0,:]/1.414
        block_B[0,:]=block_B[0,:]/1.414
        
        r=(((block_R*cos).transpose())*cos)/4
        g=(((block_G*cos).transpose())*cos)/4
        b=(((block_B*cos).transpose())*cos)/4
                
        idct[i*8:i*8+8,j*8:j*8+8,0]=r.round(2)
        idct[i*8:i*8+8,j*8:j*8+8,1]=g.round(2)
        idct[i*8:i*8+8,j*8:j*8+8,2]=b.round(2)
        
        if choice=='1':
            display(idct)
            pl.pause(arg[1]/1000+0.0000001)
   return idct
    
def display( idct):
    idct_new=np.array(idct.transpose([1,0,2]))
    idct=np.uint8(np.abs(idct_new))
    pl.clf()
    pl.subplot(1,2, 1)
    pl.title('original image')
    pl.imshow(mat_new.transpose([1,2,0]))
    pl.subplot(1,2, 2)
    pl.title('scaled image')
    pl.imshow(idct)

   
a = {
    '1': 'baseline',
    '2': 'progres',
    '3': 'progressive delivery using successive bit approximation'
    }


print 'Number of arguments:', len(s.argv),
print 'image to compress: ', s.argv[1]
print 'quantization level: ', s.argv[2]
print type(s.argv[3])
print 'Delivery mode--', s.argv[3]
print 'latency: ', s.argv[4]
arg=map(float, s.argv[3:])

#mat=[[[0 for x in xrange(3)] for x in xrange(288)] for x in xrange(352)]
dct=np.array([[[0 for x in xrange(3)] for x in xrange(288)] for x in xrange(352)])
idct=np.array([[[0 for x in xrange(3)] for x in xrange(288)] for x in xrange(352)])

mat1=np.zeros(352*288*3)
ix=0
with open("/home/parin/Downloads/data/"+s.argv[1], "rb") as f:
    byte = f.read(1)
    while byte != "":
        mat1[ix]=ord(byte)
        ix=ix+1
        byte = f.read(1)
f.close()
mat_new=np.reshape(np.uint8(mat1),[3,288,352])
mat_A=np.array(mat_new.transpose([2,1,0]))

cos=np.zeros((8,8), float)
pos=(lambda : [(i,j) for i in range(8)
        for j in range(8)])()
for i in pos:
    cos[i]="{0:.6f}".format(np.cos((2*i[1]+1)*np.pi*i[0]/16))
cos=np.mat(cos.transpose())


for i in range(352/8):
    for j in range(288/8):
        block_R=np.mat(mat_A[i*8:i*8+8,j*8:j*8+8,0])
        block_G=np.mat(mat_A[i*8:i*8+8,j*8:j*8+8,1])
        block_B=np.mat(mat_A[i*8:i*8+8,j*8:j*8+8,2])

        r=(((block_R*cos).transpose())*cos)/4
        g=(((block_G*cos).transpose())*cos)/4
        b=(((block_B*cos).transpose())*cos)/4
        
        r[:,0]=r[:,0]/1.414
        g[:,0]=g[:,0]/1.414
        b[:,0]=b[:,0]/1.414
        r[0,:]=r[0,:]/1.414
        g[0,:]=g[0,:]/1.414
        b[0,:]=b[0,:]/1.414
        
        dct[i*8:i*8+8,j*8:j*8+8,0]=r.round(2)
        dct[i*8:i*8+8,j*8:j*8+8,1]=g.round(2)
        dct[i*8:i*8+8,j*8:j*8+8,2]=b.round(2)
#        print dct[i*8:i*8+8,j*8:j*8+8,0]/32
##########idct###############
new_dct=np.array([[[0 for x in xrange(3)] for x in xrange(288)] for x in xrange(352)])
test_dct=np.array([[[0 for x in xrange(3)] for x in xrange(288)] for x in xrange(352)])
a=0
b=128
new_dct=(np.array([[[0 for x in xrange(3)] for x in xrange(288)] for x in xrange(352)]))
idct=new_dct.copy()

cos=cos.transpose()

if s.argv[3]=='1':
    calc_idct(dct,cos,idct, s.argv[3])

elif s.argv[3]=='2':
    for i in range(8):
        for j in range(8):
            for k in range(352/8):
                for l in range(288/8):
                    new_dct[k*8:k*8+i,l*8:l*8+j,0]=dct[k*8:k*8+i,l*8:l*8+j,0]
                    new_dct[k*8:k*8+i,l*8:l*8+j,1]=dct[k*8:k*8+i,l*8:l*8+j,1]
                    new_dct[k*8:k*8+i,l*8:l*8+j,2]=dct[k*8:k*8+i,l*8:l*8+j,2]
            a=calc_idct(new_dct,cos,idct, s.argv[3])
            display(a)
            pl.pause(arg[1]/1000+0.0000001)
            print np.count_nonzero(a)
elif s.argv[3]=='3':
    for i in range(8):
        a=a+b
        b=(b>>1)
        test_dct.fill(a)
        print a
        display(calc_idct(np.bitwise_and(dct,test_dct),cos,idct, s.argv[3]))
        pl.pause(arg[1]/1000+0.0000001)
