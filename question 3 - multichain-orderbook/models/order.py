from enum import Enum
from datetime import datetime

class OrderType(Enum):
    """Represents order type (BUY or SELL)"""
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(Enum):
    """Represents the current status of an order"""
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"

class Order:
    """
    Represents a single order in the system.
    """
    
    def __init__(self, id, maker, order_type, base_asset, quote_asset, 
                 base_blockchain, quote_blockchain, amount, price, expiration_time=0):
        """
        Creates a new order for cross-chain trading.
        
        Args:
            id (str): Unique identifier for the order
            maker (str): Address of the order creator
            order_type (OrderType): BUY or SELL
            base_asset (Asset): The asset being sold/bought
            quote_asset (Asset): The asset used for pricing
            base_blockchain (Blockchain): Blockchain where baseAsset exists
            quote_blockchain (Blockchain): Blockchain where quoteAsset exists
            amount (float): Amount of baseAsset to trade
            price (float): Price in quoteAsset per unit of baseAsset
            expiration_time (int, optional): When order expires (0 for no expiration)
        """
        # Validate that we're not trying to trade the same asset on the same blockchain
        if (base_asset.id == quote_asset.id and 
            base_blockchain.id == quote_blockchain.id):
            raise ValueError("Cannot trade the same asset on the same blockchain")
            
        self.id = id
        self.maker = maker
        self.order_type = order_type
        self.base_asset = base_asset
        self.quote_asset = quote_asset
        self.base_blockchain = base_blockchain
        self.quote_blockchain = quote_blockchain
        self.amount = amount
        self.price = price
        self.timestamp = datetime.now().timestamp() * 1000  # milliseconds
        self.status = OrderStatus.PENDING
        self.filled_amount = 0
        self.expiration_time = expiration_time
        
    def get_remaining_amount(self):
        """
        Get the remaining amount to be filled.
        
        Returns:
            float: Remaining amount
        """
        return self.amount - self.filled_amount
        
    def get_total_value(self):
        """
        Get the total value of this order.
        
        Returns:
            float: Total value
        """
        return self.amount * self.price
        
    def get_remaining_value(self):
        """
        Get the remaining value to be filled.
        
        Returns:
            float: Remaining value
        """
        return self.get_remaining_amount() * self.price
        
    def is_expired(self):
        """
        Check if this order is expired.
        
        Returns:
            bool: True if expired
        """
        if self.expiration_time == 0:
            return False
        return datetime.now().timestamp() * 1000 > self.expiration_time
        
    def estimate_gas_cost(self):
        """
        Calculate estimated gas costs for this order.
        
        Returns:
            dict: Gas fees for base and quote blockchains
        """
        base_fee = self.base_blockchain.estimate_gas_fee("FILL_ORDER")
        quote_fee = self.quote_blockchain.estimate_gas_fee("FILL_ORDER")
        
        return {"base_fee": base_fee, "quote_fee": quote_fee}