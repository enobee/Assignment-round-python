import logging
from models.order import OrderStatus

class CrossChainManager:
    """
    Handles cross-chain communication and transaction execution.
    """
    
    def __init__(self, order_book):
        """
        Creates a new cross-chain manager instance.
        
        Args:
            order_book (MultiChainOrderBook): The orderbook instance
        """
        self.order_book = order_book
        self.bridges = {}  # Maps blockchain pair keys to bridge implementations
        
    def register_bridge(self, source_chain_id, dest_chain_id, bridge):
        """
        Register a bridge for a specific blockchain pair.
        
        Args:
            source_chain_id (str): ID of source blockchain
            dest_chain_id (str): ID of destination blockchain
            bridge (object): Bridge implementation
        """
        key = f"{source_chain_id}_{dest_chain_id}"
        self.bridges[key] = bridge
        
    def get_bridge(self, source_chain_id, dest_chain_id):
        """
        Get the appropriate bridge for a blockchain pair.
        
        Args:
            source_chain_id (str): ID of source blockchain
            dest_chain_id (str): ID of destination blockchain
            
        Returns:
            object: Bridge implementation or None
        """
        key = f"{source_chain_id}_{dest_chain_id}"
        return self.bridges.get(key)
        
    async def execute_match(self, match):
        """
        Execute a matched order.
        
        Args:
            match (OrderMatch): The match to execute
            
        Returns:
            bool: True if successful
        """
        # Calculate total gas costs to ensure the trade is profitable
        gas_cost = match.estimate_total_gas_cost()
        total_value = match.taker_order.get_total_value()
        
        # Check if the trade is worth executing (address constraint #3: Gas Fees)
        MAX_GAS_PERCENT = 0.05  # 5%
        if gas_cost > total_value * MAX_GAS_PERCENT:
            logging.info(f"Trade rejected: Gas cost too high ({gas_cost} vs {total_value})")
            return False
            
        # Structure to track the execution state
        execution_state = {
            "locked_assets": []
        }
        
        try:
            # Implement cross-chain trade execution (address constraint #1: Immediate Order Fulfillment)
            # 1. Lock assets on source chains
            # 2. Generate proofs of the locks
            # 3. Release assets on destination chains
            
            # For this implementation, we'll just simulate success
            # In a real system, this would interact with actual bridges
            
            # Update order statuses
            self.update_order_statuses(match)
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to execute match: {e}")
            
            # If we locked any assets but failed later, try to unlock them
            if execution_state["locked_assets"]:
                logging.info("Attempting to unlock assets after failure")
                # In a real system, would call unlock methods on bridges
                
            return False
    
    def update_order_statuses(self, match):
        """
        Update order statuses after a successful match.
        
        Args:
            match (OrderMatch): The completed OrderMatch
        """
        # Update taker order
        match.taker_order.filled_amount += match.get_total_fill_amount()
        if match.taker_order.filled_amount >= match.taker_order.amount:
            match.taker_order.status = OrderStatus.FILLED
        else:
            match.taker_order.status = OrderStatus.PARTIALLY_FILLED
        
        # Update maker orders
        for item in match.maker_orders:
            maker_order = item["order"]
            fill_amount = item["fill_amount"]
            
            maker_order.filled_amount += fill_amount
            if maker_order.filled_amount >= maker_order.amount:
                maker_order.status = OrderStatus.FILLED
                
                # Remove filled orders from the order book
                order_book_key = (f"{maker_order.base_asset.id}_{maker_order.quote_asset.id}_"
                                 f"{maker_order.base_blockchain.id}_{maker_order.quote_blockchain.id}")
                order_book = self.order_book.order_books.get(order_book_key)
                if order_book:
                    order_book.remove_order(maker_order.id)
            else:
                maker_order.status = OrderStatus.PARTIALLY_FILLED
    
    async def submit_maker_order(self, order):
        """
        Submit a maker order to the blockchain.
        
        Args:
            order (Order): Order to submit
            
        Returns:
            bool: True if successful
        """
        try:
            # In a real implementation, this would submit to the blockchain
            # For this exercise, we'll just mark it as active
            order.status = OrderStatus.ACTIVE
            
            # Add to the order book
            order_book = self.order_book.get_or_create_order_book(
                order.base_asset.id,
                order.quote_asset.id,
                order.base_blockchain.id,
                order.quote_blockchain.id
            )
            
            order_book.add_order(order)
            return True
        except Exception as e:
            logging.error(f"Failed to submit maker order: {e}")
            order.status = OrderStatus.FAILED
            return False
    
    async def process_taker_order(self, order):
        """
        Process a taker order immediately.
        
        Args:
            order (Order): Taker order to process
            
        Returns:
            bool: True if successful
        """
        # Find matching orders
        match = self.order_book.process_taker_order(order)
        
        # Check if we found enough liquidity (address constraint #2: Liquidity Challenges)
        if match.get_total_fill_amount() < order.amount:
            logging.info(f"Insufficient liquidity: Found {match.get_total_fill_amount()} of {order.amount}")
            
            # Options for handling insufficient liquidity:
            # 1. Reject the order completely
            # 2. Fill what we can and convert the rest to a maker order
            # 3. Fill what we can and return the rest
            
            # For this implementation, we'll use option 1: reject the order
            return False
        
        # Execute the match (this addresses constraint #1: Immediate Order Fulfillment)
        return await self.execute_match(match)