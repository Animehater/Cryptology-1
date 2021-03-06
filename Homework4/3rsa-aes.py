#!/usr/bin/python3

# Use "pip install sympy" (possibly with sudo) to install sympy
# And "Crypto" might need "pip install pycrypto" if it's not installed

import sympy, math, Crypto, random

prime_len = 1024

# Copied from http://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def rsa_keygen():
    while True:
        try:
            p = sympy.ntheory.generate.randprime(2**prime_len,2**(prime_len+1))
            q = sympy.ntheory.generate.randprime(2**prime_len,2**(prime_len+1))
            e = 3
            N = p*q
            phiN = (p-1)*(q-1)
            pk=(N,e)
            sk=(N,modinv(e,phiN))
            return (pk,sk)
        except Exception as e:
            pass

# Rough ad-hoc algorithm, not optimized
def exp_mod(a,e,N):
    res = 1
    b = a
    i = 0
    while e>=2**i: # Invariant: b=a**(2**i)
        if e & 2**i != 0:
            e -= 2**i
            res = (res*b) % N
        b=(b*b) % N
        i += 1
    assert e==0
    return res

# Just a test
assert exp_mod(23123,323,657238293) == ((23123**323) % 657238293)

def rsa_enc(pk,m):
    (N,e) = pk
    return exp_mod(m,e,N)

def rsa_dec(sk,c):
    (N,d) = sk
    return exp_mod(c,d,N)

def int_to_bytes(i,len): # Not optimized
    res = []
    for j in range(len):
        res.append(i%256)
        i = i>>8
    return bytes(res)

def aes_cbc_enc(k,m):
    from Crypto.Cipher import AES
    from Crypto import Random
    assert len(m)%AES.block_size == 0
    k = int_to_bytes(k,AES.block_size)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(k, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(m)

def aes_cbc_dec(k,m):
    from Crypto.Cipher import AES
    from Crypto import Random
    k = int_to_bytes(k,AES.block_size)
    iv = m[:AES.block_size]
    cipher = AES.new(k, AES.MODE_CBC, iv)
    return cipher.decrypt(m[AES.block_size:])

# Just a test
assert aes_cbc_dec(2123414234,aes_cbc_enc(2123414234,b'hello there test')) == b'hello there test'

def hyb_enc(pk,m):
    assert isinstance(m,bytes)
    k = random.getrandbits(256)
    aes_k_m = aes_cbc_enc(k,m)
    assert m == aes_cbc_dec(k,aes_k_m)
    rsa_pk_k = rsa_enc(pk,k)
    return (rsa_pk_k,aes_k_m)

def hyb_dec(sk,c):
    (c1,c2) = c
    k = rsa_dec(sk,c1)
    m = aes_cbc_dec(k,c2)
    return m
def cubic_recur(x, x_left, x_right): # to big for python using recursive code

    # I got tired trying python int, round func to work, so I used binary search (O(log n) speed is fine)
    # Here is the basic concept from wiki - https://en.wikipedia.org/wiki/Dichotomy
    if (x_right >= x_left):
        point = x_left + (x_right - x_left)/2
        if x == (point**3):
            return point
        elif x > (point**3):
            return cubic(x,point+1,x_right)
        else:
            return cubic(x,x_left,point-1)
    else:
        raise Exception('System failed to find cubic root')
def cubic(x): #recursive way also didn't work well
    x_left = 0
    x_right = 2**512 # I tested, seems enough for search
    point = 0
    while (x_right - x_left) != 0:
        point = (x_right + x_left) // 2
        if x == (point**3):
            return point
        elif x > (point**3):
            x_left = point + 1
        elif x < (point**3):
            x_right = point - 1
def adv(pk,c):
    (c1,c2) = c
    print (c1)
    print (" ")
    print (c2)
    #root = c1 ** 1/3 #----- didn't work
    #root = cubic_recur(c1, 0, 2**256) #---also didn't work
    root = cubic(c1)
    print (root)
    m = aes_cbc_dec(root,c2)
    return m

def test_adv():
    (pk,sk) = rsa_keygen()
    # Generate a message m
    m = b"a few random words to be shuffle randomly to get some interesting ciphertext not really much sense in it but seemed fun to do instead of random bits etc bla bla".split()
    random.shuffle(m)
    m = b" ".join(m)
    # Get a key pair
    (pk,sk) = rsa_keygen()
    # Encrypt m
    c = hyb_enc(pk,m)
    # Just a test
    assert m == hyb_dec(sk,c)
    # Call the adversary, let him guess m
    m2 = adv(pk,c)
    assert isinstance(m2,bytes)
    # Check
    if m==m2:
        print("Success. The adversary broke the scheme")
    else:
        print("*** Failure ***")

test_adv()