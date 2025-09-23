from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

class LoginScreen3(Screen):
    password_hint = StringProperty("")
    
    def set_password_hint(self, hint):
        self.password_hint = hint or "No hint provided"
        
    def on_enter(self):

        if self.password_hint and self.password_hint != "No hint provided":
            hint_text = f"Password hint: {self.password_hint}"
        else:
            hint_text = "Enter your 2FA password"
        
        if hasattr(self, 'ids') and 'hint_label' in self.ids:
            self.ids.hint_label.text = hint_text
    
    def on_verify_pressed(self):
        """Обработка нажатия кнопки Verify"""
        password = self.ids.password_input.text.strip()
        
        if not password:
            print("Password cannot be empty")
            return
        from kivy.app import App
        app = App.get_running_app()
        
        if hasattr(app, 'process_password'):
            app.process_password(password)