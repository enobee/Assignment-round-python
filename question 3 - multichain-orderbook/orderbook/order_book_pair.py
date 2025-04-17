from models.order import OrderType, OrderStatus

class OrderBookPair:
    """
    Represents the order book for a specific trading pair.
    """
    
    def __init__(self, base_asset, quote_asset, base_blockchain, quote_blockchain):
        """
        Creates a new order book for a specific trading pair.
        
        Args:
            base_asset (Asset): Base asset in the trading pair
            quote_asset (Asset): Quote asset in the trading pair
            base_blockchain (Blockchain): Blockchain for the base asset
            quote_blockchain (Blockchain): Blockchain for the quote asset
        """
        # Validate that we're not trying to trade the same asset on the same blockchain
        if (base_asset.id == quote_asset.id and 
            base_blockchain.id == quote_blockchain.id):
            raise ValueError("Cannot trade the same asset on the same blockchain")
            
        self.base_asset = base_asset
        self.quote_asset = quote_asset
        self.base_blockchain = base_blockchain
        self.quote_blockchain = quote_blockchain
        self.buy_orders = []
        self.sell_orders = []
        
    def add_order(self, order):
        """
        Add an order to the order book.
        
        Args:
            order (Order): Order to add
        """
        # Validate that the order matches this pair
        if (order.base_asset.id != self.base_asset.id or
            order.quote_asset.id != self.quote_asset.id or
            order.base_blockchain.id != self.base_blockchain.id or
            order.quote_blockchain.id != self.quote_blockchain.id):
            raise ValueError("Order does not match this order book pair")
            
        # Add to appropriate list and sort
        if order.order_type == OrderType.BUY:
            self.buy_orders.append(order)
            # Sort buy orders by price (highest first) and then by timestamp
            self.buy_orders.sort(key=lambda x: (-x.price, x.timestamp))
        else:
            self.sell_orders.append(order)
            # Sort sell orders by price (lowest first) and then by timestamp
            self.sell_orders.sort(key=lambda x: (x.price, x.timestamp))
            
    def remove_order(self, order_id):
        """
        Remove an order from the order book.
        
        Args:
            order_id (str): ID of order to remove
            
        Returns:
            bool: True if order was found and removed
        """
        # Try to remove from buy orders
        for i, order in enumerate(self.buy_orders):
            if order.id == order_id:
                self.buy_orders.pop(i)
                return True
                
        # Try to remove from sell orders
        for i, order in enumerate(self.sell_orders):
            if order.id == order_id:
                self.sell_orders.pop(i)
                return True
                
        return False
        
    def find_matching_orders(self, taker_order):
        """
        Find matching orders for a taker order.
        
        Args:
            taker_order (Order): Taker order to match
            
        Returns:
            list: List of matching orders
        """
        if taker_order.order_type == OrderType.BUY:
            # For a buy order, find sell orders with price <= taker price
            return [
                order for order in self.sell_orders
                if (order.status == OrderStatus.ACTIVE and
                    order.price <= taker_order.price and
                    not order.is_expired())
            ]
        else:
            # For a sell order, find buy orders with price >= taker price
            return [
                order for order in self.buy_orders
                if (order.status == OrderStatus.ACTIVE and
                    order.price >= taker_order.price and
                    not order.is_expired())
            ]
            
    def has_enough_liquidity(self, taker_order):
        """
        Check if there is enough liquidity to fill a taker order.
        
        Args:
            taker_order (Order): Taker order to check
            
        Returns:
            bool: True if enough liquidity is available
        """
        matching_orders = self.find_matching_orders(taker_order)
        total_available = sum(order.get_remaining_amount() for order in matching_orders)
        
        return total_available >= taker_order.amount