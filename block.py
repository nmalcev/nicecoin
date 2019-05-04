import hashlib
import time


class Block:
	def __init__(self, transactions=[], index=0):
		self.index = index
		self.previousHash = ""
		self.transactions = transactions
		self.timestamp = time.time()
		self.nonce = 0
		self.merkleRoot = self.getMercleRoot()
		self.hash = self.calculateHash()

	
	def calculateHash(self):
		# calculate hash from metadata
		return hashlib.sha256(
			str(self.index) + 
			str(''.join([transaction.to_hash() for transaction in self.transactions])) + 
			str(self.timestamp) + 
			self.previousHash + 
			str(self.merkleRoot) +
			str(self.nonce)
		).hexdigest()


	def mineBlock(self, blockValid):
		# Method for Proof of Work
		startTime = time.time()
		
		while not blockValid(self):
			self.nonce += 1
			self.hash = self.calculateHash()
		
		computeTime = time.time() - startTime

		return computeTime
	
	def to_dict(self):
		return {
			'index': self.index,
			'previousHash':	self.previousHash,
			'transactions': [transaction.to_dict() for transaction in self.transactions],
			'timestamp': self.timestamp,
			'nonce': self.nonce,
			'merkleRoot': self.merkleRoot,
			'hash': self.hash,
		}
	
	def getMercleRoot(self):
		"""
		https://hackernoon.com/merkle-trees-181cb4bc30b4
		"""
		if (len(self.transactions) == 0):
			return None

		hashList = [transaction.signature for transaction in self.transactions]

		# _aggregateTree() iterates by paires
		if (len(hashList) % 2 == 1):
			hashList.append(hashList[0])

		root = self._aggregateTree(hashList)
		while (type(root) is list):
			root = self._aggregateTree(root)

		return root
	

	def _aggregateTree(self, list):	
		if len(list) == 2:
			return list[0] + list[1]
		else:
			# Iterate list by pairs
			out = []
			cur = None
			for item in list:
				if cur is None:
					cur = item
				else:
					out.append(hashlib.sha256(cur + item).hexdigest())
					cur = None
			return out		


