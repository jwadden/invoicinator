from datetime import date, datetime
import dateutil.parser
from isoweek import Week

import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty


import settings

from functions import get_hours

class InvoicinatorApp(App):
    def build(self):
        include_date = dateutil.parser.parse('2015-06-24')

        week = Week.withdate(include_date)
        start_date = week.monday()
        end_date = (week + 1).monday()

        filename = 'invoice-%s.pdf' % week.sunday()
            
        hours_dict = get_hours(start_date, end_date)
        
        #print(hours_dict)
        
        hours_input = Invoicinator(hours_dict=hours_dict)
        hours_input.update_hours_display()
        
        return hours_input

class HoursEntry(BoxLayout):
    case_name_display = StringProperty()
    num_hours_display = StringProperty()

class Invoicinator(Widget):
    def __init__(self, hours_dict={}, *args, **kwargs):
        self.hours_dict = hours_dict
        
        super(Invoicinator, self).__init__(*args, **kwargs)
    
    def update_hours_display(self):
        print(self.hours_dict)
        for name, num_hours in self.hours_dict.items():
            new_hours = HoursEntry(
                case_name_display=name,
                num_hours_display=str(num_hours)
            )
            
            self.hours_display.add_widget(new_hours)
            
            
            
        

if __name__ == '__main__':
    InvoicinatorApp().run()
