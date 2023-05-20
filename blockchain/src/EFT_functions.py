from web3 import Web3
import json
import binascii

from config import settings

# Web3 provider
w3 = Web3(Web3.HTTPProvider(settings.SEPOLIA_RPC_URL)) # Insert your RPC URL here

# Create variables
account_address = {
    'private_key': f'{settings.PRIVATE_KEY}',
    'address': f'{settings.ACCOUNT_ADDRESS}',
}
contract_address = settings.EFToken_ContractAddress


# Create contract instance
with open('./blockchain/contracts/contracts_EFToken_sol_EFToken.abi', 'r') as f:
    abi = json.load(f)
contract = w3.eth.contract(address=contract_address, abi=abi)

def getOwner():
    return contract.functions.owner().call() 

def uploadPic(
                    _clubID,
                    _activityID,
                    _activityName,
                    _date,
                    _picID,
                    _picNum,
                    _base64,
                    _gas
):
    nonce = w3.eth.get_transaction_count(settings.ACCOUNT_ADDRESS)
    txn = contract.functions.UploadPicture(
                                        _clubID,
                                        _activityID,
                                        _activityName,
                                        _date,
                                        _picID,
                                        _picNum,
                                        _base64
                                        ).build_transaction(
    {
        'from': settings.ACCOUNT_ADDRESS,
        'gas': _gas,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce
    })

    signed_txn = w3.eth.account.sign_transaction(txn, settings.PRIVATE_KEY)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

    return '0x' + binascii.hexlify(txn_hash).decode('utf-8')

def ModifyPicnum_Add(
                    _clubID,
                    _activityID,
                    _activityName,
                    _oldnum,
                    _picID,
                    _picNum,
                    _add
):
    nonce = w3.eth.get_transaction_count(settings.ACCOUNT_ADDRESS)
    txn = contract.functions.ModifyPicnum_Add(
                                        _clubID,
                                        _activityID,
                                        _activityName,
                                        _oldnum,
                                        _picID,
                                        _picNum,
                                        _add
                                        ).build_transaction(
    {
        'from': settings.ACCOUNT_ADDRESS,
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce
    })

    signed_txn = w3.eth.account.sign_transaction(txn, settings.PRIVATE_KEY)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

    return '0x' + binascii.hexlify(txn_hash).decode('utf-8')

def ModifyPicnum_Retake(
                    _clubID,
                    _activityID,
                    _activityName,
                    _oldnum,
                    _picID,
                    _picNum,
                    _add
):
    nonce = w3.eth.get_transaction_count(settings.ACCOUNT_ADDRESS)
    txn = contract.functions.ModifyPicnum_Retake(
                                        _clubID,
                                        _activityID,
                                        _activityName,
                                        _oldnum,
                                        _picID,
                                        _picNum,
                                        _add
                                        ).build_transaction(
    {
        'from': settings.ACCOUNT_ADDRESS,
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce
    })

    signed_txn = w3.eth.account.sign_transaction(txn, settings.PRIVATE_KEY)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

    return '0x' + binascii.hexlify(txn_hash).decode('utf-8')

def BookResource_backend(_clubID, _resourceID, _date):
    nonce = w3.eth.get_transaction_count(settings.ACCOUNT_ADDRESS)
    txn = contract.functions.BookResource_backend(_clubID, _resourceID, _date).build_transaction(
    {
        'from': settings.ACCOUNT_ADDRESS,
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce
    })

    signed_txn = w3.eth.account.sign_transaction(txn, settings.PRIVATE_KEY)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    return '0x' + binascii.hexlify(txn_hash).decode('utf-8')

def CreateClub(_id, _name, _addr):
    nonce = w3.eth.get_transaction_count(settings.ACCOUNT_ADDRESS)
    txn = contract.functions.CreateClub(_id, _name, _addr).build_transaction(
    {
        'from': settings.ACCOUNT_ADDRESS,
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce
    })

    signed_txn = w3.eth.account.sign_transaction(txn, settings.PRIVATE_KEY)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    return '0x' + binascii.hexlify(txn_hash).decode('utf-8')
    
def CreateResource(_id, _name, _cost):
    nonce = w3.eth.get_transaction_count(settings.ACCOUNT_ADDRESS)
    txn = contract.functions.CreateResource(_id, _name, _cost).build_transaction(
    {
        'from': settings.ACCOUNT_ADDRESS,
        'gas': 200000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce
    })

    signed_txn = w3.eth.account.sign_transaction(txn, settings.PRIVATE_KEY)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    return '0x' + binascii.hexlify(txn_hash).decode('utf-8')
    