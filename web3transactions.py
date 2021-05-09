from web3 import Web3
import json

url = 'http://127.0.0.1:7545'

web3 = Web3(Web3.HTTPProvider(url))

# gas = 2000000

def make_transaction(account_sender, account_reciver, private_key, value, gas):
    nonce = web3.eth.get_transaction_count(account_sender)

    transaction_tx = {
        'nonce' : nonce,
        'to': account_reciver,
        'value': web3.toWei(value, 'ether'),
        'gas': gas,
        'gasPrice': web3.toWei(50, 'gwei')
    } 

    signed_tx = web3.eth.account.sign_transaction(transaction_tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    return web3.toHex(tx_hash)