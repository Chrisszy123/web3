from solcx import compile_standard, install_solc
import json
from web3 import Web3

install_solc("0.6.0")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile the solidity code

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# deploying

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["Storage"]["evm"]["bytecode"][
    "object"
]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["Storage"]["abi"]

# connecting to the local ganache blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # connecting to http provider
chain_id = 1337
my_address = "0x9f6439556EDdEFE72c404ab4e67bd4D74Ec754FD"
private_key = "0x8adaf56c6e8a4c65e10be468e04ef69d776827b0d0855720fa330205f8ae551a"  # remember not to hardcode the private key when deploying live

# creating the contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# build a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
# sign a transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# send a transaction
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
transaction_reciept = w3.eth.wait_for_transaction_receipt(txn_hash)

# working with contract
# you need 2 things
# contract address
# contract abi
simple_storage = w3.eth.contract(address=transaction_reciept.contractAddress, abi=abi)
# call -> simulate a call and getting a value in return
# transact -> making a state change
print(simple_storage.functions.retrieve().call())

# making a transaaction

store_txn = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce
        + 1,  # everytime we make a transaction the nonce has to change or be unique
    }
)
sign_store_txn = w3.eth.account.sign_transaction(store_txn, private_key=private_key)

send_store_txn = w3.eth.send_raw_transaction(sign_store_txn.rawTransaction)
transaction_store_reciept = w3.eth.wait_for_transaction_receipt(send_store_txn)
print(simple_storage.functions.retrieve().call())
