#RSA + prime generator
#generate parameters P,Q,e
#encrypt and decrypt message
#Bob: encrypt m, calculate c, send c
#Alice: receive c, calculate d, decrypt c, find m


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

#calculate greatest common divisor
def gcd(a,b):
    while b:
        a,b = b, a%b
    return a




#generate parameters
#generate fixed-length binary number
#start and end with '1'
#binary to integer
import random
def generator(length):
    a=['0','1']
    num='1'
    for i in range (length-2):
        num=num+random.choice(a)
    num=num+'1'
    num=bin2int(num)
    return num

#randomly select value a from [1,num-1]
#satify gcd(a,num)=1
def select_a(num):
    a=random.randint(1,num-1)
    return a

#Fermat witness test
#a^(n-1) mod n ==1  -> false witness, prime
#a^(n-1) mod n !=1  -> true witness, composite 
def Fermat_witness(a,n):
    if fastPower(a,n-1,n)==1:
        return False
    else:
        return True

#prime generator
#generate num-> select a-> test witness -> num is prime
#test witness for 10 times for each num
#if all 10 witnesses are false -> num is prime
def generate_prime(length):
    judge=True # initial state = true -> enter the loop
    while judge==True: # judge conditions, true-> start new loop
        judge=False # (initial state = true) will wash out the following judgements in "or" function
        num=generator(length)
        for i in range (10):
            a=select_a(num)
            new_judge=Fermat_witness(a,num)
            judge=judge or new_judge # as long as there is one true in 10 tests, then num is not prime, start new loop
    return num

#generate parameters
P=generate_prime(256)
Q=generate_prime(256)
PQ=P*Q
F=(P-1)*(Q-1)
#e is coprime to F
e=F
while gcd(e,F)!=1:
    e=generate_prime(512)
print ("P: ", P)
print ("Q: ", Q)
print ("e: ", e)



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

