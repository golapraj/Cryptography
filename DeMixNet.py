                                                #########################################
                                                #                                       #
                                                # Author: Md. Asaf-uddowla Golap        #
                                                # Email : asaf.golap@gmail.com          #
                                                # Date  : 20/12/2018                    #
                                                #                                       #
                                                #########################################

from random import randint,randrange, random

def is_prime(n, k=5): 
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

def randprime2(m,n):
    found_prime = False
    while not found_prime:
        p = randint(2,n)
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

def gen_key(p,q): 

	key = randprime2(p,q) 
	while gcd(p, key) != 1: 
		key = randprime2(p,q) 

	return key 


def encrypt(msg, P, Y, g): 
	r = gen_key(2,P)
	s = pow(Y, r, P) 
	c1 = pow(g, r, P) 
	c2 = pow(s * msg,1,P)

	return c2, c1

def decrypt(en_msg, c1, x, P): 
	h = pow(c1, x, P)
	h = modinv(h,P)
	dr_msg = (en_msg*h)%P 
		
	return dr_msg 


def DecryptionMixNet(m,n): 

	P = randprime(1024) 
	g = randint(2, P) 

	print "\tP :",P
	print "\tg : ", g
	
	Xs=[]
	Ys=[]
	Y=1

	for i in range(n):
		print "\t### Mix Router ",i+1," ###"
		x = gen_key(2**10,2**16)
		y = pow(g, x, P)
		Xs.append(x)
		Ys.append(y)
		Y=(Y*y)%P
		
		print "\tx : ", x
		print "\tY : ", y

	c2,c1 = encrypt(m,P,Y,g)
	print "\t### At Sender ###"
	print "\tc1: ",c1
	print "\tc2: ",c2
	
	
	for i in range(n):
		c2 = decrypt(c2, c1, Xs[i], P)
		print "\t### At Mix Router ",i+1," ###"
		print "\tc2: ",c2



m=int(input("\tEnter Your Message: "))
n=int(input("\tEnter Number of Mix Router: "))
DecryptionMixNet(m,n) 
