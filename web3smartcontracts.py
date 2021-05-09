from web3 import Web3 
import json 

url = "http://127.0.0.1:7545"

web3 = Web3(Web3.HTTPProvider(url))

web3.eth.defaultAccount = web3.eth.accounts[0]

abi = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "num2",
				"type": "uint256"
			}
		],
		"name": "buy_coin",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "num3",
				"type": "uint256"
			}
		],
		"name": "sell_coin",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "num",
				"type": "uint256"
			}
		],
		"name": "store",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "retrieve",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

bytecode = "608060405234801561001057600080fd5b506102b6806100206000396000f3fe608060405234801561001057600080fd5b506004361061004c5760003560e01c80632e64cec11461005157806354987b881461006f5780636057361d1461009f578063dce36c35146100bb575b600080fd5b6100596100eb565b604051610066919061018b565b60405180910390f35b61008960048036038101906100849190610153565b6100f4565b604051610096919061018b565b60405180910390f35b6100b960048036038101906100b49190610153565b610114565b005b6100d560048036038101906100d09190610153565b61011e565b6040516100e2919061018b565b60405180910390f35b60008054905090565b60008160005461010491906101fc565b6000819055506000549050919050565b8060008190555050565b60008160005461012e91906101a6565b6000819055506000549050919050565b60008135905061014d81610269565b92915050565b60006020828403121561016557600080fd5b60006101738482850161013e565b91505092915050565b61018581610230565b82525050565b60006020820190506101a0600083018461017c565b92915050565b60006101b182610230565b91506101bc83610230565b9250827fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff038211156101f1576101f061023a565b5b828201905092915050565b600061020782610230565b915061021283610230565b9250828210156102255761022461023a565b5b828203905092915050565b6000819050919050565b7f4e487b7100000000000000000000000000000000000000000000000000000000600052601160045260246000fd5b61027281610230565b811461027d57600080fd5b5056fea2646970667358221220c546790336608b159f62d090d725e0ea97b38037da8e945b660926f4cf511fbb64736f6c63430008010033"


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

# print("done")
# storevalue(0)
# buy_coinvalue(10)
# sell_coinvalue(5)
# print(retrievevalue())