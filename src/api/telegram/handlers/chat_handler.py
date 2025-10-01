import time

class ChatHandler:
    def __init__(self, client):
        self.client = client
        self.chats = []
        self.on_chats_loaded = None
        self.chat_list_loaded = False
        self.pending_chat_requests = set()
        self.last_chat_load_time = 0
    
    def handle_update(self, update):
        update_type = update.get('@type')
        
        if update_type == 'updateAuthorizationState':
            auth_state = update.get('authorization_state', {})
            if auth_state.get('@type') == 'authorizationStateReady':
                time.sleep(2)
                self.load_chats()
            return True
        
        elif update_type == 'updateChatLastMessage':
            self._handle_chat_update(update)
            return True
        
        elif update_type == 'updateNewChat':
            self._handle_new_chat(update)
            return True
        
        elif update_type == 'chats':
            self.process_chats_response(update)
            return True
        
        elif update_type == 'chat':
            self._handle_chat_info(update)
            return True
        
        return False
    
    def load_chats(self):
        current_time = time.time()
        if current_time - self.last_chat_load_time < 5:
            return
        
        self.last_chat_load_time = current_time
        print("Loading chats...")
        
        query = {
            "@type": "getChats",
            "chat_list": {"@type": "chatListMain"},
            "limit": 100,
            "offset_order": "9223372036854775807",
            "offset_chat_id": 0
        }
        self.client._send(query)
    
    def process_chats_response(self, response):
        if response.get('@type') == 'chats':
            chat_ids = response.get('chat_ids', [])
            total_count = response.get('total_count', 0)
            
            print(f"Received {len(chat_ids)} chat IDs, total: {total_count}")
            
            if chat_ids:
                self._load_chat_details(chat_ids)
            else:
                print("No chats found")
    
    def _load_chat_details(self, chat_ids):
        self.chats = []
        self.pending_chat_requests = set(chat_ids)
        
        for i, chat_id in enumerate(chat_ids):
            if i > 0:
                time.sleep(0.1) 
            
            query = {
                "@type": "getChat",
                "chat_id": chat_id
            }
            self.client._send(query)
    
    def _handle_chat_info(self, chat_data):
        chat_id = chat_data.get('id')
        
        if chat_id in self.pending_chat_requests:
            self.pending_chat_requests.remove(chat_id)
            
            self.chats.append(chat_data)
            
            print(f"Loaded chat: {chat_data.get('title', 'Unknown')} (ID: {chat_id})")
            
            if not self.pending_chat_requests and self.on_chats_loaded:
                self.on_chats_loaded(self.chats)
    
    def _handle_chat_update(self, update):
        chat_id = update.get('chat_id')
        last_message = update.get('last_message', {})
        
        for chat in self.chats:
            if chat['id'] == chat_id:
                chat['last_message'] = last_message
                break
    
    def _handle_new_chat(self, update):
        chat = update.get('chat', {})
        if chat:
            self.chats.append(chat)
            if self.on_chats_loaded:
                self.on_chats_loaded(self.chats)
    
    def add_chat(self, chat):
        self.chats.append(chat)
        if self.on_chats_loaded:
            self.on_chats_loaded(self.chats) 