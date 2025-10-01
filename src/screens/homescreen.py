from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock

class ChatItem(BoxLayout):
    avatar_text = StringProperty("?")
    chat_title = StringProperty("Unknown Chat")
    last_message = StringProperty("No messages")
    
    def __init__(self, chat_data, **kwargs):
        super().__init__(**kwargs)
        self.update_chat_data(chat_data)
    
    def update_chat_data(self, chat_data):
        title = chat_data.get('title', 'Unknown Chat')
        self.chat_title = title
        self.avatar_text = title[0].upper() if title else "?"
        
        last_message = chat_data.get('last_message', {})
        if last_message:
            content = last_message.get('content', {})
            content_type = content.get('@type', '')
            
            if content_type == 'messageText':
                text_content = content.get('text', {})
                if isinstance(text_content, dict):
                    self.last_message = text_content.get('text', 'Text message')[:50] + "..." if len(text_content.get('text', '')) > 50 else text_content.get('text', 'Text message')
                else:
                    self.last_message = str(text_content)[:50] + "..." if len(str(text_content)) > 50 else str(text_content)
            elif content_type == 'messagePhoto':
                self.last_message = '📷 Photo'
            elif content_type == 'messageVideo':
                self.last_message = '🎥 Video'
            elif content_type == 'messageDocument':
                self.last_message = '📄 Document'
            else:
                self.last_message = 'Message'
        else:
            self.last_message = 'No messages'

class HomeScreen(Screen):
    sidebar = ObjectProperty(None)
    chats_container = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chats_loaded = False
    
    def on_enter(self):
        if self.sidebar:
            self.sidebar.close_menu()
        
        if not self.chats_loaded:
            Clock.schedule_once(self.load_chats, 0.5)
    
    def load_chats(self, dt):
        app = self.get_app()
        if app and hasattr(app, 'telegram_client'):
            if app.telegram_client and app.telegram_client.is_authorized:
                app.telegram_client.load_chats()
    
    def update_chats(self, chats):
        self.chats_loaded = True
        
        if not self.ids:
            Clock.schedule_once(lambda dt: self._update_chats_ui(chats), 0.1)
        else:
            self._update_chats_ui(chats)
    
    def _update_chats_ui(self, chats):
        if not hasattr(self, 'ids') or 'chats_scroll_container' not in self.ids:
            return
        
        container = self.ids.chats_scroll_container
        container.clear_widgets()
        
        if not chats:
            no_chats_label = Label(
                text="No chats yet\nStart a conversation in Telegram!",
                font_size='16sp',
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=100,
                text_size=(300, None),
                halign='center',
                valign='middle'
            )
            container.add_widget(no_chats_label)
            return
        
        for chat in chats:
            chat_item = ChatItem(chat_data=chat)
            container.add_widget(chat_item)
        
        container.add_widget(Widget(size_hint_y=None, height=20))
    
    def get_app(self):
        from kivy.app import App
        return App.get_running_app()