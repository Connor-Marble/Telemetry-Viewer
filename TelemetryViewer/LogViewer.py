from kivy.app import App

from kivy.base import EventLoop

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.label import Label

import mav_parse as mp
from functools import partial
from widgets.screens import Reader, TelemetryGraphScreen,\
    StartMenu, ModeMenu, ExportMenu


class ScreenManager(FloatLayout):
    log = None
    logpath = ''
    
    def __init__(self, **kwargs):
        super(ScreenManager, self).__init__(**kwargs)

        EventLoop.window.bind(on_keyboard=self.goback)
        
        self.startmenu = StartMenu()
        self.startmenu.filebtn.bind(on_press=self.selectfile)
        self.add_widget(self.startmenu)
        
        self.filemenu = FileChooserListView()
        self.filemenu.bind(on_submit=self.openfile)
        
        self.mode_menu = None
        
    def selectfile(obj, value):
        # wait for old input to clear
        Clock.schedule_once(partial(obj.switchscreen, obj.filemenu), 0.15)

    def openfile(obj, value, selected, event):
        progbar = ProgressBar()
        
        obj.logpath = selected
        obj.switchscreen(progbar)
        obj.tlog = mp.TelemetryLog(selected[0], progbar, obj.postopen, obj.posterror)

    #callback for succesfully opening a log
    def postopen(self, dt):
        
        if self.tlog is None:
            return
        else:
            self.log = self.tlog.packets
            
        self.mode_menu = ModeMenu()
        self.mode_menu.readbtn.bind(on_press=self.readlog)
        self.mode_menu.graphbtn.bind(on_press=self.graphlog)
        self.mode_menu.exportbtn.bind(on_press=self.exportmenu)
        
        self.switchscreen(self.mode_menu)

    #callback for encountering an error
    #while opening a log
    def posterror(self, message, dt):
        print(message)
        self.switchscreen(self.startmenu)
        errorpopup = Popup(title='Error',
                      content=Label(text=message),
                           size_hint=(None, None), size=(600,200))
        errorpopup.open()
        
    def readlog(obj, value):
        rl = Reader(obj.log)
        obj.switchscreen(rl)
        
    def graphlog(obj, value):
        graph = TelemetryGraphScreen(obj, obj.log)

    def exportmenu(obj, value):
        obj.switchscreen(ExportMenu(obj.log, obj.logpath))
        
    def switchscreen(self, widget, *args):
        self.clear_widgets()
        self.add_widget(widget)
    
    def goback(self, window, key, *args):
        if key == 27:
            exit_on_back = StartMenu
            startmenu_on_back = (FileChooserListView, ModeMenu)
  
            if isinstance(self.children[0], exit_on_back):
                return False

            if isinstance(self.children[0], startmenu_on_back):
                self.switchscreen(self.startmenu)
            else:
                self.switchscreen(self.mode_menu)
            
            return True

        
class LogViewApp(App):
    def build(self):
        return ScreenManager()
    

if __name__ == '__main__':
    LogViewApp().run()
    
