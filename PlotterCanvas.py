#!/usr/bin/python3
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.plotter = fig.add_subplot(111, polar=True)
        FigureCanvas.__init__(self, fig)

        # We want to hold every plot in the figure
        self.plotter.hold(True)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot_data(self):
        self.plotter.plot()
