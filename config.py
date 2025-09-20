import dotenv
import os

dotenv.load_dotenv()

TELEGRAM_API_ID = int(os.getenv("TG_API_ID"))
TELEGRAM_API_HASH = str(os.getenv("TG_API_HASH"))
# TDJSON_PATH = "Your path"

print(TELEGRAM_API_ID, TELEGRAM_API_HASH)