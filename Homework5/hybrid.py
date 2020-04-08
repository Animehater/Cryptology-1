#!/usr/bin/python3

# You may need to install pycrypto using "pip install pycrypto"

import Crypto.PublicKey.ElGamal
import Crypto.Random
import Crypto.Random.random
from Crypto.Cipher import AES

def nb(i, length=False):
    # converts integer to bytes
    b = b''
    if length==False:
        length = (i.bit_length()+7)//8
    for _ in range(length):
        b = bytes([i & 0xff]) + b
        i >>= 8
    return b


# Not a recommended keylen. But quicker for experimenting.
elgamal_keylen = 512

def bytes_to_int(byts):
    """Converts a bitstring (given as a bytes object) into an integer"""
    assert isinstance(byts,bytes)
    i = 0
    for b in byts:
        i *= 256
        i += b
    return i

def int_to_bytes(i,len): # Not optimized
    res = []
    for j in range(len):
        res.append(i%256)
        i = i>>8
    res.reverse()
    return bytes(res)

# Test:
m = b"This is a test!"
assert int_to_bytes(bytes_to_int(m),len(m))==m



# WARNING: I have not checked whether these implementations are any
# secure. In fact, a superficial look at the code of
# Crypto.PublicKey.ElGamal leads me to think that it is not (messages
# are not required to be quadratic residues).

random = Crypto.Random.new()

def elgamal_keygen():
    """Returns an ElGamal key pair (pk,sk).
    Call as "(pk,sk) = elgamal_keygen()".
    """
    sk = Crypto.PublicKey.ElGamal.generate(elgamal_keylen, random.read)
    pk = sk.publickey()
    return (pk,sk)

def elgamal_encrypt(pk,msg):
    """Raw ElGamal encryption.
    msg must satisfy 0<=msg<pk.p"""
    assert isinstance(msg,int), "Message must be an integer"
    assert 0<=msg<pk.p, "Message must satisfy 0<=msg<p"
    k = Crypto.Random.random.StrongRandom().randint(1,pk.p-1)
    return pk.encrypt(msg,k)

def elgamal_decrypt(sk,c):
    """Raw ElGamal decryption."""
    return sk.decrypt(c)

def aes_keygen():
    """Returns a 32 bytes AES key"""
    return Crypto.Random.new().read(256//8)

def aes_encrypt(k,msg):
    """Encrypts with AES, CBC-mode. Not IND-CCA secure.
    Message length must be a multiple of 16."""
    assert isinstance(k,bytes), "Key must be a string/byte sequence"
    assert isinstance(msg,bytes), "Msg must be a string/byte sequence"
    iv = Crypto.Random.new().read(AES.block_size)
    cipher = AES.new(k,AES.MODE_CBC,iv)
    return iv+cipher.encrypt(msg)


def aes_decrypt(k,c):
    """Decrypt with AES. (Probably not IND-CCA secure)"""
    assert isinstance(k,(str,bytes)), "Key must be a string/byte sequence"
    assert isinstance(c,(str,bytes)), "Ciphertext must be a string/byte sequence"
    iv = c[:16]
    cipher = AES.new(k,AES.MODE_CBC,iv)
    return cipher.decrypt(c[16:])


# Just for demo & testing:
k = aes_keygen()
msg = b"Hello world... !"
c = aes_encrypt(k,msg)
msg2 = aes_decrypt(k,c)
print("Result of decrypting with AES:",msg2)
assert msg==msg2, "AES encryption did not decrypt correctly"

    
# Just for demo & testing:
(pk,sk) = elgamal_keygen()
msg = 1234567
c = elgamal_encrypt(pk,msg)
msg2 = elgamal_decrypt(sk,c)
print("Result of decrypting with ElGamal:", msg2)
assert msg==msg2, "ElGamal encryption did not decrypt correctly"


def hybrid_keygen():
    return elgamal_keygen() # already does the job, so why not reuse it

def hybrid_encrypt(pk,msg):
    sim_key = aes_keygen()
    sim_key_for_el = bytes_to_int(sim_key)
    c1 = elgamal_encrypt(pk, sim_key_for_el)
    c2 = aes_encrypt(sim_key, msg)
    return (c1,c2)

def hybrid_decrypt(sk,c):
    c1,c2 = c
    sim_key_for_el = elgamal_decrypt(sk, c1)
    sim_key = nb(sim_key_for_el) #your functions didn't work
    msg = aes_decrypt(sim_key,c2) 
    return msg 


# Just for demo & testing:
(pk,sk) = hybrid_keygen()
msg = b"Hello my world!!"
c = hybrid_encrypt(pk,msg)
msg2 = hybrid_decrypt(sk,c)
print("Result of decrypting with hybrid encryption:", msg2)
assert msg==msg2, "Hybrid encryption did not decrypt correctly"


