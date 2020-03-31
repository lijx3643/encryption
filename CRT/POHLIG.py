#Pohlig Hellman
#solve the discrete log problem (g^x = h (mod p)) for x

#read parameters from file
def read(file):
    read=[]
    f=open('POHLIGinput.txt')
    lines = f.readlines()
    for line in lines:
            line=line.strip('\n')
            read.append(line)
    return int(read[0]),int(read[1]),int(read[2])

#factorizaiton of given number P
def factor(P):
    list=[]
    n=int((P)**0.5)
    i=2
    while i<=n:
        while (P)%i==0:
            list.append(i)
            P=P//i
        i+=1
    return list

#calculate fast power
def fastPower(g,x,p):
    a = g
    b = 1
    while x>0:
        if x%2 == 1:
            b = (b*a)%p
        a = (a*a)%p
        x = x//2
    return b

#calculate inverse
def gcd(a,b,p):
    p0,p1=0,1
    while a%b:
        c=a//b
        p0,p1=p1,(p0-p1*c)%p
        a,b = b, a%b
    return p1

#calculate new g, new h
#g_new=g^((p-1)/(q^e))
#h_new=h^((p-1)/(q^e))
def calculate(g,h,q,factor_list):
    g_new=fastPower(g,((P-1)/(q**factor_list.count(q))),P)
    h_new=fastPower(h,((P-1)/(q**factor_list.count(q))),P)
    return g_new,h_new

#babystep, giantstep
#calculate (g^x = A (mod p)) for x
def BSGS(g,A,p):
    list1=[]
    n=int(p**0.5)+1
    g_inverse=gcd(p,g,p)
    signal=0
    j=0

    #finish list1 
    for i in range (n):
        list1.append(fastPower(g,i,p))
    #judgment for each number in list2
    while signal!=1:
        number=fastPower(g_inverse,j*n,p)*A%p
        if number in list1:
            a=list1.index(number)+j*n
            signal=1
        j+=1
    return a

#read parameters
P,g,h=read('POHLIGinput.txt')
#factorization of P-1
factor_list=factor(P-1)
#find set of factors
factor_set=list(set(factor_list))

#calculate x1,x2...for CRT
x_list=[]
for q in factor_set:
    g_new,h_new=calculate(g,h,q,factor_list)
    x=BSGS(g_new,h_new,P)
    x_list.append(x)

#CRT
result=0
for i in range(len(x_list)):
    m=factor_set[i]**factor_list.count(factor_set[i])
    n=(P-1)//m
    result+=x_list[i]*n*gcd(m,n,m)
result=result%(P-1)
print (result)