# Nicecoin - a Bitcoin blockchain copy

This repository contains a  Nicecoin blockchain. 

### Basics

The proof of work computation, is closer to the Bitcoin implementation. The application searchs a [nonce](https://en.bitcoin.it/wiki/Nonce) that will produce a hash of block with 10 leading zeros.

The algorithm in NiceCoin implements a Proof of Work consensus algorithm. This principle is used to to create distributed trustless consensus and solve the double-spend problem. The Proof of Work means that miner for the verification need to demonstrate a piece of data which is difficult to produce but easy for others to verify and which satisfies certain requirements. In current case the proof is a hash with 10 leading zeros (target difficulty).

I have created the Wallet class (wallet.py) that is able to identify each user.
Key features:
1. Each wallet has unique address;
2. It creates private and public keys for each wallet;
3. Wallet class provides a `transfer()` method responsible for creation signed transactions.

In Nicecoin the double spending is impossible because:
1. Since user has created a transaction the user’s assets are decreased on the amount of transaction;
2. The transaction cannot be added and existing more than in one block.


Nicecoin supports multiple transactions and Merkle tree in Block in the script block.py.

### Dependencies
``` shell	
pip install -r requirements.txt
```

### Execution
``` shell
python app.py
```
