g = 666 # Shared base
p = 6661 # Shared prime
PK = 2227 # Bob public key ( = g**x % p)

# Helper function brute forcing a private key
def brute_force_private_key(PK, g, p):
    for i in range(1, p):
        if g**i % p == PK:
            return i

# 1) Alice wants to send the message 2000 to Bob

m = 2000 # Alice's message

# Alice picks a random integer from 1, ..., p - 1
from random import randint
y = randint(1, p-1)

# Alice computes the shared secret
s = PK**y % p

# Alice computes the chipetext (c1, c2) and send it to Bob
c1 = g**y % p
c2 = m*s % p

# 2) Eve intercepts Alice's chipertext and decrypts it by finding Bob's private key

# Eve bruteforces Bob's private key
x_eve = brute_force_private_key(PK, g, p)

print("Bob's private key is", x_eve)

# Eve recostructs the shared secret
s_eve = c1**x_eve % p
assert(s == s_eve)

# Eve finds the inverse of s_eve
s_eve_inverse = pow(s_eve, -1, p)

assert(s_eve * s_eve_inverse % p == 1)

m_eve = c2 * s_eve_inverse % p
assert(m == m_eve)

print("Eve reconstructs the message", m_eve)

# 3) Mallory intercepts Alice's chipertext and, without decrypting it, modifies it
# such that it opens to 6000

c2_mallory = 3*c2 % p # This is a valid encryption of 3*m

# Suppose Bob tries to open it

x = 66

# Bob reconstructs the shared secret
s_bob = c1**x % p
assert(s == s_bob)

# Bob finds the inverse of s_bob
s_bob_inverse = pow(s_bob, -1, p)
        
m_bob = c2_mallory * s_bob_inverse % p
assert(3*m == m_bob)
 
print("Bob reconstructs the Mallory's message", m_bob)