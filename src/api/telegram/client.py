from tdlib import TDJsonClient
from ....config import *

class TelegramClient:
    def __init__(self, ):
        self.td_client = TDJsonClient
        self.is_authorized = False
    
    def initialize(self):
        self._send({"@type": "setTdlibParameters", 
                   "database_directory": "tdlib_db",
                   "use_message_database": True,
                   "use_secret_chats": True,
                   "api_id": TG_API_ID,
                   "api_hash": TG_API_HASH,
                   "system_language_code": "en",
                   "device_model": "Desktop",
                   "system_version": "Linux",
                   "application_version": "1.0",
                   "enable_storage_optimizer": True})
    
    def _send(self, query):
        self.td_client.send(query)
    
    def receive(self, timeout=1.0):
        return self.td_client.receive(timeout)
    
    def close(self):
        self.td_client.destroy()
    
    def __enter__(self):
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()