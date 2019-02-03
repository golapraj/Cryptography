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

    d = modinv(e,fi)
    
    return p,q,d,e,n

def Blinding(m):
    r=blindingfactor(n)
    a=pow(r,e,n)
    bm=(m*a)
    bm=pow(bm,1,n)
    
    return (bm,r)

def Signing(bm):
    sm=pow(bm,d,n)
    return sm

def Unblinding(sm):
    invr=modinv(r,n)
    um=(sm*invr)
    um=pow(um,1,n)
    return um

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
bm,r=Blinding(m)
print "\tBlinding Factor, r: ",r
print "\tBlinded Message, alpha = r^e * m:",bm



###########################
# Phase 3: Signing        #
###########################
print "\n\t-:Signing Phase:-"
sm=Signing(bm)
print "\tSigned Message, t = alpha^d:",sm



###########################
# Phase 4: Unblinding     #
###########################
print "\n\t-:Unblinding Phase:-"
um=Unblinding(sm)
print "\tUnblinded Signed Message, s = t * r^-1: ",um



###########################
# Phase 5: Verification   #
###########################
print "\n\t-:Verification Phase:-"
vm=Verification(um)
if(m==vm):
    print "\tVerified Message, m = s^e: ",vm
    print "\tm = vm  ==> Verified"
else:
    print "\tVerified Message, s^e: ",vm
    print "\tm != vm  ==> Not Verified"
