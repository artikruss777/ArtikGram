from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty, BooleanProperty
import re
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from src.screens.welcome import WelcomeScreen
from src.screens.login1 import LoginScreen1
from src.screens.login2 import LoginScreen2
from src.screens.login3 import LoginScreen3

class ArtikGram(App):
    telegram_client = None
    current_phone_number = ""
    
    def build(self):
        Builder.load_file('src/kv/my.kv')
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginScreen1(name='login1'))
        sm.add_widget(LoginScreen2(name='login2'))
        sm.add_widget(LoginScreen3(name='login3'))
        sm.current = 'welcome'
        
        Clock.schedule_once(self.initialize_telegram_client, 1.0)
        
        return sm
    
    def initialize_telegram_client(self, dt):
        try:
            from src.api.telegram.client import TelegramClient
            self.telegram_client = TelegramClient()
            self.telegram_client.initialize()
            
            Clock.schedule_interval(self.process_telegram_updates, 0.1)
            
        except Exception as e:
            error_msg = f"Failed to initialize Telegram client: {e}"
            print("Error", error_msg)

    
    def process_telegram_updates(self, dt):
        if self.telegram_client:
            try:
                update = self.telegram_client.receive(0)
                if update and update.get('@type') == 'updateAuthorizationState':
                    auth_state = update.get('authorization_state', {})
                    self.handle_auth_state(auth_state)
            except Exception as e:
                print(f"Error processing Telegram updates: {e}")
    
    def handle_auth_state(self, auth_state):
        state_type = auth_state.get('@type')
        
        if state_type == 'authorizationStateWaitCode':
            code_info = auth_state.get('code_info', {})
            code_type = code_info.get('type', {}).get('@type', '')
            
            if code_type == 'authenticationCodeTypeSms':
                print("SMS code sent to your phone")
            elif code_type == 'authenticationCodeTypeTelegramMessage':
                print("Code sent via Telegram message")
            
            self.root.current = 'login2'
            
        elif state_type == 'authorizationStateReady':
            print("Authorization completed!")
            
        elif state_type == 'authorizationStateWaitPassword':
            print("2FA password required")
            password_hint = auth_state.get('password_hint', '')
            print(f"Password hint: {password_hint}")
            
            if self.root and hasattr(self.root, 'get_screen'):
                try:
                    screen = self.root.get_screen('login3')
                    if screen and hasattr(screen, 'set_password_hint'):
                        screen.set_password_hint(password_hint)
                except:
                    pass
            
            self.root.current = 'login3'
        
        elif state_type == 'authorizationStateWaitPhoneNumber':
            self.root.current = 'login1'
        
        elif state_type == 'authorizationStateWaitRegistration':
            print("Account registration required")
        
        elif state_type == 'authorizationStateWaitTdlibParameters':
            print("Waiting for TDLib parameters")
        
        elif state_type == 'authorizationStateClosing':
            print("Authorization is closing")
        
        elif state_type == 'authorizationStateClosed':
            print("Authorization closed")
    
    def format_country_code(self, text_input):
        text = text_input.text
        if not text.startswith('+'):
            text = '+' + text.replace('+', '')
        
        cleaned = re.sub(r'[^\d+]', '', text)
        
        if cleaned.startswith('++'):
            cleaned = '+' + cleaned[2:]
        
        if text_input.text != cleaned:
            text_input.text = cleaned
        
        self.update_phone_format()
    
    def format_phone_number(self, text_input):
        text = text_input.text
        cleaned = re.sub(r'[^\d]', '', text)
        
        if len(cleaned) > 15:
            cleaned = cleaned[:15]
        
        if text_input.text != cleaned:
            text_input.text = cleaned
        
        self.update_phone_format()
    
    def update_phone_format(self):
        if not self.root:
            return
        
        try:
            screen = self.root.get_screen('login1')
            if not screen:
                return
                
            country_code = screen.ids.country_code_input.text
            phone_text = screen.ids.phone_input.text
            
            country_digits = re.sub(r'[^\d]', '', country_code)
            phone_digits = re.sub(r'[^\d]', '', phone_text)
            
            if phone_digits:
                formatted_phone = self.format_for_display(phone_digits)
                screen.ids.formatted_phone_label.text = f"{country_code} {formatted_phone}"
            else:
                screen.ids.formatted_phone_label.text = country_code
            
            has_valid_country = country_code.startswith('+') and len(country_digits) > 0
            has_valid_phone = len(phone_digits) >= 5  
            
            screen.ids.continue_button.disabled = not (has_valid_country and has_valid_phone)
            
        except Exception as e:
            print(f"Error in update_phone_format: {e}")
    
    def format_for_display(self, digits):
        if not digits:
            return ""
        if len(digits) <= 3:
            return digits
        elif len(digits) <= 6:
            return f"{digits[:3]} {digits[3:]}"
        elif len(digits) <= 8:
            return f"{digits[:3]} {digits[3:6]} {digits[6:]}"
        else:
            return f"{digits[:3]} {digits[3:6]} {digits[6:8]} {digits[8:]}"
    
    def process_password(self, password):
        try:
            if not self.telegram_client:
                print("Error", "Telegram client not initialized.")
                return
            
            self.telegram_client.password_auth.send_password(password)
            
        except Exception as e:
            error_msg = f"Error processing password: {e}"
            print("Error", error_msg)
    
    def process_phone_number(self, country_code, phone_number):
        try:
            if not self.telegram_client:
                print("Error", "Telegram client not initialized.")
                return
            
            full_phone = self.telegram_client.phone_auth.set_phone_number(
                country_code, phone_number
            )
            self.current_phone_number = full_phone
            
            self.telegram_client.phone_auth.send_phone_number()
            
        except Exception as e:
            error_msg = f"Error processing phone number: {e}"
            print("Error", error_msg)
    
    def process_verification_code(self, code):
        try:
            if not self.telegram_client:
                print("Error", "Telegram client not initialized.")
                return
            
            self.telegram_client.code_auth.send_code(code)
            
        except Exception as e:
            error_msg = f"Error processing verification code: {e}"
            print("Error", error_msg)
    
    def resend_code(self):
        try:
            if not self.telegram_client:
                print("Error", "Telegram client not initialized.")
                return
            
            query = {"@type": "resendAuthenticationCode"}
            self.telegram_client._send(query)
            print("Code resent successfully")
            
        except Exception as e:
            error_msg = f"Error resending code: {e}"
            print("Error", error_msg)
    
    def on_stop(self):
        if self.telegram_client:
            self.telegram_client.close()