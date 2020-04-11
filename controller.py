from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, BooleanProperty, ReferenceListProperty, ObjectProperty, StringProperty
)

from random import randint
from kivy.uix.button import Button
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
        print(this_drink_num[0])
        this_drink = self.list[this_drink_num[0]]
        print(this_drink.name)
        for item in this_drink.list:
            print(item, this_drink.list[item])
        self.current_item = this_drink_num[0]
        self.update_item()
        #self.label_wid.text = 'My label after button press'
        #self.info = 'New info text'
        
class ControllerApp(App):

    def build(self):
        cont = Controller(info='Hello world')
        cont.read_xml()
        box = BoxLayout(orientation='horizontal', spacing=20, pos=(0,550))
        i = 0;
        callbacks = []
        
        for item in cont.list:
            print("_ _ " + item.name)
            btn = Button(text=item.name, on_press=Command(cont.do_action, i), size_hint=(.1,.1))
            i += 1
            box.add_widget(btn)
        
        cont.add_widget(box)
        return cont


if __name__ == '__main__':
    
    ControllerApp().run()
