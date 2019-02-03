                                                #########################################
                                                #                                       #
                                                # Author: Md. Asaf-uddowla Golap        #
                                                # Email : asaf.golap@gmail.com          #
                                                # Date  : 20/12/2018                    #
                                                #                                       #
                                                #########################################
from random import randint,randrange, random

def is_prime(n, k=100): 
    from random import randint
    if n < 2: return False
    for p in [2,3,5,7,11,13,17,19,23,29]:
        if n % p == 0: return n == p
    s, d = 0, n-1
    while d % 2 == 0:
        s, d = s+1, d//2
    for i in range(k):
        x = pow(randint(2, n-1), d, n)
        if x == 1 or x == n-1: continue
        for r in range(1, s):
            x = (x * x) % n
            if x == 1: return False
            if x == n-1: break
        else: return False
    return True

def randprime(n):
    found_prime = False
    while not found_prime:
        p = randint(2**(n-1), 2**n)
        if is_prime(p):
            return p

def gcd(a, b):
    while b:
        a, b = b, a%b
    return a
      
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('invalid modular inverse ')
    else:
        return (x + m) % m

def blindingfactor(n):
    r=randint(2, 2**32)
    while (gcd(r,n)!=1):
        r=randint(2, 2**32)
    return r

def Initialization(N):
    p = randprime(N)
    q = randprime(N)

    if not (is_prime(p) and is_prime(q)):
        raise ValueError('p or q not prime')
    elif p == q:
        raise ValueError('p=q')

    n=p*q

    fi=(p-1)*(q-1)

    e=2
    
    while(True):
        t=gcd(e,fi)
        if t==1:
            break
        else:
            e=e+1

    d=modinv(e,fi)
    
    return p,q,d,e,n

def Blinding(m):
    r1=blindingfactor(n)
    r2=blindingfactor(n)
    
    if r1 == r2:
        raise ValueError('r1 = r2')
        
    a1 = randprime(10)
    a2 = randprime(15)
    
    if not (is_prime(a1) and is_prime(a2)):
        raise ValueError('a1 or a2 not prime')
    elif a1 == a2:
        raise ValueError('a1 = a2')
    
    bm1=pow(r1,e,n)*pow(m,a1,n)
    bm1=pow(bm1,1,n)
    
    bm2=pow(r2,e,n)*pow(m,a2,n)
    bm2=pow(bm2,1,n)
    
    return (bm1,bm2,r1,r2,a1,a2)

def Signing(bm1,bm2):
    
    b1 = randprime(20)
    b2 = randprime(25)
    
    if not (is_prime(b1) and is_prime(b2)):
        raise ValueError('b1 or b2 not prime')
    elif b1 == b2:
        raise ValueError('b1 = b2')
        
    sm1=pow(bm1,b1*d,n)
    sm2=pow(bm2,b2*d,n)
    return (sm1,sm2,b1,b2)

def Unblinding(sm1,sm2):
    invr1=pow(r1,b1,n)
    invr2=pow(r2,b2,n)
    
    invr1 = modinv(invr1,n)
    invr2 = modinv(invr2,n)

    um1=(sm1*invr1)%n
   
    um2=(sm2*invr2)%n
    
    g,w,u = egcd(a1*b1,a2*b2)

    print "\tw: ", w
    print "\tu: ", u

    #print "\ta1*b1*w + a2*b2*u = ", a1*b1*w + a2*b2*u,"\n"

    if(w<0):
        s1 = pow(um1,-w,n)
        s1 = modinv(s1,n)
    else:    
        s1=pow(um1,w,n)
    
    if(u<0):
        s2 = pow(um2,-u,n)
        s2 = modinv(s2,n)
    else:    
        s2=pow(um2,u,n)

    um = pow(s1*s2,1,n)
    
    return (um,um1,um2,w,u)

def Verification(um):
    v=pow(um,e,n)
    return v
    

m=int(input("\tEnter Your Message: "))

###########################
# Phase 1: Initialization #
###########################
print "\n\t-:Initialization Phase:-"
p,q,d,e,n=Initialization(512)
print "\t p: ",p
print "\t q: ",q
print "\t n = p*q: ",n
print "\t d: ",d
print "\t e: ",e



###########################
# Phase 2: Blinding       #
###########################
print "\n\t-:Blinding Phase:-"
bm1,bm2,r1,r2,a1,a2=Blinding(m)
print "\tRandom Number, r1: ",r1
print "\tRandom Number, r2: ",r2
print "\tRandom Prime, a1: ",a1
print "\tRandom Prime, a2: ",a2
print "\tBlinded Message, alpha 1: ",bm1
print "\t              , alpha 2: ",bm2



###########################
# Phase 3: Signing        #
###########################
print "\n\t-:Signing Phase:-"
sm1,sm2,b1,b2=Signing(bm1,bm2)
print "\tRandom Prime, b1: ",b1
print "\tRandom Prime, b2: ",b2
print "\tSigned Message, t1 = alpha^b1*d: ",sm1
print "\t              , t2 = alpha^b2*d: ",sm2



###########################
# Phase 4: Unblinding     #
###########################
um,um1,um2,w,u=Unblinding(sm1,sm2)
print "\tUnblinded Signed Message, s1 = t1 * r1^-b1: ",um1
print "\t                       , s2 = t2 * r2^-b2: ",um2
print "\tUnblinded Signed Message, s = s1^w * s2^u: ",um



###########################
# Phase 5: Verification   #
###########################
print "\n\t-:Verification Phase:-"
vm=Verification(um)
if(m==vm):
    print "\tVerified Message, m = s^e:",vm
    print "\tm = vm  ==> Verified"
else:
    print "\tVerified Message, m = s^e:",vm
    print "\tm != vm  ==> Not Verified"
