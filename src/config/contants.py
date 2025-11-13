import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

APP_NAME = os.getenv("APP_NAME", "mcv-mcp-server")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))
TRANSPORT = os.getenv("TRANSPORT", "http")

MCV_CLIENT_ID     = os.getenv("MCV_CLIENT_ID", "default-client-id")
MCV_CLIENT_SECRET = os.getenv("MCV_CLIENT_SECRET", "default-client-secret")
MCV_REDIRECT_PATH  = os.getenv("MCV_REDIRECT_PATH", "/callback")