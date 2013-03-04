import numpy as np

mat=[[[0 for x in xrange(3)] for x in xrange(288)] for x in xrange(352)]
dct=np.array([[[0 for x in xrange(3)] for x in xrange(8)] for x in xrange(8)])


count=0
i=-1
k=0
with open("/home/parin/Downloads/data/image1.rgb", "rb") as f:
    byte = f.read(1)
    while byte != "":
#        if count==0 or count==352*288 or count==2*352*288:
#            print ord(byte)
        j=count%288
        if j==0:
            i+=1
        i=i%352
        k=int(count/(352*288))
        mat[i][j][k]=ord(byte)
        count+=1
        byte = f.read(1)
f.close()


cos=np.zeros((8,8), float)

pos=(lambda : [(i,j) for i in range(8)
        for j in range(8)])()

for i in pos:
    cos[i]="{0:.2f}".format(np.cos((2*i[1]+1)*np.pi*i[0]/16))
cos=cos.transpose()
print cos

mat_A=np.array(mat)

for i in range(352/8):
    for j in range(288/8):
        block_R=mat_A[i*8:i*8+8,j*8:j*8+8,0].tolist()
        block_G=mat_A[i*8:i*8+8,j*8:j*8+8,1].tolist()
        block_B=mat_A[i*8:i*8+8,j*8:j*8+8,2].tolist()

        r=((np.matrix(block_R)*np.matrix(cos)).transpose())*np.matrix(cos)
        g=((np.matrix(block_G)*np.matrix(cos)).transpose())*np.matrix(cos)
        b=((np.matrix(block_B)*np.matrix(cos)).transpose())*np.matrix(cos)

        dct[i*8:i*8+8,j*8:j*8+8,0]=r.round(2)
        dct[i*8:i*8+8,j*8:j*8+8,1]=g.round(2)
        dct[i*8:i*8+8,j*8:j*8+8,2]=b.round(2)
        print dct[0:8,0:8,0]/32
