#read file function
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

file=read('ECSubtractinput.txt')

A=file[0]
B=file[1]
p=file[2]
Px=file[3]
Py=file[4]
Qx=file[5]
Qy=file[6]

#Elliptic Curve
#P-Q

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

print (elliptic_curve_PQ(Px,Py,Qx,-Qy,p))

