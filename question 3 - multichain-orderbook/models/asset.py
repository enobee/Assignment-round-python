
class Asset:
    """
    Asset Class Design
    
    Represents a tradable asset (token) that exists across multiple blockchains.
    Each asset has a consistent identity but different contract addresses on different chains.
    """
    
    def __init__(self, id, symbol, name, decimals):
        """
        Creates a new asset with its basic properties
        
        Args:
            id (str): Unique identifier for the asset
            symbol (str): Symbol/ticker of the asset (e.g., "ETH", "SOL")
            name (str): Full name of the asset (e.g., "Bitcoin", "Ethereum")
            decimals (int): Number of decimal places for precision
        """
        # Store basic asset properties
        # Initialize dictionary to store addresses on different blockchains
        pass
    
    def add_blockchain_address(self, blockchain_id, contract_address):
        """
        Register this asset's contract address on a specific blockchain
        
        For example, registering USDC's address on Ethereum and Polygon:
        - add_blockchain_address("ethereum", "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
        - add_blockchain_address("polygon", "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")
        
        Args:
            blockchain_id (str): ID of the blockchain
            contract_address (str): Contract address on that blockchain
        """
        # Store the address in the dictionary using blockchain ID as key
        pass
    
    def get_address_on_blockchain(self, blockchain_id):
        """
        Retrieve this asset's contract address on a specific blockchain
        
        Used when constructing transactions or queries involving this asset
        on a particular blockchain.
        
        Args:
            blockchain_id (str): ID of the blockchain
            
        Returns:
            str: Contract address or None if not registered
        """
        # Retrieve address from the dictionary using blockchain ID as key
        pass