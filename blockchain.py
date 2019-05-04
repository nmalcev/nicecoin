import json

from datetime import timedelta
from block import Block
from transaction import Transaction
	
class Blockchain:
    # Initialize blockchain
	def __init__(self, genesisBlock, fileName = "chain.json"):
		self.chain = [genesisBlock]
		self.fileName = fileName
		self.transactions = []
		# PoW properties		
		self.difficulty = 4	
		self.difficulty_bits = 8
		self.hashPattern = "0" * self.difficulty
		self.target = 2 ** (256 - self.difficulty_bits)
		self._activeTransactions = []
		
		

	def addBlock(self):
		self._activeTransactions = list(self.transactions)
		self.transactions = []
		newBlock = Block(self._activeTransactions)
		# Method to add new block from Block class
		newBlock.index = len(self.chain)
		newBlock.previousHash = self.chain[-1].hash
		computeTime = newBlock.mineBlock(self.createValidator())
		self.chain.append(newBlock)
				
		self.writeBlocks()
		if (callable(self.onBlockReadyHandler)):
			self.onBlockReadyHandler(newBlock.transactions)
		self._activeTransactions = []		
		return (newBlock, computeTime)

	
	def createValidator(self):
		"""
		Implementation of PoW check
		"""
		def blockValidator(block): 
			return block.hash[:self.difficulty] == self.hashPattern and long(block.hash, 16) < self.target
		return blockValidator


	def writeBlocks(self):
		# Method to write new mined block to blockchain
		dataFile = file(self.fileName, "w")
		chainData = []

		for block in self.chain:
			chainData.append(block.to_dict())

		dataFile.write(json.dumps(chainData, indent = 4))
		dataFile.close()


	def addTransaction(self, transaction):
		if not self._isValidTransaction(transaction):
			return False
		self.transactions.append(transaction)
		return True


	def addOnBlockReadyHandler(self, handler):
		self.onBlockReadyHandler = handler 


	def toJSON(self, inst):
		return json.dumps(inst, default=lambda o: o.__dict__, sort_keys=True, indent=4)


	def _isValidTransaction(self, transaction):
		"""
		Validation of transactions:
		"""
		# Only signed transactions allowed
		if transaction.sign is None:
			return False
		
		# If transaction is already processing
		for tr in self._activeTransactions:
			if (tr.sign == transaction.sign):
				return False
		
		for tr in self.transactions:
			if (tr.sign == transaction.sign):
				return False

		# If transactions is already in the blockchaine
		for block in self.chain:
			for tr in block.transactions:
				if (tr.sign == transaction.sign):
					return False

		return True
		
