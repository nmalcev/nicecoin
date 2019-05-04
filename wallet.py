import Crypto
import binascii
import hashlib

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

from transaction import Transaction

class Wallet:
	def __init__(self, initAmount):
		# A nicecoin wallet contains a collection of key pairs,
		# each consisting of a private key and a public key.		
		self.amount = initAmount
		self.public_key = None
		self.private_key = None
		self.address = None
		self.BITS = 1024

		self.generate_keys()
		self.generate_address()
		

	def generate_address(self):
		# A address is a string of digits and characters that can be shared with anyone who wants to send you money.
		self.address = hashlib.sha256(self.public_key.encode('ascii')).hexdigest()

		return self.address


	def generate_keys(self):
		random_generator = Crypto.Random.new().read

		private_key = RSA.generate(self.BITS, random_generator)
		public_key = private_key.publickey()

		private_key = private_key.exportKey(format='DER')
		public_key = public_key.exportKey(format='DER')

		self.private_key = binascii.hexlify(private_key).decode('ascii')
		self.public_key = binascii.hexlify(public_key).decode('ascii')
	

	def transfer(self, destinationAddress, amount):
		"""
		The transfer() method:
		1. creates transaction to another destination, 
		2. sign this transaction
		"""
		# Check if there is enough money
		if (self.amount < amount):
			return None

		self.amount = self.amount - amount
		transaction = Transaction(self.address, destinationAddress, amount, 0)
		transaction.sign(self.private_key)
		return transaction



