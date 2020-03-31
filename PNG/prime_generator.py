#Prime Generator
#Miller Rabin test

#read parameters
def read(file):
    read=[]
    f=open(file)
    lines = f.readlines()
    for line in lines:
            line=line.strip('\n')
            read.append(line)
    return int(read[0])

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

#generate random number with fixed length
#number cannot be divided by 2,3,5,7
#length shoule be longer than 3 (2,3,5,7 won't be generated)
import random
def generator(length):
    length-=1
    num=random.randint(2**length,(2**(length+1)-1))
    while num%2==0 or num%3==0 or num%5==0 or num%7==0:
        num=random.randint(2**length,(2**length)*2-1)
    return num

#num-1=(2^k)*q
#calculate k,q
def calculate_k_q(num):
    num=num-1
    count=0
    while num%2==0:
        count+=1
        num//=2
    return count,num

#randomly select value a from [1,num-1]
#satify gcd(a,num)=1
def select_a(num):
    a=random.randint(1,num-1)
    while gcd(a,num)!=1:
        a=random.randint(1,num-1)
    return a

#witness test
#round1
#a^q mod n !=1  -> satisfy true witness
def round1(a,q,n):
    if fastPower(a,q,n)!=1:
        return True
    else:
        return False

#round2
#for all i in [0,k-1]
#a^((2^i)*q) mod n != -1 or (n-1)  ->  satisfy true witness
def round2(a,q,n,k):
    for i in range (0,k):
        if fastPower(a,(2**i)*q,n)==-1 or fastPower(a,(2**i)*q,n)==(n-1):
            return False
    return True

#judgement on round1 and round2
#round1 and round2 == True  -> True witness 
def test_witness(a,q,n,k):
    if round1(a,q,n) and round2(a,q,n,k)==True:
        return True
    else:
        return False

#prime generator
#generate num-> select a-> test witness -> num is prime
#test witness for 10 times for each num
#if all 10 witnesses are false -> num is prime
def generate_prime(length):
    judge=True # initial state = true -> enter the loop
    while judge==True: # judge conditions, true-> start new loop
        judge=False # (initial state = true) will wash out the following judgements in "or" function
        num=generator(length)
        k,q=calculate_k_q(num)
        for i in range (10):
            a=select_a(num)
            k,q=calculate_k_q(num)
            new_judge=test_witness(a,q,num,k)
            judge=judge or new_judge # as long as there is one true in 10 tests, then num is not prime, start new loop
    return num

#generate parameters
length=read("PNGinput.txt")
P=generate_prime(length)
print ("P: ", P)


