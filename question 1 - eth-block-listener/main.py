import os
import time
import logging
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account

# Load environment variables
load_dotenv()

ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")
SENDER_PRIVATE_KEY = os.getenv("SENDER_PRIVATE_KEY")
RECEIVER_ADDRESS = os.getenv("RECEIVER_ADDRESS")

# Logging config
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Validate environment variables
if not all([ALCHEMY_API_KEY, SENDER_PRIVATE_KEY, RECEIVER_ADDRESS]):
    logging.error("One or more environment variables are missing. Please check your .env file.")
    exit(1)

try:
    provider_url = f"https://eth-sepolia.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
    w3 = Web3(Web3.HTTPProvider(provider_url))

    if not w3.is_connected():
        raise ConnectionError("Failed to connect to the Ethereum network.")
except Exception as e:
    logging.error(f"Error initializing Web3: {e}")
    exit(1)

# Wallet setup
try:
    account = Account.from_key(SENDER_PRIVATE_KEY)
    logging.info(f"Connected wallet: {account.address}")
except Exception as e:
    logging.error(f"Invalid private key: {e}")
    exit(1)

# Block listener with send logic
block_count = 0
try:
    current_block = w3.eth.block_number
    logging.info(f"Starting block: {current_block}")

    while True:
        latest_block = w3.eth.block_number
        if latest_block > current_block:
            block_count += 1
            current_block = latest_block
            logging.info(f"New Block: {latest_block} | Block Count: {block_count}")

            if block_count % 10 == 0:
                try:
                    nonce = w3.eth.get_transaction_count(account.address)
                    gas_price = w3.eth.gas_price
                    tx = {
                        'to': Web3.to_checksum_address(RECEIVER_ADDRESS),
                        'value': w3.to_wei(0.001, 'ether'),
                        'gas': 21000,
                        'gasPrice': gas_price,
                        'nonce': nonce,
                        'chainId': 11155111  # Sepolia chain ID
                    }

                    signed_tx = w3.eth.account.sign_transaction(tx, private_key=SENDER_PRIVATE_KEY)
                    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                    logging.info("Sending 0.001 ETH...")
                    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                    logging.info(f"Transaction confirmed! Hash: {tx_hash.hex()}")

                except Exception as tx_err:
                    logging.error(f"Transaction error: {tx_err}")

        time.sleep(2)  # Poll every 2 seconds

except KeyboardInterrupt:
    logging.warning("Script stopped manually.")
except Exception as e:
    logging.error(f"Unexpected error occurred: {e}")
