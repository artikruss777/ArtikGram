from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from src.screens.welcome import *
from src.screens.login1 import LoginScreen1
from kivy.properties import StringProperty, BooleanProperty
import re
from kivy.clock import Clock

from kivy.lang import Builder


class ArtikGram(App):
    def build(self):

        Builder.load_file('src/kv/my.kv')
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginScreen1(name='login1'))
        sm.current = 'welcome'
        return sm
    def on_start(self):
        self.update_phone_format()
    
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
        cursor_pos = text_input.cursor_index()
        
        digits = re.sub(r'\D', '', text)
        if len(digits) > 15:
            digits = digits[:15]
        
        formatted = ''
        for i, digit in enumerate(digits):
            if i == 3:
                formatted += ' '
            if i == 6:
                formatted += ' '
            if i == 8:
                formatted += ' '
            formatted += digit
        
        if text_input.text != formatted:
            text_input.text = formatted
            new_cursor_pos = min(cursor_pos + formatted.count(' ') - text.count(' '), len(formatted))
            text_input.cursor = (new_cursor_pos, 0)
        
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
            phone_digits = re.sub(r'\D', '', phone_text)
            
            formatted_phone = f"{country_code} {self.format_for_display(phone_digits)}"
            screen.ids.formatted_phone_label.text = formatted_phone
            
            country_digits = re.sub(r'\D', '', country_code)
            has_country_code = len(country_digits) > 0
            has_phone_number = len(phone_digits) >= 5
            
            screen.ids.continue_button.disabled = not (has_country_code and has_phone_number)
            
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
            return f"{digits[:3]} {digits[3:6]} {digits[6:8]} {digits[8:10]}"
    
    def process_phone_number(self, country_code, phone_number):
        country_digits = re.sub(r'\D', '', country_code)
        phone_digits = re.sub(r'\D', '', phone_number)
        if country_digits and phone_digits:
            full_phone = f"+{country_digits}{phone_digits}"
            print(f"Full phone number for TDLib: {full_phone}")