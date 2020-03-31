#Elliptic Curve
#a*P

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

#parameters
Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
a = 55179115824979878594564946684576670362812219109178118526265814188406326272077
p=2**256-2**32-2**9-2**8-2**7-2**6-2**4-1
A=0
B=7

#P+P
def elliptic_curve_PP(x,y,p):
    if x==0 and y==0:
        return 0,0
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
    if Px==0 and Py==0:
        return Qx,Qy
    if Qx==0 and Qy==0:
        return Px,Py
    if Px==Qx and (Py+Qy)%p==0:
        return 0,0
    else:
        k_up=(Qy-Py)%p
        k_down=(Qx-Px)%p
        k_down_inverse=InverseCalculator(k_down,p)
        k=(k_up*k_down_inverse)%p
        b=(Py-k*Px)%p
        x=(k*k-Px-Qx)%p
        y=(-(k*x+b))%p
        return x,y

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
print (Px,Py)
