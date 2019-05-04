import time
import binascii
import hashlib

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from collections import OrderedDict

class Transaction:
	def __init__(self, sender_address, recipient_address, amount, fees=0):
		"""
		A transaction tells the network that the owner of some Nicecoin value has authorized the transfer of that value to another owner.
		"""
		self.sender_address = sender_address
		self.recipient_address = recipient_address
		self.amount = amount
		self.fees = fees
		self.timestamp = time.time()
		self.signature = None


	def to_dict(self):
		return {
			'sender': self.sender_address,
			'recipient': self.recipient_address,
			'amount': self.amount,
			'timestamp': self.timestamp,
			'fees': self.fees,
			'signature': self.signature
		}


	def to_hash(self):
		return hashlib.sha256(
			self.sender_address +
			self.recipient_address +
			str(self.amount) +
			str(self.fees) +
			str(self.timestamp)
		).hexdigest()


	def sign(self, sender_private_key):
		secret_key = binascii.unhexlify(sender_private_key)
		"""
		1. Most bitcoin transactions requires a valid digital signature to be included in the blockchain,
		which can only be generated with a secret key;
		2. In the scope of the transaction, the current Nicecoin owner presents own public key and a signature in a transaction to spend those Nicccoin.
		Through the presentation of the public key and signature, everyone in the Nicecoin network can verify and accept the transaction as valid, confirming that the person transferring the nicecoin owned them at the time of the transfer.
		"""
		private_key = RSA.importKey(secret_key)
		signer = PKCS1_v1_5.new(private_key)
		self.signature = binascii.hexlify(self.to_hash()).decode('ascii')
		
		return self.signature
