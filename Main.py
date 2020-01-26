import kivy
kivy.require('1.11.1')

from kivy.config import Config
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '800')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'resizable', '0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.graph import Graph, SmoothLinePlot
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from math import sin, cos


class MainGraph(Graph):
    # Graph Properties
    xlabel_name = StringProperty('X')
    ylabel_name = StringProperty('Y')
    xmin = NumericProperty(-3)
    xmax = NumericProperty(3)
    ymin = NumericProperty(-10)
    ymax = NumericProperty(10)

    def update_graph(self):
        plot = SmoothLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x / 10, sin(x / 10)) for x in range(self.xmin * 10, self.xmax * 10 + 1)]
        self.add_plot(plot)


class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)


class GraphCalcApp(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    GraphCalcApp().run()
