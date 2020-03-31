#RSA 
#encrypt and decrypt message
#Bob: encrypt m, calculate c, send c
#Alice: receive c, calculate d, decrypt c, find m

#read file function
def read(file):
    read=[]
    f=open(file)
    lines = f.readlines()
    for line in lines:
            line=line.strip('\n')
            read.append(line)
    return int(read[0]),int(read[1]),int(read[2])

#message transform functions
def msg2bin(message):
    return ''.join(['{0:08b}'.format(ord(i)) for i in message])
def bin2int(binary):
    return int(binary,2)
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

#calculate g^x mod p
def fastPower(g,x,p):
    a = g
    b = 1
    while x>0:
        if x%2 == 1:
            b = (b*a)%p
        a = (a*a)%p
        x = x//2
    return b

#read parameters
P,Q,e=read('RSAinput.txt')
PQ=P*Q

#Bob
#define message m
m='I am Peppa Pig. This is my little brother, George. This is Mummy Pig. And this is Daddy Pig. Hahaha~'

#calculate c for message a
def calculate_c(a):
    a=bin2int(msg2bin(a))
    c=fastPower(a,e,PQ)
    return c

#calculate inverse
def inverse(a,b,p):
    p0,p1=0,1
    while a%b:
        c=a//b
        p0,p1=p1,(p0-p1*c)%p
        a,b = b, a%b
    return p1

#for every 50 digits in message, split it into chunks
#calculate c for every chunk a
#record each c in list_c
count=0
chunk=50
list_c=[]
while count<len(m):
    if (count+chunk)>len(m):
        a=m[count:-1]
    else:
        a=m[count:count+chunk]
    c=calculate_c(a)
    list_c.append(c)
    count+=chunk
print ("list_c: ", list_c)

#Alice
#calculate d
F=(P-1)*(Q-1)
d=inverse(F,e,F)

#for each c in list_c, calculte its m
#append chunk m on mes_decry
mes_decry=''
for c in list_c:
    m=fastPower(c,d,PQ)
    m=bin2msg(int2bin(m))
    mes_decry=mes_decry+m
print (mes_decry)

