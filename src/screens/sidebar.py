from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.animation import Animation

class Sidebar(BoxLayout):
    main_app = ObjectProperty(None)
    is_open = False
    
    def toggle_menu(self):
        if self.is_open:
            self.close_menu()
        else:
            self.open_menu()
    
    def open_menu(self):
        anim = Animation(width=250, duration=0.2)
        anim.start(self)
        self.is_open = True
    
    def close_menu(self):
        anim = Animation(width=0, duration=0.2)
        anim.start(self)
        self.is_open = False
    
    def on_menu_item_click(self, item):
        print(f"Menu item clicked: {item}")
        self.close_menu()
    
    def on_logout_click(self):
        if self.main_app:
            self.main_app.logout()
        self.close_menu()
    
    def on_settings_click(self):
        print("Settings clicked")
        self.close_menu()