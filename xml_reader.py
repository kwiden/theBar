import xml.etree.ElementTree as ET

class Drink:
    
    def __init__(self, name):
        self.name = name
        list = {}
        self.list = list
    
    def add_ingredient(self, name, qty):
        self.list[name] = qty
    
    def toString(self):
        output = "" + self.name + ":\n"
        for ing in self.list:
            output += "[" + ing + " " + self.list[ing] + "oz] "
        return output
            
def read_recipes():
    
    book = []

    tree = ET.parse('data.xml')
    root = tree.getroot()

    for dr in root.findall('drink'):
        name = dr.get('name')
        recipe = Drink(name)
        for ingr in dr.findall('ing'):
            recipe.add_ingredient(ingr.get('name'),ingr.text)
        book.append(recipe)
    
    #for drink in book:
       # print(drink.toString())
    
    return book