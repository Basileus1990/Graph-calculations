import kivy
kivy.require('1.11.1')

from kivy.config import Config
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '850')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'resizable', '0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty


class MainWindow(BoxLayout):
    bg_color = ListProperty([0.05, 0.05, 0.05, 1])
    main_window = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(*kwargs)
        self.main_window = self


class GraphCalcApp(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    GraphCalcApp().run()
