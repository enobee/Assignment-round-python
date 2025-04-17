from datetime import datetime
from models.order_match import OrderMatch

class MultiChainOrderBook:
    """
    Central orderbook system that manages trading pairs across multiple blockchains.
    """
    
    def __init__(self):
        """
        Creates a new multichain order book system.
        """
        self.order_books = {}  # Maps trading pair keys to OrderBookPair objects
        self.supported_blockchains = {}  # Maps blockchain IDs to Blockchain objects
        self.supported_assets = {}  # Maps asset IDs to Asset objects
        
    def add_blockchain(self, blockchain):
        """
        Add a supported blockchain.
        
        Args:
            blockchain (Blockchain): Blockchain to add
        """
        self.supported_blockchains[blockchain.id] = blockchain
        
    def add_asset(self, asset):
        """
        Add a supported asset.
        
        Args:
            asset (Asset): Asset to add
        """
        self.supported_assets[asset.id] = asset
        
    def get_or_create_order_book(self, base_asset_id, quote_asset_id, 
                                base_blockchain_id, quote_blockchain_id):
        """
        Create an order book for a trading pair if it doesn't exist.
        
        Args:
            base_asset_id (str): ID of base asset
            quote_asset_id (str): ID of quote asset
            base_blockchain_id (str): ID of base blockchain
            quote_blockchain_id (str): ID of quote blockchain
            
        Returns:
            OrderBookPair: Order book for this trading pair
        """
        # Get assets and blockchains
        base_asset = self.supported_assets.get(base_asset_id)
        quote_asset = self.supported_assets.get(quote_asset_id)
        base_blockchain = self.supported_blockchains.get(base_blockchain_id)
        quote_blockchain = self.supported_blockchains.get(quote_blockchain_id)
        
        if not all([base_asset, quote_asset, base_blockchain, quote_blockchain]):
            raise ValueError("Invalid asset or blockchain")
            
        # Create a unique key for this trading pair
        key = f"{base_asset_id}_{quote_asset_id}_{base_blockchain_id}_{quote_blockchain_id}"
        
        # Check if we already have this order book
        if key not in self.order_books:
            # Import here to avoid circular import
            from orderbook.order_book_pair import OrderBookPair
            
            # Create a new order book pair
            order_book = OrderBookPair(
                base_asset,
                quote_asset,
                base_blockchain,
                quote_blockchain
            )
            self.order_books[key] = order_book
            
        return self.order_books[key]
        
    def process_taker_order(self, taker_order):
        """
        Process a taker order and try to find matching maker orders.
        
        Args:
            taker_order (Order): Taker order to process
            
        Returns:
            OrderMatch: Match object with matching maker orders
        """
        # Create a unique ID for this match
        match_id = f"match_{int(datetime.now().timestamp() * 1000)}_{taker_order.id}"
        match = OrderMatch(match_id, taker_order)
        
        # Get the appropriate order book
        order_book_key = (f"{taker_order.base_asset.id}_{taker_order.quote_asset.id}_"
                         f"{taker_order.base_blockchain.id}_{taker_order.quote_blockchain.id}")
        order_book = self.order_books.get(order_book_key)
        
        if not order_book:
            # No order book exists for this pair, so there are no matches
            return match
            
        # Find matching orders
        matching_orders = order_book.find_matching_orders(taker_order)
        remaining_amount = taker_order.amount
        
        # Fill orders until the taker order is completely filled or we run out of matches
        for maker_order in matching_orders:
            if remaining_amount <= 0:
                break
                
            fill_amount = min(remaining_amount, maker_order.get_remaining_amount())
            match.add_maker_order(maker_order, fill_amount)
            
            remaining_amount -= fill_amount
            
        return match