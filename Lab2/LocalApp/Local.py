import hashlib
from Crypto.Cipher import AES 
from Crypto.Hash import HMAC, SHA256, SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto import Random
from base64 import b64encode, b64decode

from subprocess import call 
import os
from getpass import getpass

g = 49219889161355988781215013502497
p = 85078259166789497942343655585226249444673826357883

def clear(): 
    # check and make call for specific operating system 
    _ = call('clear' if os.name =='posix' else 'cls') 

def split_bits(bits):
    return bits[0:128],bits[129:257]

def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

def verify_sign(public_key_loc, signature, data):
    pub_key = open(public_key_loc, "r").read() 
    rsakey = RSA.importKey(pub_key) 
    signer = PKCS1_v1_5.new(rsakey) 
    digest = SHA256.new() 
    digest.update(b64decode(data)) 
    if signer.verify(digest, b64decode(signature)):
        return True
    return False

def sign_data(private_key_loc, data):
    key = open(private_key_loc, "r").read() 
    rsakey = RSA.importKey(key) 
    signer = PKCS1_v1_5.new(rsakey) 
    digest = SHA256.new() 
    digest.update(b64decode(data)) 
    sign = signer.sign(digest) 
    return b64encode(sign)

clear()
public_key = open('pubkey').read()
beta = input("Enter the SMS you have recieved: ")
clear()
a = getpass("Enter your password: ")
clear()
alpha = pow(g, int(a)) % p
m = int(alpha) | int(beta)

K = pow(int(beta), int(a), p)

k1,k2 = split_bits("{0:b}".format(K))

E = AES.new(bitstring_to_bytes(k1), AES.MODE_ECB)

H = HMAC.new(bitstring_to_bytes(k2), digestmod=SHA256)
H.update(bitstring_to_bytes("{0:b}".format(m)))

to_enc = m | int(H.hexdigest(), base=16)
to_enc_str = str(to_enc)
pad_bits = 16 - (len(to_enc_str) % 16)

to_enc_str = to_enc_str + (' ' * pad_bits)
e = E.encrypt(to_enc_str)

print("Send to website: ")
print(str(b64encode(e), "UTF-8"))
input("Hit enter to continue...")
clear()
b64_signature = input("Enter website's response: ")
clear()

if(verify_sign('key', b64_signature, b64encode(e))):
    print("\033[1;32;40m The signature is authentic.\033[0;37;40m")
else:
    print("\033[1;31;40m The signature is not authentic.\033[0;37;40m")

input("Press enter to exit.")
