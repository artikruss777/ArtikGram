class PasswordAuth:
    def __init__(self, client):
        self.client = client
    
    def send_password(self, password):
        query = {
            "@type": "checkAuthenticationPassword",
            "password": password
        }
        
        self.client._send(query)
        return True