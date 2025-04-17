import os
import asyncio
from dotenv import load_dotenv
from web3 import Web3
from swap import swap_on_uniswap, swap_on_curve
from eth_account import Account

load_dotenv()

# Load environment variables
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ARBITRUM_RPC = os.getenv("ARBITRUM_RPC")
OPTIMISM_RPC = os.getenv("OPTIMISM_RPC")

# Set up providers
arbitrum = Web3(Web3.HTTPProvider(f"https://arb-mainnet.g.alchemy.com/v2/{ARBITRUM_RPC}"))
optimism = Web3(Web3.HTTPProvider(f"https://opt-mainnet.g.alchemy.com/v2/{OPTIMISM_RPC}"))

# Wallet setup
acct = Account.from_key(PRIVATE_KEY)
wallet_address = acct.address

# Contract addresses
UNISWAP_ROUTER = "0xE592427A0AEce92De3Edee1F18E0157C05861564"
CURVE_POOL = "0x45c562b0a4e2efc8768315e4eced54c46041f657"

USDC_ARBITRUM = "0xff970a61a04b1ca14834a43f5de4533ebddb5cc8"
USDT_ARBITRUM = "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9"

async def run_uniswap_swap():
    try:
        amount_in = Web3.to_wei(5, 'mwei')  # USDC has 6 decimals
        tx = swap_on_uniswap(arbitrum, acct, UNISWAP_ROUTER, USDC_ARBITRUM, USDT_ARBITRUM, amount_in)
        print(f"Uniswap Swap TX: {tx}")
        return tx
    except Exception as e:
        print(f"Uniswap swap failed: {str(e)}")
        return None

async def run_curve_swap():
    try:
        amount_in = Web3.to_wei(5, 'mwei')
        tx = swap_on_curve(optimism, acct, CURVE_POOL, amount_in)
        print(f"Curve Swap TX: {tx}")
        return tx
    except Exception as e:
        print(f"Curve swap failed: {str(e)}")
        return None

async def main():
    print("Starting crosschain swaps simultaneously...")

    # Run both swaps concurrently
    uniswap_task = asyncio.create_task(run_uniswap_swap())
    curve_task = asyncio.create_task(run_curve_swap())

    # Wait for both to complete
    tx1, tx2 = await asyncio.gather(uniswap_task, curve_task)

    print("All swaps attempted.")
    if tx1:
        print(f"Uniswap TX hash: {tx1}")
    if tx2:
        print(f"Curve TX hash: {tx2}")
    return tx1, tx2

if __name__ == "__main__":
    asyncio.run(main())
