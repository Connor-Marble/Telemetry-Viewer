from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.slider import Slider

from kivy.properties import ObjectProperty

from kivy.core.window import Window


from ..libs.garden.graph import Graph, MeshLinePlot
from ..libs.Mavlink.apm_mavlink_v1 import MAVLink_vfr_hud_message


class Reader(Widget):
    log = None
    log_text = ObjectProperty(Label)

    scroll_down = ObjectProperty(Button)
    scroll_up = ObjectProperty(Button)

    xscroll_down = ObjectProperty(Button)
    xscroll_up = ObjectProperty(Button)

    line_pos = ObjectProperty(Label)

    scrollbar = ObjectProperty(Slider)
    
    scrollpos = 0

    loglines = []
    
    def __init__(self, log, **kwargs):
        super(Reader, self).__init__()
        suReader = super(Reader, self)

        lineheight = self.log_text.font_size + 4
        self.lines = int((Window.size[1]-200)/lineheight - 2)
        
        self.scroll_down.bind(on_press=self.scroll)
        self.scroll_up.bind(on_press=self.scroll)

        self.xscroll_down.bind(on_press=self.scroll)
        self.xscroll_up.bind(on_press=self.scroll)

        self.scrollbar.bind(on_touch_move=self.scrollbar_moved)
        self.scrollbar.bind(on_touch_up=self.scrollbar_released)
        
        self.log_text.y = Window.size[1]/2
        self.log_text.text_size = (None, Window.size[1]-100)
        
        self.log_text.shorten = True
        
        self.log = log
        
        for i in range(len(self.log)):
            line = (str(self.log[i])+'\n')
            self.loglines.append(line)

        self.update_scroll_pos_label()
        self.DisplayLog()
        
    def DisplayLog(self):
        log_text = ''.join(self.loglines[
            self.scrollpos:self.lines+self.scrollpos])
        
        self.log_text.text = log_text
        self.log_text.texture_update()
        self.log_text.x = self.log_text.texture_size[0]*0.5

    def scroll(instance, value):

        buttonText = value.text
        
        if value == instance.scroll_down:
            instance.scrollpos += 1
        if value == instance.scroll_up:
            instance.scrollpos -= 1
        if value == instance.xscroll_down:
            instance.scrollpos += 10
        if value == instance.xscroll_up:
            instance.scrollpos -= 10

        instance.clamp_scroll()
        instance.update_scroll_pos_label()
        instance.DisplayLog()

    def update_scroll_pos_label(self):
        self.line_pos.text =\
            'lines: ' + str(self.scrollpos) +\
            ' - ' + str(self.scrollpos + self.lines) +\
            '/' + str(len(self.loglines))

    def scrollbar_moved(instance, value, scrollvalue):
        instance.scrollpos = int(
            ((100-instance.scrollbar.value)/100) *
            len(instance.loglines))
        
        instance.clamp_scroll()
        instance.update_scroll_pos_label()

    def scrollbar_released(instance, value, scrollvalue):
        instance.DisplayLog()

    def clamp_scroll(self):
        self.scrollpos = max(0, min(self.scrollpos,
                                    len(self.loglines)))
        
        
class TelemetryGraphScreen():
    
    def __init__(self, layout, log):
        self.log = log

        graph = self.getgraphwidget()
        if graph is not None:
            layout.clear_widgets()
            layout.add_widget(graph)

    def getgraphwidget(self):
        altitudes = []
        for i in self.log:
            if type(i) is MAVLink_vfr_hud_message:
                altitudes.append(i.alt)

        if len(altitudes) is 0:
            return

        graph = Graph(size=(400, 400),
                      xlabel='packet number',
                      ylabel='VRF HUD Alt', x_ticks_minor=5,
                      x_ticks_major=25, y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      x_grid=True, y_grid=True, xmin=0, xmax=len(altitudes),
                      ymin=min(altitudes), ymax=max(altitudes))
        
        plot = MeshLinePlot(color=[1, 1, 0, 1])
        plot.points = [(x, altitudes[int(x)]) for
                       x in xrange(0, len(altitudes))]
        
        graph.add_plot(plot)
        return graph
    
    
class StartMenu(Widget):
    filebtn = ObjectProperty(Button)

    
class ModeMenu(Widget):
    readbtn = ObjectProperty(Button)
    graphbtn = ObjectProperty(Button)
    exportbtn = ObjectProperty(Button)
    
    log = None

    
class ExportMenu(Widget):
    def __init__(self, log, logpath):
        super(ExportMenu, self).__init__()
        
        self.log = log
        print(logpath)
        self.logpath = logpath

    def savetext(self):
        filename = self.logpath[0]

        # remove file extension if one exists
        if '.' in filename:
            filename = filename[:filename.rindex('.')]

        filename += '.txt'
        with open(filename, 'w') as txt:
            for packet in self.log:
                txt.write(str(packet)+'\n')

    def savekml(self):
        pass
        
