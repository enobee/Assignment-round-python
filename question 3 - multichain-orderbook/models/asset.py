class Asset:
    """
    Represents a tradable asset that exists across multiple blockchains.
    """
    
    def __init__(self, id, symbol, name, decimals):
        """
        Creates a new asset with its basic properties.
        
        Args:
            id (str): Unique identifier for the asset
            symbol (str): Symbol/ticker of the asset (e.g., "BTC")
            name (str): Full name of the asset (e.g., "Bitcoin")
            decimals (int): Number of decimal places for precision
        """
        self.id = id
        self.symbol = symbol
        self.name = name
        self.decimals = decimals
        self.addresses = {}  # Maps blockchain ID to contract address
        
    def add_blockchain_address(self, blockchain_id, contract_address):
        """
        Register this asset's contract address on a specific blockchain.
        
        Args:
            blockchain_id (str): ID of the blockchain
            contract_address (str): Contract address on that blockchain
        """
        self.addresses[blockchain_id] = contract_address
        
    def get_address_on_blockchain(self, blockchain_id):
        """
        Retrieve this asset's contract address on a specific blockchain.
        
        Args:
            blockchain_id (str): ID of the blockchain
            
        Returns:
            str: Contract address or None if not registered
        """
        return self.addresses.get(blockchain_id)