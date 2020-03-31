#Elliptic Curve Elgamal
#Alice receives C1, C2 from Bob
#M=C2-a*C1 

#read parameters
def read(file):
    read=[]
    f=open(file)
    lines = f.readlines()
    for line in lines:
        #remove '\n' 
        line=line.strip('\n')
        #split x,y coordinates of P or Q based on ',' signal
        if ',' in line:
            line=line.split(',')
            for i in line:
                read.append(int(i))
        else:
            read.append(int(line))
    return read
file=read('ECElGamalinput.txt')

A=file[0]
B=file[1]
p=file[2]
Gx=file[3]
Gy=file[4]
C1x=file[5]
C1y=file[6]
C2x=file[7]
C2y=file[8]
a=file[9]

def int2bin(integer):
    binString = ''
    while integer:
        if integer % 2 == 1:
            binString = '1' + binString
        else:
            binString = '0' + binString
        integer //= 2
    while len(binString)%8 != 0:
        binString = '0' + binString
    return binString

def bin2int(binary):
    return int(binary,2)

def bin2msg(binary):
    return ''.join(chr(int(binary[i*8:i*8+8],2)) for i in range(len(binary)//8))

def int2msg(integer):
    return bin2msg(int2bin(integer))

def fastPower(g,x,p):
    a = g
    b = 1
    while x>0:
        if x%2 == 1:
            b = (b*a)%p
        a = (a*a)%p
        x = x//2
    return b

def InverseCalculator(g,p):
    return fastPower(g,p-2,p)


#Elliptic Curve
#P+P
def elliptic_curve_PP(x,y,p):
    if x=='bigo' and y=='bigo':
        return 'bigo','bigo'
    k_up=(3*x*x+A)%p
    k_down=(2*y)%p
    k_down_inverse=InverseCalculator(k_down,p)
    k=k_up*k_down_inverse
    b=(y-k*x)%p
    x=(k*k-x-x)%p
    y=(-(k*x+b))%p
    return x,y

#P+Q
def elliptic_curve_PQ(Px,Py,Qx,Qy,p):
    if Px=='bigo' and Py=='bigo':
        return Qx,Qy
    if Qx=='bigo' and Qy=='bigo':
        return Px,Py
    if Px==Qx and (Py+Qy)%p==0:
        return 'bigo','bigo'
    else:
        k_up=(Qy-Py)%p
        k_down=(Qx-Px)%p
        k_down_inverse=InverseCalculator(k_down,p)
        k=(k_up*k_down_inverse)%p
        b=(Py-k*Px)%p
        x=(k*k-Px-Qx)%p
        y=(-(k*x+b))%p
        return x,y

#a*P
def callculate_aG(a,p,Gx,Gy):
    #find binary a, add P according to binary a
    new_a=str(int(int2bin(a)))
    new_a=new_a[::-1]
    lis=[]
    x=Gx
    y=Gy
    for i in range (len(new_a)):
        lis.append([x,y])
        x,y=elliptic_curve_PP(x,y,p)

    #find start point
    start=0
    while new_a[start]!='1':
        start+=1

    Px=lis[start][0]
    Py=lis[start][1]
    i=start+1
    #add Q
    while i<len(new_a):
        if new_a[i]=='1':
            Qx=lis[i][0]
            Qy=lis[i][1]
            Px,Py=elliptic_curve_PQ(Px,Py,Qx,Qy,p)
        i+=1
    return Px,Py

#n=a*C1
nx,ny=callculate_aG(a,p,C1x,C1y)
#m=C2-n=C2-a*C1
mx,my=elliptic_curve_PQ(C2x,C2y,nx,-ny,p)

print (int2msg(mx))