import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
API_ID = str(os.getenv("API_ID"))
API_HASH = str(os.getenv("API_HASH"))