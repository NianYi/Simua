#!/usr/bin/env python
from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64
class rsa(object):
	def __init__(self):
		self.random_generator = Random.new().read
		secret = RSA.generate(1024,self.random_generator)
		private_pem = secret.exportKey()
		public_pem = secret.publickey().exportKey()
		with open('private.pem','w') as f:
			f.write(private_pem)
		with open('public.pem','w') as f:
			f.write(public_pem)
	@classmethod
	def encrypt(cls,oriString):
		with open('public.pem') as f:
			key = f.read()
			rsakey  =RSA.importKey(key)
			cipher = Cipher_pkcs1_v1_5.new(rsakey)
			cipher_text = base64.b64encode(cipher.encrypt(oriString))
			return cipher_text
	@classmethod
	def decrypt(cls,secString):
		with open('private.pem') as f:
			key = f.read()
			rsakey  =RSA.importKey(key)
			cipher = Cipher_pkcs1_v1_5.new(rsakey)
			ori_text = cipher.decrypt(base64.b64decode(secString),Random.new().read)
			return ori_text

