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

    if state_type == 'authorizationStateWaitPassword':
        has_recovery_email = auth_state.get('has_recovery_email', False)
        password_hint = auth_state.get('password_hint', '')
    
    if self.on_auth_state_change:
        self.on_auth_state_change(state_type, auth_state)