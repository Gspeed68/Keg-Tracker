"""
Blockchain and NFT functionality for Keg Tracker.

This module handles:
- Connecting to Ethereum blockchain
- Creating NFT metadata
- Minting NFTs for kegs
- Managing wallet interactions
"""

import os
from web3 import Web3
from dotenv import load_dotenv
import json
from PIL import Image
import requests
from datetime import datetime

# Load environment variables
load_dotenv()

class KegNFT:
    def __init__(self):
        # Initialize Web3 connection (using Infura as an example)
        self.infura_url = os.getenv('INFURA_URL')
        self.w3 = Web3(Web3.HTTPProvider(self.infura_url))
        
        # Load contract ABI and address
        self.contract_address = os.getenv('CONTRACT_ADDRESS')
        with open('KegNFT.json', 'r') as f:
            self.contract_abi = json.load(f)
        
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )
        
        # Set up account
        self.account = os.getenv('WALLET_ADDRESS')
        self.private_key = os.getenv('PRIVATE_KEY')

    def create_keg_metadata(self, keg_id, keg_type, location, status):
        """
        Create metadata for the keg NFT.
        
        Args:
            keg_id: Unique identifier for the keg
            keg_type: Type of keg (Sixtel or Half Barrel)
            location: Current location
            status: Current status (Full or Empty)
            
        Returns:
            Dictionary containing NFT metadata
        """
        metadata = {
            "name": f"Keg #{keg_id}",
            "description": f"A {keg_type} keg currently located at {location}",
            "image": f"https://your-api.com/kegs/{keg_id}/image",
            "attributes": [
                {
                    "trait_type": "Type",
                    "value": keg_type
                },
                {
                    "trait_type": "Location",
                    "value": location
                },
                {
                    "trait_type": "Status",
                    "value": status
                },
                {
                    "trait_type": "Creation Date",
                    "value": datetime.now().isoformat()
                }
            ]
        }
        return metadata

    def mint_nft(self, keg_id, keg_type, location, status):
        """
        Mint an NFT for a keg.
        
        Args:
            keg_id: Unique identifier for the keg
            keg_type: Type of keg
            location: Current location
            status: Current status
            
        Returns:
            Transaction hash of the minting operation
        """
        # Create metadata
        metadata = self.create_keg_metadata(keg_id, keg_type, location, status)
        
        # Upload metadata to IPFS (you would need to implement this)
        metadata_uri = self._upload_to_ipfs(metadata)
        
        # Build transaction
        nonce = self.w3.eth.get_transaction_count(self.account)
        
        transaction = self.contract.functions.mintNFT(
            self.account,
            metadata_uri
        ).build_transaction({
            'chainId': 1,  # Mainnet
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': nonce,
        })
        
        # Sign transaction
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, 
            private_key=self.private_key
        )
        
        # Send transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        return tx_hash.hex()

    def _upload_to_ipfs(self, metadata):
        """
        Upload metadata to IPFS.
        This is a placeholder - you would need to implement actual IPFS upload.
        """
        # TODO: Implement IPFS upload
        return "ipfs://your-metadata-hash"

    def get_nft_owner(self, token_id):
        """
        Get the current owner of an NFT.
        
        Args:
            token_id: The NFT token ID
            
        Returns:
            Address of the current owner
        """
        return self.contract.functions.ownerOf(token_id).call()

    def transfer_nft(self, token_id, to_address):
        """
        Transfer an NFT to another address.
        
        Args:
            token_id: The NFT token ID
            to_address: Address to transfer to
            
        Returns:
            Transaction hash of the transfer
        """
        nonce = self.w3.eth.get_transaction_count(self.account)
        
        transaction = self.contract.functions.transferFrom(
            self.account,
            to_address,
            token_id
        ).build_transaction({
            'chainId': 1,
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': nonce,
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction,
            private_key=self.private_key
        )
        
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return tx_hash.hex() 