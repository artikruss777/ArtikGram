import re

class PhoneAuth:
    def __init__(self, client):
        self.client = client
        self.phone_number = None
    
    def set_phone_number(self, country_code, phone_number):
        country_digits = re.sub(r'[^\d]', '', country_code)
        phone_digits = re.sub(r'[^\d]', '', phone_number)
        
        if not country_digits or not phone_digits:
            raise ValueError("Invalid phone number format")
        
        self.phone_number = f"+{country_digits}{phone_digits}"
        return self.phone_number
    
    def send_phone_number(self):
        if not self.phone_number:
            raise ValueError("Phone number not set")
        
        query = {
            "@type": "setAuthenticationPhoneNumber",
            "phone_number": self.phone_number
        }
        
        self.client._send(query)
        return True