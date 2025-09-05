from kivy.uix.screenmanager import Screen
import re

class LoginScreen1(Screen):
    
    def update_continue_button(self):
        country_code = self.ids.country_code_input.text
        phone_number = self.ids.phone_input.text
        
        country_digits = re.sub(r'[^\d]', '', country_code)
        phone_digits = re.sub(r'[^\d]', '', phone_number)
        
        has_valid_country = country_code.startswith('+') and len(country_digits) > 0
        has_valid_phone = len(phone_digits) >= 5
        
        self.ids.continue_button.disabled = not (has_valid_country and has_valid_phone)