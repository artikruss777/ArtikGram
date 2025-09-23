import json
import os
from pathlib import Path

class SettingsManager:
    def __init__(self):
        self.settings_file = Path('user_settings.json')
        self.settings = self._load_settings()
    
    def _load_settings(self):
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading settings: {e}")
        
        return {
            'is_authorized': False,
            'user_id': None,
            'phone_number': None,
            'auth_state': 'not_authorized'
        }
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def set_authorized(self, user_id=None, phone_number=None):
        self.settings['is_authorized'] = True
        self.settings['auth_state'] = 'authorized'
        if user_id:
            self.settings['user_id'] = user_id
        if phone_number:
            self.settings['phone_number'] = phone_number
        self.save_settings()
    
    def set_unauthorized(self):
        self.settings['is_authorized'] = False
        self.settings['auth_state'] = 'not_authorized'
        self.settings['user_id'] = None
        self.settings['phone_number'] = None
        self.save_settings()
    
    def is_user_authorized(self):
        return self.settings.get('is_authorized', False)
    
    def get_auth_state(self):
        return self.settings.get('auth_state', 'not_authorized')

settings_manager = SettingsManager()