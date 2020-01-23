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


class MainWindow(BoxLayout):
    # Graph variables
    graph = ObjectProperty(None)
    xlabel_name = StringProperty('X')
    ylabel_name = StringProperty('Y')
    xmin = NumericProperty(-10)
    xmax = NumericProperty(10)
    ymin = NumericProperty(-2)
    ymax = NumericProperty(2)

    def update_graph(self):
        plot = SmoothLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x, sin(x)) for x in range(self.xmin, self.xmax + 1)]
        self.graph.add_plot(plot)


class GraphCalcApp(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    GraphCalcApp().run()
