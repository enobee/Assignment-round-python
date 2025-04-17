from enum import Enum

class OrderType(Enum):
    """
    Order Types Definition
    
    Represents the two possible order directions in the system.
    """
    BUY = "BUY"    # Order to buy an asset
    SELL = "SELL"  # Order to sell an asset

class OrderStatus(Enum):
    """
    Order Status Definition
    
    Represents the possible states of an order throughout its lifecycle.
    """
    PENDING = "PENDING"              # Order created but not yet confirmed on blockchain
    ACTIVE = "ACTIVE"                # Order is active in the order book
    PARTIALLY_FILLED = "PARTIALLY_FILLED"  # Order partially filled
    FILLED = "FILLED"                # Order completely filled
    CANCELLED = "CANCELLED"          # Order was cancelled
    FAILED = "FAILED"                # Order failed (e.g., due to blockchain errors)

class Order:
    """
    Order Class Design
    
    Represents a single order in the multichain orderbook system.
    Each order specifies an exchange between two assets across two blockchains.
    """
    
    def __init__(self, id, maker, order_type, base_asset, quote_asset, 
                 base_blockchain, quote_blockchain, amount, price, expiration_time=0):
        """
        Creates a new order for cross-chain trading
        
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
        # Implementation would:
        # - Validate order parameters (ensure not trading same asset on same blockchain)
        # - Initialize order properties
        # - Set initial status to PENDING
        pass
    
    def get_remaining_amount(self):
        """
        Get the remaining amount to be filled
        
        Used to determine if an order can be matched with another order
        and how much of it can be filled.
        
        Returns:
            float: Remaining amount
        """
        # Implementation would calculate amount - filled_amount
        pass
    
    def get_total_value(self):
        """
        Get the total value of this order
        
        Used to calculate the total potential trade value.
        For example, if buying 10 tokens at 2 USD each, the total value is 20 USD.
        
        Returns:
            float: Total value
        """
        # Implementation would calculate amount * price
        pass
    
    def get_remaining_value(self):
        """
        Get the remaining value to be filled
        
        Similar to get_total_value, but only for the unfilled portion.
        Used to calculate potential partial fills.
        
        Returns:
            float: Remaining value
        """
        # Implementation would calculate get_remaining_amount() * price
        pass
    
    def is_expired(self):
        """
        Check if this order is expired
        
        Orders can have optional time limits. This method checks
        if the current time has passed the expiration time.
        
        Returns:
            bool: True if expired
        """
        # Implementation would check if current time exceeds expiration_time
        pass
    
    def estimate_gas_cost(self):
        """
        Calculate estimated gas costs for this order
        
        Since this is a cross-chain system, we need to calculate gas costs
        on both blockchains involved in the trade.
        
        Returns:
            dict: Gas fees for base and quote blockchains
        """
        # Implementation would get gas fees from both blockchains
        # and return dictionary with both costs
        pass