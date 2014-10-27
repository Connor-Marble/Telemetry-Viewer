from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.properties import ObjectProperty

from ..libs.garden.graph import Graph, MeshLinePlot
from ..libs.Mavlink.apm_mavlink_v1 import MAVLink_vfr_hud_message

class Reader(Widget):
    log = None
    log_text = ObjectProperty(Label)

    scroll_down = ObjectProperty(Button)
    scroll_up = ObjectProperty(Button)
        
    scrollpos = 0

    def __init__(self, log, **kwargs):
        super(Reader,self).__init__()
        self.scroll_down.bind(on_press=self.scroll)
        self.scroll_up.bind(on_press=self.scroll)
        self.lines=super(Reader,self).height/7
        #TODO account for multi-line packages
        self.log_text.y = self.scroll_down.height
        self.loglines = []
        self.log = log
        
        for i in range(len(self.log)):
            line = (str(self.log[i])+'\n')
            self.loglines.append(line)
            
        print(len(self.loglines))
        print(len(self.log))
        
    def DisplayLog(self):
        log_text = ''.join(self.loglines[self.scrollpos:self.lines+self.scrollpos])
        self.log_text.text = log_text
        
    
    def scroll(instance, value):
        buttonText = value.text

        instance.scrollpos += 1 if buttonText == 'V' else -1
        
        instance.DisplayLog()

class TelemetryGraphScreen():
    
    def __init__(self, layout,log):
        self.log = log
        layout.clear_widgets()
        self.checkbox = CheckBox()
        graph = self.getgraphwidget()
        layout.add_widget(graph)



    def getgraphwidget(self):
        altitudes = []
        for i in self.log:
            if type(i) is MAVLink_vfr_hud_message:
                altitudes.append(i.alt)

        
        graph = Graph(size = (400,400),xlabel='packet number', ylabel='VRF HUD Alt', x_ticks_minor=5,
                      x_ticks_major=25, y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=-0, xmax=len(altitudes), ymin=min(altitudes), ymax=max(altitudes))
        plot = MeshLinePlot(color=[1, 1, 0, 1])
        plot.points = [(x, altitudes[int(x)]) for x in xrange(0, len(altitudes))]
        graph.add_plot(plot)
        return graph
    
    
class StartMenu(Widget):
    filebtn = ObjectProperty(Button)

class ModeMenu(Widget):
    readbtn = ObjectProperty(Button)
    graphbtn = ObjectProperty(Button)
    log = None

