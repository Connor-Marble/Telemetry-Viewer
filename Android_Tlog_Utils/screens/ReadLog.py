from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.properties import ObjectProperty

import math


class Reader(Widget):
    log = None
    log_text = ObjectProperty(Label)
    scroll_down = ObjectProperty(Button)
    lines = 25 #TODO get number of lines based on screen height
    scrollpos = 0

    def _init__(self,**kwargs):
        super(Reader,self).__init__(kwargs)
        scroll_down.bind(on_press=scroll)

    def DisplayLog(self):
        log_text = ''
        for i in range(self.lines):
            if i < self.lines:
                log_text += str(self.log[i+self.scrollpos])
                log_text += '\n'

        self.log_text.text = log_text
    
    def scroll(self):
        print(scrollpos)
        scrollpos+=1
        DisplayLog()
