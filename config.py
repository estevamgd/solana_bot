from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Access the API key
BOT_TOKEN = os.getenv("TELEGRAM_API_KEY")
DB_FILE = "wallets.db"
RPC_URL = "https://api.mainnet-beta.solana.com"
