# Question 1: Ethereum Block Listener - Auto ETH Sender

This python script listens to new blocks on the Ethereum **Sepolia Testnet** using the Alchemy RPC and automatically sends **0.001 ETH** to a specified address **every 10th block**.

## Features

- Connects to Ethereum Sepolia testnet via Alchemy.
- Listens to new blocks in real-time.
- Sends 0.001 ETH to a specified address every 10 blocks.
- Uses `web3.py` for Ethereum interaction.
- Securely handles private key and RPC via `.env`.

## Installation

```bash
pip install -r requirements.txt
```

## Environment Setup

Create a .env file in the root directory and add the following:

```env
ALCHEMY_API_KEY=your_sepolia_api_key_from_alchemy
SENDER_PRIVATE_KEY=your_private_key_without_quotes
RECEIVER_ADDRESS=receiver_wallet_address
```

## Usage

```bash
 python main.py
```

You'll see output like:

```bash
Starting block: 8136576
New Block: 8136577 | Block Count: 1
New Block: 8136578 | Block Count: 2
New Block: 8136579 | Block Count: 3
New Block: 8136580 | Block Count: 4
New Block: 8136581 | Block Count: 5
New Block: 8136582 | Block Count: 6
New Block: 8136583 | Block Count: 7
New Block: 8136584 | Block Count: 8
New Block: 8136585 | Block Count: 9
New Block: 8136586 | Block Count: 10
Sending 0.001 ETH...
Transaction confirmed! Hash: 4e9dbfff936be09cefc0f0368b6b269dc38acf93bca1adab5026442a119109c5

```

## Notes

- Ensure your sender wallet has Sepolia test ETH.
- The gas fee is charged on top of the 0.001 ETH.
- Script runs continuously and listens for new blocks on Sepolia.

## Tech Stack

- Python 3.8+
- web3.py
- python-dotenv
- Alchemy RPC

## License

MIT
