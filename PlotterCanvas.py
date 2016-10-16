#!/usr/bin/python3
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=1, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # self.plotter = self.fig.add_subplot(111, polar=True)
        FigureCanvas.__init__(self, self.fig)

        # self.plotter.scatter(45*3.1416/180, 0.5, s=800)
        # We want to hold every plot in the figure
        # self.plotter.hold(True)
        # TODO: Set angular grid off
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot_data(self, data):
        self.plotter.plot(data)

    def plot_scatter(self, theta, r, size, color):
        self.plotter.scatter(theta, r, c=color, s=size, alpha=0.5)
        self.draw()

    def renew(self):
        self.fig.clf()
        self.plotter = self.fig.add_subplot(111, polar=True)
        self.plotter.set_ylim(0, 1100)
        # self.plotter.axes.get_xaxis().set_visible(False)
