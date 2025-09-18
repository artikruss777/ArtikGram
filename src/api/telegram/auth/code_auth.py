class CodeAuth:
    def __init__(self, client):
        self.client = client
    
    def send_code(self, code):
        query = {
            "@type": "checkAuthenticationCode",
            "code": code
        }
        
        self.client._send(query)
        return True