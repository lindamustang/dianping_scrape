import os
from dotenv import load_dotenv
load_dotenv()

SERVICE_ENDPOINT = os.getenv('SERVICE_ENDPOINT')
SERVICE_SECRET = os.getenv('SERVICE_SECRET')
