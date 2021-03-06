from kivy_garden.graph import Graph, SmoothLinePlot
from kivy.properties import NumericProperty, StringProperty
import ctypes
import pathlib
import pygame
from math import sin
from Classes.calc_handler import CalcHandler

pygame.init()


class MainGraph(Graph):
    # Graph Properties
    xlabel_name = StringProperty()
    ylabel_name = StringProperty()
    xmin = NumericProperty()
    xmax = NumericProperty()
    ymin = NumericProperty()
    ymax = NumericProperty()
    main_window = None

    def __init__(self, **kwargs):
        super(MainGraph, self).__init__(**kwargs)

        # assigning the default values
        self.xlabel_name = 'X'
        self.ylabel_name = 'Y'
        self.xmin = -4
        self.xmax = 4
        self.ymin = -4
        self.ymax = 4

    def update_graph(self):
        plot = SmoothLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x / 10, sin(x / 10)) for x in range(
            self.xmin * 10, self.xmax * 10 + 1)]
        try:
            calc = CalcHandler(self.main_window)
            self.add_plot(calc.get_plot())
        except WrongInput as e:
            e.display_error_message()
            print(e)
            return

    # Removes all plots from graph
    def reset_graph(self):
        for i in range(len(self.plots)):
            self.remove_plot(self.plots[0])


class WrongInput(Exception):
    # displays error message and plays an error sound
    def display_error_message(self):
        sound_path = str(pathlib.Path(__file__).parent.parent.absolute()) + '\\Audio\\Error Sound.mp3'
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()

        ctypes.windll.user32.MessageBoxW(0, str(self), 'Your input isn\'t correct!', 0)
