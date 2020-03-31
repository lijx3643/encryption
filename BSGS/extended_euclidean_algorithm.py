# Calculate inverse of number with extended euclidean algorithm
def gcd(a,b,p):
    p0,p1=0,1
    while a%b:
        c=a//b
        p0,p1=p1,(p0-p1*c)%p
        a,b = b, a%b
    return p1

def fastPower(g,x,p):
    a = g
    b = 1
    while x>0:
        if x%2 == 1:
            b = (b*a)%p
        a = (a*a)%p
        x = x//2
    return b

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

def bin2msg(binary):
    return ''.join(chr(int(binary[i*8:i*8+8],2)) for i in range(len(binary)//8))

def int2msg(integer):
    return bin2msg(int2bin(integer))
#read information from input.txt
read=[]
f=open('input.txt')
lines = f.readlines()
for line in lines:
        line=line.strip('\n')
        read.append(line)
p,g,A,c1,c2=int(read[0]),int(read[1]),int(read[2]),int(read[3]),int(read[4])

list1=[]
list2=[]
dict1={}
dict2={}

n=int(p**0.5)+1
g_inverse=gcd(p,g,p)
signal=0
i=0

while signal!=1:
    list1.append(fastPower(g,i,p))
    list2.append(fastPower(g_inverse,i*n,p)*A%p)
    dict1[list1[i]]=i
    dict2[list2[i]]=i
    if list1[i] in list2:
        a=i+(dict2[list1[i]])*n
        signal=1
    if list2[i] in list1:
        a=dict1[list2[i]]+i*n
        signal=1
    i+=1

number=(fastPower(gcd(p,c1,p),a,p)*c2)%p
print (int2msg(number))