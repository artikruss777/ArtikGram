from src.app import ArtikGram
from src.api.telegram.client import *
from src.api.telegram.tdlib import *
from config import *

if __name__ == '__main__':
    artikgram_client = TelegramClient(api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)
    artikgram_client.initialize()
    ArtikGram().run()