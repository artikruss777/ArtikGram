from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import json

class ChatItem(BoxLayout):
    title = StringProperty('')
    preview = StringProperty('')
    
    def __init__(self, chat_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 80
        self.padding = [10, 5]
        self.spacing = 10
        
        self.chat_data = chat_data
        self.title = chat_data.get('title', 'Unknown Chat')
        
        
        last_message = chat_data.get('last_message', {})
        if last_message:
            content = last_message.get('content', {})
            if content.get('@type') == 'messageText':
                self.preview = content.get('text', {}).get('text', '')[:30] + '...'
            else:
                self.preview = '[Media]'
        else:
            self.preview = 'No messages'

class HomeScreen(Screen):
    chats = ListProperty([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chat_loader_event = None
    
    def on_enter(self):
        print("HomeScreen entered, loading chats...")
        self.load_chats()
        
        self.chat_loader_event = Clock.schedule_interval(lambda dt: self.load_chats(), 3.0)
    
    def on_leave(self):
        if self.chat_loader_event:
            self.chat_loader_event.cancel()
    
    def load_chats(self):
        try:
            from kivy.app import App
            app = App.get_running_app()
            
            if not app or not app.telegram_client:
                print("No telegram client available")
                return
            
            print("Requesting chats...")
            
            query = {
                "@type": "getChats",
                "chat_list": {"@type": "chatListMain"},
                "limit": 20
            }
            
            app.telegram_client._send(query)
            
        except Exception as e:
            print(f"Error loading chats: {e}")
    
    def update_chat_list(self, chat_ids):
        if not chat_ids:
            print("No chat IDs received")
            return
        
        print(f"Received chat IDs: {chat_ids}")
        
        
        for chat_id in chat_ids:
            query = {
                "@type": "getChat",
                "chat_id": chat_id
            }
            
            from kivy.app import App
            app = App.get_running_app()
            if app and app.telegram_client:
                app.telegram_client._send(query)
    
    def add_chat(self, chat_data):
        if not chat_data:
            return
        
        chat_id = chat_data.get('id')
        
        
        existing_ids = [chat.get('id') for chat in self.chats]
        if chat_id not in existing_ids:
            self.chats.append(chat_data)
            print(f"Added chat: {chat_data.get('title')}")
            self.update_chat_display()
    
    def update_chat_display(self):
        if not hasattr(self, 'ids') or 'chat_list_layout' not in self.ids:
            print("No chat_list_layout found")
            return
        
        chat_layout = self.ids.chat_list_layout
        chat_layout.clear_widgets()
        
        print(f"Updating display with {len(self.chats)} chats")
        
        if not self.chats:
            
            no_chats = Label(
                text='No chats found\nStart a conversation!',
                size_hint_y=None,
                height=100,
                color=(0, 0, 0, 1),  
                font_size='16sp'
            )
            chat_layout.add_widget(no_chats)
        else:
            
            for chat in self.chats:
                chat_item = ChatItem(chat_data=chat)
                chat_layout.add_widget(chat_item)
    
    def handle_update(self, update):
        update_type = update.get('@type')
        print(f"Received update: {update_type}")
        
        if update_type == 'chats':
            chat_ids = update.get('chat_ids', [])
            self.update_chat_list(chat_ids)
        
        elif update_type == 'chat':
            self.add_chat(update)
        
        elif update_type == 'updateNewChat':
            self.add_chat(update.get('chat', {}))
    
    def logout(self):
        from kivy.app import App
        app = App.get_running_app()
        if app:
            app.logout()
