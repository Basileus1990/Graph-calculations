from kivy_garden.graph import Graph, SmoothLinePlot
from kivy.properties import NumericProperty, StringProperty
from math import sin


class MainGraph(Graph):
    # Graph Properties
    xlabel_name = StringProperty()
    ylabel_name = StringProperty()
    xmin = NumericProperty()
    xmax = NumericProperty()
    ymin = NumericProperty()
    ymax = NumericProperty()

    def __init__(self, **kwargs):
        super(MainGraph, self).__init__(**kwargs)

        # assigning the default values
        self.xlabel_name = 'X'
        self.ylabel_name = 'Y'
        self.xmin = 0
        self.xmax = 10
        self.ymin = -1
        self.ymax = 1

    def update_graph(self):
        plot = SmoothLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x / 10, sin(x / 10)) for x in range(self.xmin * 10, self.xmax * 10 + 1)]
        self.add_plot(plot)