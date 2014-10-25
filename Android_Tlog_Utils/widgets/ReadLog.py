from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.properties import ObjectProperty

import math


class Reader(Widget):
    log = None
    log_text = ObjectProperty(Label)

    scroll_down = ObjectProperty(Button)
    scroll_up = ObjectProperty(Button)
        
    scrollpos = 0

    def __init__(self,**kwargs):
        super(Reader,self).__init__()
        self.scroll_down.bind(on_press=self.scroll)
        self.scroll_up.bind(on_press=self.scroll)
        self.lines=super(Reader,self).height/7
        #TODO account for multi-line packages
        self.log_text.y = self.scroll_down.height
        
        
        
    def DisplayLog(self):
        log_text = ''
        for i in range(self.lines):
            if i < self.lines:
                log_text += str(self.log[i+self.scrollpos])
                log_text += '\n'

        self.log_text.text = log_text
        
    
    def scroll(instance, value):
        buttonText = value.text

        instance.scrollpos += 1 if buttonText == 'V' else -1
        
        instance.DisplayLog()
