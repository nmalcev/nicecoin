
from blockchain import Blockchain
from block import Block
from wallet import Wallet
from transaction import Transaction

import sys

class Client:
	"""
	Test Client
	Something like Controller.
	Here I create blockchain and wallets
	"""
	def __init__(self):
		"""
		
		"""
		self.wallets = {};
		# Initialise wallets of participaters
		# And give 100 Nicecoins to each of them
		self.walletA = self.registerWallet(Wallet(100))
		self.walletB = self.registerWallet(Wallet(100))
		
		
		# Init Nicecoin BlockChain
		genesisBlock = Block([], 0)
		self.blockchain = Blockchain(genesisBlock)
		
		# It is handler that will execute when transaction will be succeeded
		def onBlockReadyHandler(transactions):
			print("[Transacton completed]")
			for transaction in transactions:
				wallet = self.wallets[transaction.recipient_address] 

				if (wallet is not None):
					print("W: %s gain: %d" % (transaction.recipient_address, transaction.amount))
					wallet.amount = wallet.amount + transaction.amount
			self.debug()
 	
		self.blockchain.addOnBlockReadyHandler(onBlockReadyHandler)

	def initTransactions(self):
		# Create transfers between wallets
		# Add transactions in blockchain
		self.debug()
		self.trans1 = self.walletA.transfer(self.walletB.address, 10)
		self.trans2 = self.walletB.transfer(self.walletA.address, 20)
		trans3 = self.walletB.transfer(self.walletA.address, 5)

		# The transacton instance may be equal to None if there wer not enough money in wallet
		if self.trans1 != None and self.blockchain.addTransaction(self.trans1):
			print "Trans1 was successfully added"
		if self.trans2 != None and self.blockchain.addTransaction(self.trans2):
			print "Trans2 was successfully added"
		if trans3 != None and self.blockchain.addTransaction(trans3):
			print "Trans3 was successfully added"
		
		self.examineDuplicationTransactions()
		# Display changes in wallets 
		self.debug()
		# Try to add trans1 

	def examineDuplicationTransactions(self):
		# Examine duplications
		if self.trans2 != None and self.blockchain.addTransaction(self.trans2):
			# Fail
			print "Copy of Trans2 was successfully added!!!"
		else:
			print "Copy of Trans2 was rejected"
		
	
	def addBlock(self):
		block, computeTime = self.blockchain.addBlock()
		print("[Add Block] # %d %s %f" % (block.index, block.hash, computeTime))
		self.debug()

	
	def debug(self):
		print("[D] A: %d NC, B: %d NC, #trans: %d" % 
			(self.walletA.amount, self.walletB.amount, len(self.blockchain.transactions))
		)

	
	def dump(self):
		print("[Blockchain]")
		for block in self.blockchain.chain:
			print("# %d %s" % (block.index, block.hash))


	def registerWallet(self, wallet):
		self.wallets[wallet.address] = wallet	
		return wallet	


if __name__ == '__main__':	
	client = Client()
	client.initTransactions()
	client.addBlock()
	client.examineDuplicationTransactions()
	client.dump()





