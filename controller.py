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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
import xml_reader as xml

def getColor(i):
    colors = [[1,0,0,1],[1,.6,0,1],[1,1,0,1],[0,1,0,1],[0,0,1,1],[1,0,1,1]]
    return colors[i%6]
    

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
        box = layout = GridLayout(cols=3)
        i = 0;
        
        for item in self.list:
            btn = Button(text=item.name, on_press=Command(self.do_action, i),background_normal = '', background_color = getColor(i))
            i += 1
            box.add_widget(btn)
        
        self.add_widget(box)

    def read_xml(self):
        self.list = xml.read_recipes()
        self.current_item = 0
        self.list_len = len(self.list)
        print(self.list_len)
        self.current_item = 0;
        
    def do_action(self, this_drink_num):
        this_drink = self.list[this_drink_num[0]]
        self.current_item = this_drink_num[0]
        bar_app.screen_manager.current = this_drink.name
        
        #self.label_wid.text = 'My label after button press'
        #self.info = 'New info text'
        
class Drink_Page(FloatLayout):
    
    def __init__(self, name, ingr_list, **kwargs):
        super().__init__(**kwargs)
        
        self.labels = []
        self.ingredients = ingr_list
        self.name = name
        
        la = Label(text=name,font_size = '48sp')
        
        box = BoxLayout(orientation='vertical')
        box.add_widget(la)
        i = 0;
        
        for item in ingr_list:
            this_row = BoxLayout(orientation='horizontal', padding = [1,1,1,1])
            print(item, ingr_list[item])
            lab = Label(text=str(item),font_size = '24sp')
            qty = Label(text=ingr_list[item],font_size = '24sp')
            self.labels.append(qty)
            plus = Button(text='+',font_size = '24sp',on_press=Command(self.plus, i))
            minus = Button(text='-',font_size = '24sp',on_press=Command(self.minus, i))
            this_row.add_widget(lab)
            this_row.add_widget(qty)
            this_row.add_widget(plus)
            this_row.add_widget(minus)
            #btn = Button(text=item.name, on_press=Command(cont.do_action, i), size_hint=(.1,.1))
            #i += 1
            box.add_widget(this_row)
            i+=1

        sbtn = Button(text='Back to Main',on_press = self.go_to_main)
        box.add_widget(sbtn)
        self.add_widget(box)
        
        
    def go_to_main(self,instance):
        self.reset_vals()
        bar_app.screen_manager.current = 'Main'
        
    def minus(self, qty):
        self.change_val(qty[0],-1)
        
    def plus(self, qty):
        self.change_val(qty[0], 1)
        
    def change_val(self, this_qty, plus_min):
        print(self.labels[this_qty].text)
        val = float(self.labels[this_qty].text)
        val += .25 * plus_min
        self.labels[this_qty].text = str(val)
        
    def reset_vals(self):
        i = 0
        for item in self.ingredients:
            self.labels[i].text = self.ingredients[item]
            i += 1
        
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
