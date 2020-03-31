#Elliptic Diffie Hellman
#find shared secret K
#use the X coordinate from K, decipher the ciphertext

#read file
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
            read.append(line)
    return read
file=read('ECDHinput.txt')

A=int(file[0])
B=int(file[1])
p=int(file[2])
Gx=file[3]
Gy=file[4]
Qax=file[5]
Qay=file[6]
b=int(file[7])
#do not convert text into int
#starting 0 will be lost
text=file[8]


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

#K=b*Qa=a*Qb
Kx,Ky=callculate_aG(b,p,Qax,Qay)
intKx=int2bin(Kx)
text=str(text)
#truncate Kx into fixed length (same with len(text))
m=intKx[0:len(text)]

#decipher text using xor calculation
decipher=''
for i in range (len(text)):
    if text[i]!=m[i]:
        decipher+='1'
    else:
        decipher+='0'

print (bin2msg(decipher))




