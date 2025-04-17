import json

def load_abi(file_path):
    with open(file_path, "r") as file:
        return json.load(file)
    
def approve_token(web3, account, token_address, spender_address, amount):
    abi = load_abi("abis/erc20_abi.json")
    token_contract = web3.eth.contract(address=token_address, abi=abi)

    txn = token_contract.functions.approve(spender_address, amount).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 100000,
        'gasPrice': web3.to_wei('2', 'gwei')
    })

    signed_txn = web3.eth.account.sign_transaction(txn, account.key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    return tx_hash.hex()


def swap_on_uniswap(web3, account, router_address, token_in, token_out, amount_in):
    abi = load_abi("abis/uniswap_router_abi.json")
    contract = web3.eth.contract(address=router_address, abi=abi)

    recipient = account.address
    deadline = web3.eth.get_block('latest')['timestamp'] + 300

    params = {
        "tokenIn": token_in,
        "tokenOut": token_out,
        "fee": 500,
        "recipient": recipient,
        "deadline": deadline,
        "amountIn": amount_in,
        "amountOutMinimum": 0,
        "sqrtPriceLimitX96": 0
    }

    txn = contract.functions.exactInputSingle(params).build_transaction({
        'from': recipient,
        'nonce': web3.eth.get_transaction_count(recipient),
        'gas': 500000,
        'gasPrice': web3.to_wei('2', 'gwei'),
        'value': 0
    })

    signed_txn = web3.eth.account.sign_transaction(txn, account.key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    return tx_hash.hex()

def swap_on_curve(web3, account, pool_address, amount_in):
    abi = load_abi("abis/curve_pool_abi.json")
    contract = web3.eth.contract(address=pool_address, abi=abi)

    i = 2  # USDT
    j = 1  # USDC

    txn = contract.functions.exchange(i, j, amount_in, 0).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 500000,
        'gasPrice': web3.to_wei('2', 'gwei'),
    })

    signed_txn = web3.eth.account.sign_transaction(txn, account.key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    return tx_hash.hex()
