from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class HomeScreen(Screen):    
    sidebar = ObjectProperty(None)
    
    def on_enter(self):
        if self.sidebar:
            self.sidebar.close_menu()

class ChatItem():
    def __init__(self):
        pass