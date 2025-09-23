from .tdlib import TDJsonClient
from .auth import PhoneAuth, CodeAuth, PasswordAuth
from .handlers import AuthHandler
from ...utils.config_loader import load_config

class TelegramClient:
    def __init__(self, api_id=None, api_hash=None):
        self.td_client = TDJsonClient()
        self.phone_auth = PhoneAuth(self)
        self.code_auth = CodeAuth(self)
        self.password_auth = PasswordAuth(self)
        self.auth_handler = AuthHandler(self)
        self.is_authorized = False
        
        config_api_id, config_api_hash = load_config()
        
        self.api_id = api_id or config_api_id
        self.api_hash = api_hash or config_api_hash
        
        if not self.api_id or not self.api_hash:
            raise ValueError("API ID and API Hash must be provided.")
        
        try:
            self.api_id = int(self.api_id)
        except (ValueError, TypeError):
            raise ValueError("API ID must be an integer")
        
        if not isinstance(self.api_hash, str):
            raise ValueError("API Hash must be a string")
        
        self.auth_handler.on_auth_state_change = self._on_auth_state_change
    
    def initialize(self):
        self._send({
            "@type": "setTdlibParameters", 
            "database_directory": "tdlib_db",
            "use_message_database": True,
            "use_secret_chats": True,
            "api_id": int(self.api_id),
            "api_hash": self.api_hash,
            "system_language_code": "en",
            "device_model": "Desktop",
            "system_version": "Linux",
            "application_version": "1.0",
            "enable_storage_optimizer": True
        })
        
        self._send({"@type": "getAuthorizationState"})
    
    def _send(self, query):
        self.td_client.send(query)
    
    def receive(self, timeout=1.0):
        return self.td_client.receive(timeout)
    
    def process_updates(self, timeout=1.0):
        while True:
            update = self.receive(timeout)
            if not update:
                break
    
    def _on_auth_state_change(self, state_type, auth_state):
        if state_type == 'authorizationStateReady':
            self.is_authorized = True
    
    def close(self):
        if hasattr(self, 'td_client') and self.td_client:
            self.td_client.destroy()
    
    def __enter__(self):
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def _on_auth_state_change(self, state_type, auth_state):
        if state_type == 'authorizationStateReady':
            self.is_authorized = True
            print("User successfully authorized")
        elif state_type == 'authorizationStateClosed':
            self.is_authorized = False
            print("User authorization ended")