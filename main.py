import numpy as np
import random

xno = 2
N = 6
bits = 5
S = np.zeros((N,(xno*bits)))
for i in range(N):
    for j in range((xno*bits)):
        S[i][j]=random.randint(0,1)

limit=np.zeros((xno,2))

limit[0][0]=float(input("Enter the maximum limit of variable x1 :"))
limit[0][1]=float(input("Enter the minimum limit of variable x1 :"))
limit[1][0]=float(input("Enter the maximum limit of variable x2 :"))
limit[1][1]=float(input("Enter the minimum limit of variable x2 :"))
crossProb = float(input("Enter the cross over probability in fraction round off to 2 decimal place :"))
n= int(input("Do you want to use Elitism in the solution generation?\n If NO enter value as zero\n If YES enter an even integer between 0 to 6 :"))
mutProb = float(input("Enter the mutation probability in fraction round off to 2 decimal place :"))
genlimit=int(input("Number of generations to be exectuted for :"))

gen=0

children=np.zeros((N,(xno*bits)))
children[:,:]=S[:,:]

while(gen<genlimit):
    S[:,:] = children[:,:]
    def fun(x1,x2):
        z=x1 +x2 -2*(x1**2) - x2**2 + x1*x2
        return z


    x = np.zeros((N, xno))
    for i in range(N):
        for j in range(xno):
            for k in range(bits * j, (j + 1) * bits):
                x[i][j] += S[i][k] * (2 ** (bits - (k - j * bits) - 1))

    realx = np.zeros((N, xno))
    for i in range(N):
        for j in range(xno):
            realx[i][j] = limit[j][1] + x[i][j] * (limit[j][0] - limit[j][1]) / ((2 ** bits) - 1)

    fv =np.zeros(N)
    for i in range(N):
        fv[i] = 1 / (1 + (fun(realx[i][0], realx[i][1]) ** 2))

    # Elitism

    for j in range(n):
        b=np.argmax(fv)
        children[j,:]=S[b,:]
        fv=np.delete(fv,b)
        S=np.delete(S,b,0)

    probability = np.zeros(N-n)
    for i in range(N-n):
        probability[i] = fv[i]/np.sum(fv)

    cumulativeProb = np.zeros(N-n)
    for i in range(N-n):
        if(i==0):
            cumulativeProb[0]=probability[0]
        cumulativeProb[i] =cumulativeProb[i-1] + probability[i]

    matingPool=np.zeros((N-n,(xno*bits)))

    for k in range(N-n):
        matingIndex=(random.randint(0,100))/100
        for i in range(N-n):
            if(matingIndex<=cumulativeProb[i]):
                index = i
                break
        if(matingIndex>cumulativeProb[N-n-1]):
            index = N -n- 1
        matingPool[k, :] = S[index, :]



    # Generating a set of non repeating
    # random numbers
    I=np.zeros(N-n)
    I[0] = random.randint(0,N-n-1)
    k=1
    while(k<N-n):
        index = random.randint(0,N-n-1)
        for i in range(k):
            if(index != I[k-i-1]):
                r=True
            if(index == I[k-i-1]):
                r=False
                break
        if(r==True):
            I[k]=index
            k=k+1

    # Generating the CorssOver Parents pairs
    # and children solutions

    parents = np.zeros((N-n, (xno * bits)))

    for j in range(N-n):
        parents[j,:] = matingPool[int(I[j]),:]


    # First and last parents in the matrix form a pair
    # Similarly second and secondlast parent form a pair
    crossoverSite=random.randint(1,xno*bits-1)

    temp=np.zeros(crossoverSite)
    for j in range(int((N-n)/2)):
            if(random.randint(0,100)<=(crossProb*100)):
                temp[:] = parents[j,0:crossoverSite]
                parents[j,0:crossoverSite] = parents[N-n-j-1,0:crossoverSite]
                parents[N-n-j-1,0:crossoverSite] = temp[:]

    for i in range(N-n):
        for j in range(xno*bits):
            if((random.randint(0,100)/100)<mutProb):
                parents[i][j] = (parents[i][j] + 1)%2


    for j in range(n,N):
        children[j,:]=parents[j-n,:]

    gen=gen+1
    S=np.zeros((N,xno*bits))
x = np.zeros((N, xno))
for i in range(N):
    for j in range(xno):
        for k in range(bits * j, (j + 1) * bits):
            x[i][j] += children[i][k] * (2 ** (bits - (k - j * bits) - 1))

for i in range(N):
    for j in range(xno):
        realx[i][j] = limit[j][1] + x[i][j] * (limit[j][0] - limit[j][1]) / ((2 ** bits) - 1)

print("\n\nSolution after generation " + str(gen)+"\n")
print(realx)
fv=np.zeros(N)
for i in range(N):
    fv[i] = 1 / (1 + (fun(realx[i][0], realx[i][1]) ** 2))
b=np.argmax(fv)
print("\nOptimized solution is :\n\n")
print("x1\tx2")
print(str(realx[b][0])+"\t"+str(realx[b][1]))