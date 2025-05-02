# Keg Tracker

A Flask-based web application for tracking keg inventory with blockchain integration. This application provides a simple and efficient way to manage your keg inventory, including tracking keg types, locations, and status, with the added capability of creating NFTs for each keg on the Ethereum blockchain.

## Features

- Add new kegs with type (Sixtel or Half Barrel), location, and status (Full or Empty)
- View all kegs in a clean, tabular format
- Update keg locations and status
- Delete kegs from inventory
- Create NFTs for kegs on the Ethereum blockchain
- Track NFT ownership and transactions
- Simple and intuitive web interface
- SQLite database backend for reliable data storage

## Prerequisites

- Python 3.x
- pip (Python package installer)
- Ethereum wallet with ETH for gas fees
- Infura account and API key

## Installation

1. Clone or download this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up blockchain configuration:
   - Create a `.env` file based on `.env.example`
   - Add your Infura API key
   - Add your Ethereum wallet address and private key
   - Deploy the smart contract and add the contract address

## Blockchain Setup

1. Create an Infura account at https://infura.io/
2. Create a new project and get your API key
3. Deploy the smart contract (`KegNFT.sol`):
   - Compile the contract using a Solidity compiler
   - Deploy to Ethereum mainnet (or testnet for development)
   - Save the deployed contract address
4. Update your `.env` file with:
   ```
   INFURA_URL=https://mainnet.infura.io/v3/YOUR-PROJECT-ID
   CONTRACT_ADDRESS=0x...  # Your deployed contract address
   WALLET_ADDRESS=0x...   # Your Ethereum wallet address
   PRIVATE_KEY=your-private-key
   ```

## Usage

1. Start the application:
   ```bash
   python keg_tracker_v1.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. Use the web interface to:
   - Add new kegs using the form at the top
   - Create NFTs for kegs (requires ETH for gas fees)
   - View all existing kegs in the table
   - Update keg locations and status
   - Delete kegs as needed
   - View NFT transaction hashes on Etherscan

## Database Structure

The application uses a SQLite database with the following table structure:

```sql
CREATE TABLE kegs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keg_type TEXT NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL,
    nft_token_id TEXT
)
```

- `id`: Auto-incrementing primary key
- `keg_type`: Type of keg (Sixtel or Half Barrel)
- `location`: Current location of the keg
- `status`: Current status (Full or Empty)
- `nft_token_id`: Transaction hash of the NFT (if created)

## Smart Contract

The application uses a custom ERC721 smart contract (`KegNFT.sol`) for NFT functionality:
- Implements the standard ERC721 interface
- Allows minting of new NFTs
- Tracks ownership and transfers
- Uses IPFS for metadata storage

## Dependencies

- Flask==3.0.2
- Werkzeug==3.0.1
- web3==6.15.1
- python-dotenv==1.0.1
- Pillow==10.2.0
- requests==2.31.0

## Development

The application is built using:
- Flask for the web framework
- SQLite for the database
- HTML/CSS for the frontend
- Jinja2 for templating
- Web3.py for blockchain interaction
- OpenZeppelin contracts for NFT standard

## Security Notes

- Never commit your `.env` file or private keys to version control
- Use environment variables for sensitive information
- Consider using a testnet for development
- Keep your private keys secure

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is open source and available under the MIT License.

## Support

For support, please open an issue in the GitHub repository. 