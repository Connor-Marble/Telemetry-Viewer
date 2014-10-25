from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.checkbox import CheckBox

import math

from ..libs.garden.graph import Graph, MeshLinePlot
from ..libs.Mavlink.apm_mavlink_v1 import *

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
    
    
