from flask import Flask, request, send_from_directory

import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256, SHA
from Crypto.Signature import PKCS1_v1_5
from Crypto import Random
from base64 import b64encode, b64decode

import os
import random
import json

from twilio.rest import Client

from subprocess import call 
import os
from getpass import getpass


def clear(): 
    _ = call('clear' if os.name =='posix' else 'cls') 

twilio_secrets = json.loads(open('twilio.secret').read())

account_sid = twilio_secrets["account_sid"]
auth_token = twilio_secrets["auth_token"]

client = Client(account_sid, auth_token)
values = json.loads(open('../src/values.json').readline())
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'key')

private_key = open(static_file_dir + '/private.pem').read()
sign_key = RSA.importKey(private_key,  passphrase='Brennan123')

app = Flask(__name__)

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

@app.route("/api/key")
def key():
    return send_from_directory(static_file_dir, 'public.pem')

@app.route("/api/login")
def login():
    email = request.args.get('email')
    users = json.loads(open("emails.secret").readline())

    alpha = users[email]["alpha"]
    b = users[email]["b"]

    beta = generate_beta_from_b(b);
    K = pow(int(alpha), b, int(values["p"]))
    m = beta | int(alpha)
    k1,k2 = split_bits("{0:b}".format(K))

    E = AES.new(bitstring_to_bytes(k1), AES.MODE_ECB)
    H = HMAC.new(bitstring_to_bytes(k2), digestmod=SHA256)
    H.update(bitstring_to_bytes("{0:b}".format(m)))
    to_enc = m | int(H.hexdigest(), base=16)
    to_enc_str = str(to_enc)
    pad_bits = 16 - (len(to_enc_str) % 16)

    to_enc_str = to_enc_str + (' ' * pad_bits)
    e = E.encrypt(to_enc_str)

    our_verificaiton = str(b64encode(e), "UTF-8")
    to_verify = request.args.get('m1')

    if (our_verificaiton != to_verify):
        return "Signatures do not match", 403

    h = SHA.new(e)

    signer = PKCS1_v1_5.new(sign_key)
    signature = signer.sign(h)

    print(b64encode(e))

    return sign_data(static_file_dir + '/private.pem', b64encode(e))
     

@app.route("/api/sendCode")
def sendCode():
    email = request.args.get('email')
    users = json.loads(open("emails.secret").readline())
    users[email]["b"],beta = generate_beta_and_b();
    sendSMS("+1" + users[email]["phone"], beta)
    open("emails.secret",'w').write(json.dumps(users))
    return "Success"

@app.route('/api/user', methods = ['POST'])
def create_user():
    email = request.args.get('email')
    users = json.loads(open("emails.secret").readline())
    if (users[email]):
        return "User already exists", 503
    users[email]["alpha"] = request.args.get('alpha')
    users[email]["phone"] = request.args.get('phonenumber')
    open("emails.json", 'w').write(json.dumps(users))
    return 200

def sendSMS(number, message):
    code = client.messages.create(body=message,from_='+12892047798',to=number)
    return code.sid

def generate_beta_and_b():
    b = random.randint(0, int(values["p"]))
    beta = pow(int(values["g"]), b, int(values["p"]))
    return b,beta;

def generate_beta_from_b(b):
    beta = pow(int(values["g"]), b, int(values["p"]))
    return beta;

def split_bits(bits):
    return bits[0:128],bits[129:257]

def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

def pad(data_to_pad, block_size, style='pkcs7'):
    padding_len = block_size-len(data_to_pad)%block_size
    if style == 'pkcs7':
        padding = bchr(padding_len)*padding_len
    elif style == 'x923':
        padding = bchr(0)*(padding_len-1) + bchr(padding_len)
    elif style == 'iso7816':
        padding = bchr(128) + bchr(0)*(padding_len-1)
    else:
        raise ValueError("Unknown padding style")
    return data_to_pad + padding


if __name__ == "__main__":
    clear()
    app.run()
