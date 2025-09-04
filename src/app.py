from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from src.screens.welcome import *

class ArtikGram(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.current = 'welcome'
        return sm