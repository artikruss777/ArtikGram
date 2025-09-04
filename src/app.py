from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from src.screens.welcome import *
from src.screens.login1 import LoginScreen1

from kivy.lang import Builder


class ArtikGram(App):
    def build(self):

        Builder.load_file('src/kv/my.kv')
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginScreen1(name='login1'))
        sm.current = 'welcome'
        return sm