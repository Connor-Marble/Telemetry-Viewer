from kivy.app import App

from kivy.base import EventLoop

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock

import mav_parse as mp
from functools import partial
from widgets.screens import Reader, TelemetryGraphScreen, StartMenu, ModeMenu

class ScreenManager(FloatLayout):
    log = None
    def __init__(self,**kwargs):
        super(ScreenManager,self).__init__(**kwargs)

        EventLoop.window.bind(on_keyboard=self.goback)
        
        self.startmenu = StartMenu()
        self.startmenu.filebtn.bind(on_press=self.selectfile)
        self.add_widget(self.startmenu)
        
        self.filemenu = FileChooserListView()
        self.filemenu.bind(on_submit=self.openfile)

    def selectfile(obj,value):
        #wait for old input to clear
        Clock.schedule_once(partial(obj.switchscreen,obj.filemenu),0.15)

    def openfile(obj,value,selected,event):
        obj.log = mp.TelemetryLog(selected[0]).ParsePackets()
        mode_menu = ModeMenu()
       

        mode_menu.readbtn.bind(on_press=obj.readlog)
        mode_menu.graphbtn.bind(on_press=obj.graphlog)

        obj.switchscreen(mode_menu)

    def readlog(obj,value):
        rl = Reader(obj.log)
        obj.switchscreen(rl)
        
    def graphlog(obj,value):
        graph = TelemetryGraphScreen(obj,obj.log)
        obj.switchscreen(graph)
        
    def switchscreen(self, widget, *args):
        self.clear_widgets()
        self.add_widget(widget)
    
    def goback(self, window, key, *args):
        if key==27:
            self.switchscreen(self.startmenu)
            return True

class LogViewApp(App):
    def build(self):
        return ScreenManager()
    

if __name__ == '__main__':
    LogViewApp().run()
