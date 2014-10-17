from kivy.uix.widget import Widget
from kivy.properties import Property
import math

class Reader(Widget):
    log = None
    log_text = Property('<Log_Text>')
    lines = 25 #TODO get number of lines based on screen height
    scroll = 0

    def _init__(self,**kwargs):
        super(Reader,self).__init__(kwargs)

    def DisplayLog(self):
        log_text = ''
        for i in range(self.lines):
            if i < self.lines:
                log_text += str(self.log[i+scroll])
                log_text += '\n'

        self.log_text.text = log_text

    
