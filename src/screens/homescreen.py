from kivy.uix.screenmanager import Screen

class HomeScreen(Screen):
    pass

class ChatItem():
    def __init__(self, name=None):
        self.name = name