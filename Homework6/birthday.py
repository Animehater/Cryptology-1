#!/usr/bin/python3
import time
import sys
if sys.version_info < (3,):
    print("Use Python 3 to run this code")
    exit(1)

import hashlib, random

sha256 = hashlib.new('sha256')

# Change this to something lower for experiments but make sure to put it back to 48 afterwards
# Must be a multiple of 4
hashlen = 48
tic = time.perf_counter()
# A hash function:
# The input is an integer.
# The output is a 'hash_len' bit string, encoded in hex (8 bytes)
def H(number:int) -> str:
    hash = sha256.copy()
    hash.update(str(number).encode('ascii'))
    return hash.hexdigest()[0:hashlen//4]

assert H(123) != H(1230)
assert len(H(1))*4 == hashlen

# This is not the right solution. Too slow.
# On my computer:
#   hashlen | time
#    16     |  0.1 sec
#    24     |  45 sec
#    32     |  7 hours
#    48     |  estimate: 52 years
#    64     |  estimate: 3.4 million years
# Of course, this is highly unoptimized code. The same algorithm would run muuuch faster
# if implemented well
def find_collision_slow():
    while True:
        x1 = random.randint(0,2**(hashlen*2))
        x2 = random.randint(0,2**(hashlen*2))
        h1 = H(x1)
        h2 = H(x2)
        if h1==h2 and x1!=x2:
            return (x1,x2)

# Commented out because it's too slow. You can try it out using smaller values of hashlen
#(x1,x2) = find_collision_slow()
# print (x1,x2)
# assert x1 != x2
# assert H(x1) == H(x2)


# Collision finding using birthday attack
# Returns a pair (x1,x2) such that H(x1)=H(x2)
# My code, quite unoptimized (using off-the-shelf python datastructes) takes the following time:
#   hashlen | time
#    16     |  <0.1 sec
#    24     |  <0.1 sec
#    32     |  0.5 sec
#    48     |  72 sec
#    64     |  7min 20sec
def find_collision():
    hashMap = {} #hashmaps are optimal, search and input time is O(1), for array O(1) and O(n) 
    n = hashlen//2
    for i in range(2**n):
        x1 = random.randint(0,2**(hashlen*2))
        h1 = H(x1)
        if h1 in hashMap:
            return (x1, hashMap[h1]) 
        hashMap[h1] = x1
    return (1,1)
def find_collision_infinite():
    hashMap = dict()
    while 1 == 1 :
        x1 = random.randint(0,2**(hashlen*2))
        h1 = H(x1)
        if h1 in hashMap:
            return (x1, hashMap[h1]) # 
        hashMap[h1] = x1

(x1,x2) = find_collision() #sometimes won't work
#(x1,x2) = find_collision_infinite() will always work, or python will just kill it 
print (x1,x2)
assert x1 != x2
assert H(x1) == H(x2)
toc = time.perf_counter()
print(f"Made attack in {toc - tic:0.4f} seconds")
