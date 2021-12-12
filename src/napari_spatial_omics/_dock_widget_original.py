"""
This module is an example of a barebones QWidget plugin for napari

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton
from magicgui import magic_factory
from napari.layers import Points


class ExampleQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        btn = QPushButton("Click me!")
        btn.clicked.connect(self._on_click)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(btn)

    def _on_click(self):
        print("napari has", len(self.viewer.layers), "layers")


@magic_factory
def example_magic_widget(
        spot_map: "napari.layers.Points",
        gene: str = 'IGHG1',
        color: str = 'red',
        size: str = '10'
    ) -> "napari.layers.Points":
    #print(f"you have selected {img_layer}")
    data = [spot_map.data[i].tolist() for i in range(len(spot_map.data)) if spot_map.properties['gene'][i] == gene]
    return Points(data, size=int(size), face_color=color)

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return [example_magic_widget, ExampleQWidget]
"""

from qtpy.QtWidgets import QWidget
from napari_plugin_engine import napari_hook_implementation
#from magicgui import magic_factory

class MyWidget(QWidget):
    def __init__(selfself, napari_viewer):
        self.viewer = napari_viewer
        super().__init__()

        # initialize layout
        layout = QGridLayout()

        # add a button
        btn = QPushButton('Click me!', self)
        def trigger():
            print("napari has", len(napari_viewer.layers), "layers")
        btn.clicked.connect(trigger)
        layout.addWidget(btn)

        # activate layout
        self.setLayout()

@napari_hook_implementation
def napari_experimental_provide_dock_widget:
    return MyWidget
"""
