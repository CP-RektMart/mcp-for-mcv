import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MCV_BASE_URL = os.getenv("MCV_BASE_URL", "https://mcv.example.com")
MCV_CLIENT_ID     = os.getenv("MCV_CLIENT_ID", "default-client-id")
MCV_CLIENT_SECRET = os.getenv("MCV_CLIENT_SECRET", "default-client-secret")
MCV_REDIRECT_PATH  = os.getenv("MCV_REDIRECT_PATH", "/callback")