
import asyncio
from models.blockchain import Blockchain
from models.asset import Asset
from models.order import Order, OrderType
from orderbook.multi_chain_order_book import MultiChainOrderBook
from execution.cross_chain_manager import CrossChainManager


class MockBridge:
    async def lock_assets(self, source_chain, asset, amount, sender, recipient):
        print(f"Locking {amount} of {asset.symbol} on {source_chain.name}")
        return {"success": True, "txHash": "txHash"}
        
    async def generate_proof(self, source_chain, tx_hash, confirmations):
        print(f"Generating proof for {tx_hash} on {source_chain.name}")
        return {"success": True, "proof": {"data": "proofData"}}
        
    async def release_assets(self, dest_chain, asset, amount, recipient, proof):
        print(f"Releasing {amount} of {asset.symbol} on {dest_chain.name} to {recipient}")
        return {"success": True, "txHash": "txHash"}

async def main():
    # Create blockchains
    ethereum = Blockchain("ethereum", "Ethereum", 15, lambda: 50)
    polygon = Blockchain("polygon", "Polygon", 2, lambda: 20)
    
    # Create assets
    eth = Asset("eth", "ETH", "Ethereum", 18)
    eth.add_blockchain_address("ethereum", "0xED7Be1ef41acE718c127A9D922f13E6DB0f751bBe")
    
    usdc = Asset("usdc", "USDC", "USD Coin", 6)
    usdc.add_blockchain_address("ethereum", "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
    usdc.add_blockchain_address("polygon", "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")
    
    # Create order book system
    order_book = MultiChainOrderBook()
    order_book.add_blockchain(ethereum)
    order_book.add_blockchain(polygon)
    order_book.add_asset(eth)
    order_book.add_asset(usdc)
    
    # Create cross-chain manager
    manager = CrossChainManager(order_book)
    
    # Register bridge
    bridge = MockBridge()
    manager.register_bridge("ethereum", "polygon", bridge)
    
    # Create a maker order: Sell 1 ETH for 2000 USDC
    maker_order = Order(
        id="order1",
        maker="0x37BD277C66CdD61bD788825B19A40A5FA3400376",
        order_type=OrderType.SELL,
        base_asset=eth,
        quote_asset=usdc,
        base_blockchain=ethereum,
        quote_blockchain=polygon,
        amount=1.0,
        price=2000.0
    )
    
    # Submit maker order
    await manager.submit_maker_order(maker_order)
    print(f"Maker order status: {maker_order.status}")
    
    # Create a taker order: Buy 0.5 ETH with 1000 USDC
    taker_order = Order(
        id="order2",
        maker="0x9EF3Db7CaF7A6ec9f8e6950b62e255B28275dE86",
        order_type=OrderType.BUY,
        base_asset=eth,
        quote_asset=usdc,
        base_blockchain=ethereum,
        quote_blockchain=polygon,
        amount=0.5,
        price=2100.0  
    )
    
    # Process taker order
    result = await manager.process_taker_order(taker_order)
    print(f"Taker order execution result: {result}")
    print(f"Taker order status: {taker_order.status}")
    print(f"Maker order fill amount: {maker_order.filled_amount}")
    print(f"Maker order status: {maker_order.status}")

if __name__ == "__main__":
    asyncio.run(main())