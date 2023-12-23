import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(verbose=True)

LANGUAGE_CODE = "en-US"

BOT_TOKEN = os.environ.get("BOT_TOKEN")
