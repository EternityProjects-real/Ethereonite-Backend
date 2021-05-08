## smart contracts to talk to the wallets and stuff 
## work to do 
## Complie solidity code get abi and bytecode 
## inject to web3

from web3 import Web3 
import json 

url = "http://127.0.0.1:7545"

web3 = Web3(Web3.HTTPProvider(url))

web3.eth.defaultAccount = web3.eth.accounts[0]

abi = ""

bytecode = ""

SmartContactsongo = web3.eth.contract(abi = abi, bytecode = bytecode)

tx_hash = SmartContactsongo.constructor().transact()

tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

# print(tx_hash)

contract = web3.eth.contract(abi = abi, address = tx_receipt.contractAddress)

# print(contract.functions.retrieve().call())

def storevalue(num):
    tx_hash = contract.functions.store(num).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return (contract.functions.retrieve().call())


def retrievevalue():
    return (contract.functions.retrieve().call())


def buy_coinvalue(num):
    tx_hash = contract.functions.buy_coin(num).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return (contract.functions.retrieve().call())


def sell_coinvalue(num):
    tx_hash = contract.functions.sell_coin(num).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    return (contract.functions.retrieve().call())