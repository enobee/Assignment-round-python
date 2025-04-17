from datetime import datetime

class OrderMatch:
    """
    Represents a match between a taker order and one or more maker orders.
    """
    
    def __init__(self, id, taker_order):
        """
        Creates a new order match instance.
        
        Args:
            id (str): Unique identifier for the match
            taker_order (Order): The taker order that initiated this match
        """
        self.id = id
        self.taker_order = taker_order
        self.maker_orders = []  
        self.status = "PENDING"
        self.timestamp = datetime.now().timestamp() * 1000
        
    def add_maker_order(self, maker_order, fill_amount):
        """
        Add a maker order to this match.
        
        Args:
            maker_order (Order): The maker order to include
            fill_amount (float): Amount of the maker order to fill
        """
        self.maker_orders.append({
            "order": maker_order,
            "fill_amount": fill_amount
        })
        
    def get_total_fill_amount(self):
        """
        Get the total fill amount across all maker orders.
        
        Returns:
            float: Total fill amount
        """
        return sum(item["fill_amount"] for item in self.maker_orders)
        
    def estimate_total_gas_cost(self):
        """
        Calculate total gas costs across all blockchains involved.
        
        Returns:
            float: Total gas cost
        """
        # Get unique blockchains involved
        blockchains = set()
        blockchains.add(self.taker_order.base_blockchain)
        blockchains.add(self.taker_order.quote_blockchain)
        
        for item in self.maker_orders:
            blockchains.add(item["order"].base_blockchain)
            blockchains.add(item["order"].quote_blockchain)
        
        # Calculate total gas
        total_gas = 0
        for blockchain in blockchains:
            total_gas += blockchain.estimate_gas_fee("FILL_ORDER")
            
        return total_gas