class AuthHandler:
    def __init__(self, client):
        self.client = client
        self.on_auth_state_change = None
    
    def handle_update(self, update):
        if update.get('@type') == 'updateAuthorizationState':
            auth_state = update.get('authorization_state', {})
            self._handle_auth_state(auth_state)
            return True
        return False
    
    def _handle_auth_state(self, auth_state):
        state_type = auth_state.get('@type')
        
        if self.on_auth_state_change:
            self.on_auth_state_change(state_type, auth_state)