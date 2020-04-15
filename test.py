from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""

<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
""")

# Declare both screens
class MenuScreen(GridLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        box = BoxLayout(orientation='horizontal', spacing=20, pos=(0,550))
        for i in range(0,5):
            btn = Button(text=str(i), size_hint=(.1,.1))
            box.add_widget(btn)
        self.add_widget(box)
        sbtn = Button(text='Goto settings',on_press = self.gotosettings, size_hint=(.1,.1))
        self.add_widget(sbtn)
        #self.name = name
        
    def gotosettings(self,instance):
        chat_app.screen_manager.current = 'Settings'

class SettingsScreen(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sbtn = Button(text='Menu',on_press = self.gotomenu, size_hint=(.1,.1))
        self.add_widget(sbtn)
        
    def gotomenu(self,instance):
        chat_app.screen_manager.current = 'Menu'

class TestApp(App):
    def build(self):

        # We are going to use screen manager, so we can add multiple screens
        # and switch between them
        self.screen_manager = ScreenManager()

        # Initial, connection screen (we use passed in name to activate screen)
        # First create a page, then a new screen, add page to screen and screen to screen manager
        self.connect_page = MenuScreen()
        screen = Screen(name='Menu')
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        # Info page
        self.info_page = SettingsScreen()
        screen = Screen(name='Settings')
        screen.add_widget(self.info_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

if __name__ == '__main__':
    chat_app = TestApp()
    chat_app.run()