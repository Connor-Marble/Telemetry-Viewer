from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, ObjectProperty, Property
from kivy.uix.filechooser import FileChooserListView

import mav_parse as mp
import TelemetryGraph as tg

class ScreenManager(FloatLayout):
    log = None
    def __init__(self,**kwargs):
        super(ScreenManager,self).__init__(**kwargs)
        
        self.startmenu = StartMenu()
        self.startmenu.filebtn.bind(on_press=self.selectfile)
        self.add_widget(self.startmenu)
        
        self.filemenu = FileChooserListView()
        self.filemenu.bind(on_submit=self.openfile)

    def selectfile(obj,value):
        obj.clear_widgets()
        obj.add_widget(obj.filemenu)

    def openfile(obj,value,selected,event):
        obj.log = mp.TelemetryLog(selected[0]).ParsePackets()
        mode_menu = ModeMenu()
       

        mode_menu.readbtn.bind(on_press=obj.readlog)
        mode_menu.graphbtn.bind(on_press=obj.graphlog)

        obj.clear_widgets()
        obj.add_widget(mode_menu)

    def readlog(obj,value):
        rl = ReadLog()
        rl.log = obj.log
        rl.DisplayLog()
        obj.clear_widgets()
        obj.add_widget(rl)

    def graphlog(obj,value):
        graph = tg.TelemetryGraphScreen(obj,obj.log)

class StartMenu(Widget):
    filebtn = ObjectProperty(Button)

class ModeMenu(Widget):
    readbtn = ObjectProperty(Button)
    graphbtn = ObjectProperty(Button)
    log = None

class ReadLog(Widget):
    log = None
    log_text = Property('<Log_Text>')
    packetlimit = 150
    def DisplayLog(self):
        log_text = ''
        for i in range(len(self.log)):
            if i < self.packetlimit:
                log_text += str(self.log[i])
                log_text += '\n'

            if i >=  self.packetlimit:
                log_text += "\n \n \n  ... Output truncated to " + str(self.packetlimit) + " packets"
                break
        self.log_text.text = log_text

class LogViewApp(App):
    def build(self):
        return ScreenManager()
    

if __name__ == '__main__':
    LogViewApp().run()
