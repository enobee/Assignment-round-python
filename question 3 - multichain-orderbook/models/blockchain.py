class Blockchain:
    """
    Represents a blockchain and its properties.
    """
    
    def __init__(self, id, name, average_block_time, gas_estimator):
        """
        Creates a new blockchain instance.
        
        Args:
            id (str): Unique identifier for the blockchain
            name (str): Human-readable name (e.g., "Ethereum")
            average_block_time (int): Average seconds for a new block
            gas_estimator (callable): Function to estimate current gas price
        """
        self.id = id
        self.name = name
        self.average_block_time = average_block_time
        self.gas_estimator = gas_estimator
        self.provider = None
        
    def estimate_gas_fee(self, operation_type):
        """
        Estimates gas fee for different operation types.
        
        Args:
            operation_type (str): Type of operation (PLACE_ORDER, CANCEL_ORDER, etc.)
            
        Returns:
            float: Estimated gas fee in native currency units
        """
        # Get current gas price
        current_gas_price = self.gas_estimator()
        
        # Get gas limit for this operation type
        gas_limit = self.get_operation_gas_limit(operation_type)
        
        # Calculate base gas fee
        gas_fee = current_gas_price * gas_limit
        
        # Apply safety buffer (10%)
        return gas_fee * 1.1
    
    def get_operation_gas_limit(self, operation):
        """
        Get gas limit for different operations.
        
        Args:
            operation (str): Operation type
            
        Returns:
            int: Gas limit in gas units
        """
        gas_limits = {
            "PLACE_ORDER": 120000,
            "CANCEL_ORDER": 80000,
            "FILL_ORDER": 180000,
            "TRANSFER_ASSET": 65000,
            "DEFAULT": 100000
        }
        
        return gas_limits.get(operation, gas_limits["DEFAULT"])
    
    def get_provider(self):
        """
        Get a provider for connecting to this blockchain.
        
        Returns:
            object: Provider for this blockchain
        """
        if not self.provider:
            # In a real implementation, this would initialize a real provider
            self.provider = {"blockchain": self.id}  # Mock provider
            
        return self.provider