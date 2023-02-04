from asyncio.windows_utils import pipe
import cv2
import math as m
import sys
import random
sys.setrecursionlimit(10**6)


img = cv2.imread(r"C:\Users\anumo\Desktop\miniproject\anu.png")
cv2.imshow("original image",img)
img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
img1=img.copy()
img2=img.copy()
cv2.imshow("original gray image",img)

lis=[]
list2=[]

a1=""
codewords=[0,13,23,26,35,46,52,57,70,75,81,92,101,104,114,127]


def compute(osd):
    min=128
    diff=(m.inf)
    for element in codewords:
        d=abs(element-osd)
        if diff>d:
            diff=d
            min=element
    return min
    
def transform(o1,o2):
    os1=o1[4:8:1]
    os2= os1 + o2[5:]
    osd=int(os2,2)
    res=compute(osd)
    res=convert7(res)
    
    o1=o1[0:4]+res[0:4]  
    o2=o2[0:5]+res[4:]
    
    return o1,o2


def convert7(a):
    val= bin(a).replace('0b','')
    x = val[::-1] #this reverses an array.
    while len(x) < 7:
        x += '0'
        val= x[::-1]
    return val
def convert(a):
    val= bin(a).replace('0b','')
    x = val[::-1] #this reverses an array.
    while len(x)<8:
        x += '0'
        val= x[::-1]
    return val
    

for i in range(0,512):
     for j in range(0,512,2):
        
        val2=img[i:i+1,j:j+2]
        o1=convert(val2[0][0])
       
        o2=convert(val2[0][1])
        
        c=transform(o1,o2)
        
        c0=int(c[0],2)
        c1=int(c[1],2)
        img[i:i+1,j:j+2]=c0,c1
        
cv2.imshow("transformed  image ",img)


#message embeding starts from here 
print("message embeding starts from here.....")


def transform_bits(o1,o2):
    os1=o1[4:8:1]
    os2= os1 + o2[5:]
    return os2
for i in range(0,500,28):
     for j in range(0,500,14):
       
        val2=img[i:i+1,j:j+14]
     
        p=0
        list3=[]
        for k in range(7):
            o1=convert(val2[0][p])
            o2=convert(val2[0][p+1])
            '''print(o1)
            print(o2)'''
            p=p+1
            c1=transform_bits(o1,o2)
            list3.append(c1)
           
            
        list2.append(list3)
                 

        
       
print("list2 before flipping",list2[1])       
        
        
    

def indexGen(key,k):   #key generation
    if k==1:
       f1=(key%7)+1
       fk=f1
    else:
       fk=(indexGen(key,k-1)%7)+1
    return fk


B = [               # 3 × 7 HpT parity matrix of the (7, 4) Hamming code
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 0],
    [0, 1, 1],
    [1, 1, 1],
    [1, 0, 1]
            ] 


def mul(A):       #Y = R'×HT
    result = [[0,0,0]]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    v=[]
    for r in result:
        for t in r:
            t=t%2
            v.append(t)

    return v



import math
def toBinary(a):
  l,m=[],[]
  for i in a:
    l.append(ord(i))
  for i in l:
    m.append((bin(i)[2:]))
  return m

print("''message'' in binary is ")
inre=input("enter the message")
li=toBinary(inre)
mi=""
for elem in li:
    mi=mi+elem
#print(mi)
print("mi",mi,len(mi))

z1=0
y1=3
a1=""
key=int(input("enter key"))   
for b1 in range(len(list2)):  #no of 7*7 blocks in list2  len(list2)
    index=indexGen(key,b1+1)
    
    for j in range(7):
        D=[]
        A=[]
        
        elem=list2[b1][j]
        
        for e in elem:
            A.append(int(e))
        
        A[index-1]=abs(int(elem[index-1])-1)
       
        y=mul([A])
      
        if y1>len(mi):
            break
        m=mi[z1:y1]
        if len(m)<3:
            k1=3
            k1=k1-len(m)
            for i in range(k1):
                m=m+str(0)
    

        
        z1=z1+3
        y1=y1+3
        
        for e in range(3):
            
            D.append(y[e]^int(m[e]))
        
       
        if D!=[0,0,0]:
            for i in range(len(B)):
                if B[i]==D:
                   index=i+1
                  
                   A[index-1]=abs(int(elem[index-1])-1)
                   
                   q=6
                   v=0
                   for z in A:
                       v=v+(int(z)*(2**q))
                       q=q-1
                   a1=convert7(v)
                 
        list2[b1][j]=a1
                       
                   
        
       
print("list2 after flipping",list2[1])




lis7=[]

for i in range(0,500,28):
     k=0
     for j in range(0,500,14):
        
        val2=img[i:i+1,j:j+14]
       
        p=0
        lis7=list2[i]
              
        
        
        lis0=[]
        for l in range(7):
            o1=convert(val2[0][p])
            o2=convert(val2[0][p+1])
            p=p+1
            e=lis7[l]
           
            o3=o1[0:4]+e[0:4]
            o4=o2[0:5]+e[4:]
            o5=int(o3,2)
            o6=int(o4,2)
                
            lis0.append(o5)
            lis0.append(o6)
        k=k+1
      
        img[i:i+1,j:j+14]=lis0
          

print("the embedded message",mi)
cv2.imshow("cover image with mesaage",img)



#message extraction phase starts from here 
z=""
print("message extraction phase starts from here ")
list2=[]
lis7=[]

def transform_bits(o1,o2):
    os1=o1[4:8:1]
    os2= os1 + o2[5:]
    return os2
for i in range(0,500,28):
     for j in range(0,500,14):
       
        val2=img[i:i+1,j:j+14]
        
        p=0
        list3=[]
        for k in range(7):
            o1=convert(val2[0][p])
            o2=convert(val2[0][p+1])
            '''print(o1)
            print(o2)'''
            p=p+1
            c1=transform_bits(o1,o2)
            list3.append(c1)
              
            
        list2.append(list3)
key=int(input("enter key the same key which is entered during embedding "))
print("list2[1] in embedding phase",list2[1])
mg=[]

def convert_to_string(ml):
    for i in range(0,len(ml),7):
        mg.append(ml[i:i+7])
    n=""
    for elem in mg:
        n=n+elem
        print(chr(int(elem,2)))
    print("the message extracted from the image is:--->",n)
    

lj=[]
n1=0
for b1 in range(10):  #no of 7*7 blocks in list2  len(list2)
    index=indexGen(key,b1+1)
    lj.append(mi)
  
    for j in range(7):
        D=[]
        A=[]
       
        syn=B[index-1]
        elem=list2[b1][j]
        
        for e in elem:
            A.append(int(e))
       
        A[index-1]=abs(int(elem[index-1])-1)
        
        Dif=mul([A])                #Rt× HT
        
        for e in range(3):
           
            D.append(Dif[e]^syn[e])
       
        
               
            
        print("ddddddddd",D)    
        if D!=[0,0,0]:
            for i in range(len(B)):
                if B[i]==Dif:
                   index=i+1
                   
                   A[index-1]=abs(int(elem[index-1])-1)
                   
                   q=6
                   v=0
                   for z in A:
                       v=v+(int(z)*(2**q))
                       q=q-1
                   a1=convert7(v)
        lj.append(D)
        
        list2[b1][j]=a1

convert_to_string(lj[0])



print("list2 after extracting message",list2[1])




for i in range(0,253,28):
    
        
    
     k=0
     for j in range(0,253,28):
        
        val2=img[i:i+1,j:j+14]
       
        p=0
        lis7=list2[i]
        
        

        lis0=[]
        for l in range(7):
            o1=convert(val2[0][p])
            o2=convert(val2[0][p+1])
            p=p+1
            e=lis7[l]
            
            o3=o1[0:4]+e[0:4]
            o4=o2[0:5]+e[4:]
            o5=int(o3,2)
            o6=int(o4,2)
            lis0.append(o5)
            lis0.append(o6)
        k=k+1
        
        img1[i:i+1,j:j+14]=lis0

        
        
    
            
        



cv2.imshow("cover image after message extraction",img1)

cv2.waitKey(0)
