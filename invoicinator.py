import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class InvoicinatorApp(App):

    def build(self):
        return HoursInput()
        
class HoursInput(Widget):
    pass

if __name__ == '__main__':
    InvoicinatorApp().run()
