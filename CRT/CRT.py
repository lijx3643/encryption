#CRT

#read parameters from file
read=[]
f=open('CRTinput.txt')
lines = f.readlines()
for line in lines:
        line=line.strip('\n')
        read.append(line)
P,Q,g,x=int(read[0]),int(read[1]),int(read[2]),int(read[3])
T=P*Q

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

#mod base and exponent
a=g%P
b=x%(P-1)
c=g%Q
d=x%(Q-1)
u=fastPower(a,b,P)
v=fastPower(c,d,Q)
m=gcd(P,Q,P)
n=gcd(Q,P,Q)
#calculate h
h=(Q*m*u+P*n*v)%T
print (h)