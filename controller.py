from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import (
    NumericProperty, BooleanProperty, ReferenceListProperty, ObjectProperty, StringProperty
)

from random import randint
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
import xml_reader as xml

class Command:
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def __call__(self, idk):
        return self.callback(self.args)
        
        
class Controller(FloatLayout):
    label_wid = ObjectProperty()
    info = StringProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.read_xml()
        box = BoxLayout(orientation='horizontal', spacing=20, pos=(0,550))
        i = 0;
        callbacks = []
        
        for item in self.list:
            btn = Button(text=item.name, on_press=Command(self.do_action, i), size_hint=(.1,.1))
            i += 1
            box.add_widget(btn)
        
        self.add_widget(box)
    
        
    def update_item(self):
        this_drink = self.list[self.current_item]
        self.label_wid.text = this_drink.name
        i = 0;
        for item in this_drink.list:
            print(item, this_drink.list[item])
        
        #print(self.list[self.current_item].list.keys()[0])
        #self.slider_id.value = self.list[self.current_item].list[0]
    def read_xml(self):
        self.list = xml.read_recipes()
        self.current_item = 0
        self.label_wid.text = self.list[self.current_item].name
        self.list_len = len(self.list)
        print(self.list_len)
        self.current_item = 0;
        self.update_item()
    
    def prev_item(self):
        if(self.current_item > 0):
            self.current_item -= 1
        else:
            self.current_item = self.list_len - 1
        self.update_item()

    def next_item(self):
        if(self.current_item < (self.list_len - 1)):
            self.current_item += 1
        else:
            self.current_item = 0
        self.update_item()

        
    def do_action(self, this_drink_num):
        this_drink = self.list[this_drink_num[0]]
        self.current_item = this_drink_num[0]
        self.update_item()
        bar_app.screen_manager.current = this_drink.name
        
        #self.label_wid.text = 'My label after button press'
        #self.info = 'New info text'
        
class Drink_Page(FloatLayout):
    
    def __init__(self, name, ingr_list, **kwargs):
        super().__init__(**kwargs)
        
        la = Label(text=name)
        
        box = BoxLayout(orientation='vertical', spacing=20)
        box.add_widget(la)
        
        for item in ingr_list:
            print(item, ingr_list[item])
            lab = Label(text=str(item))
            box.add_widget(lab)
            #btn = Button(text=item.name, on_press=Command(cont.do_action, i), size_hint=(.1,.1))
            #i += 1
            #box.add_widget(btn)

        sbtn = Button(text='Back to Main',on_press = self.go_to_main, size_hint=(.1,.1))
        self.add_widget(box)
        self.add_widget(sbtn)
        
    def go_to_main(self,instance):
        bar_app.screen_manager.current = 'Main'
        
class ControllerApp(App):

    def build(self):
        # We are going to use screen manager, so we can add multiple screens
        # and switch between them
        self.screen_manager = ScreenManager()

        # Initial, Main screen (we use passed in name to activate screen)
        # First create a page, then a new screen, add page to screen and screen to screen manager
        self.main_menu = Controller()
        screen = Screen(name='Main')
        screen.add_widget(self.main_menu)
        self.screen_manager.add_widget(screen)
        
        # Drink pages
        for drink in self.main_menu.list:
            self.drinks = Drink_Page(drink.name,drink.list)
            screen = Screen(name=drink.name)
            screen.add_widget(self.drinks)
            self.screen_manager.add_widget(screen)

        
        
        #screen = Screen(name='Settings')
        #screen.add_widget(self.info_page)
        #self.screen_manager.add_widget(screen)

        return self.screen_manager
        


if __name__ == '__main__':
    bar_app = ControllerApp()
    bar_app.run()
