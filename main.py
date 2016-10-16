#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QDoubleSpinBox
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QSpinBox

from PlotterCanvas import MyMplCanvas as Plotter
import numpy as np
from DataManager import DataObject, PolarConverter
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon

FAC_AMP = 200
TIME_MAX = 400

# noinspection PyArgumentList
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.status_bar = QStatusBar()
        self.samples_list_widget = QListWidget()
        self.button_process = QPushButton()
        self.label_panel_title = QLabel('<b>Samples Panel</b>')

        self.plt = Plotter(self)
        self.init_ui()

    def init_ui(self):
        # Setup the actions =======================================================
        # Open Action
        open_action = QAction(QIcon('Resources/Icons/fileopen.png'), 'Load &ERP data', self)
        open_action.setStatusTip('Open Data Samples')
        open_action.triggered.connect(self.menu_open)
        # Exit Action
        exit_action = QAction(QIcon('Resources/Icons/exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(qApp.quit)
        # About Action
        about_action = QAction(QIcon('Resources/Icons/about.png'), '&About', self)
        about_action.setStatusTip('About')
        about_action.triggered.connect(self.menu_about)

        # Generate the menu bar ====================================================
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        help_menu = menu_bar.addMenu('&Help')

        # Add actions to file menu
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)
        # Add actions to Help menu
        help_menu.addAction(about_action)

        # Set status bar
        self.setStatusBar(self.status_bar)

        # Connect list with status bar
        self.samples_list_widget.itemClicked.connect(self.item_selected)

        # Set the main window content ==================================================================================
        self.samples_list_widget.setMaximumWidth(200)
        self.button_process.setText('Plot Sample...')
        self.label_panel_title.setAlignment(QtCore.Qt.AlignHCenter)

        # Set the params plot Group box ============================
        param_gb = QGroupBox()
        param_gb.setTitle('Plot Parameters')
        layout_params = QVBoxLayout(param_gb)

        label_params1 =QLabel('Time Interval:   ')
        self.spinbox_params1 = QSpinBox()
        label_params2 = QLabel('Amplitude Min: ')
        self.spinbox_params2 = QDoubleSpinBox()

        self.spinbox_params1.setMaximum(TIME_MAX)
        self.spinbox_params1.setValue(80)

        self.spinbox_params2.setValue(0.0)
        self.spinbox_params2.setSingleStep(0.1)
        self.spinbox_params2.setDecimals(1)

        layout_amplitude = QHBoxLayout()
        layout_amplitude.addWidget(label_params1)
        layout_amplitude.addWidget(self.spinbox_params1)

        layout_time = QHBoxLayout()
        layout_time.addWidget(label_params2)
        layout_time.addWidget(self.spinbox_params2)

        self.radio_mode1 = QRadioButton()
        self.radio_mode2 = QRadioButton()

        self.radio_mode1.setText('Channel Order')
        self.radio_mode2.setText('Head Order')
        self.radio_mode1.setChecked(True)

        layout_params.addLayout(layout_amplitude)
        layout_params.addLayout(layout_time)
        layout_params.addWidget(self.radio_mode1)
        layout_params.addWidget(self.radio_mode2)

        panel_layout = QVBoxLayout()
        panel_layout.addWidget(self.label_panel_title)
        panel_layout.addWidget(self.samples_list_widget)
        panel_layout.addWidget(param_gb)
        panel_layout.addStretch(1)
        panel_layout.addWidget(self.button_process)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        main_layout.addWidget(self.plt)
        main_layout.addLayout(panel_layout)

        # Set window parameters
        self.status_bar.showMessage("Welcome to ERP Visualization Tool")
        self.setGeometry(0, 0, 1000, 600)
        self.setWindowTitle('Visual ERP')

        self.button_process.clicked.connect(self.plot_sample)

        self.show()
        # For debug purposes
        self.menu_open()

    def item_selected(self, item):
        # TODO: Manage changes in selection with keys
        self.status_bar.showMessage('Sample: %s' % item.text())

    def menu_open(self):
        # TODO: File chooser
        self.data_object = DataObject('data_erp.mat')
        self.samples_list_widget.clear()
        self.samples_list_widget.insertItems(0, self.data_object.get_titles())

    def menu_about(self):
        print("About")

    def plot_sample(self):
        # Error management
        selected = self.samples_list_widget.currentItem()
        if selected is None:
            return

        self.plt.renew()
        sample_title = selected.text()
        self.status_bar.showMessage('Plotting (%s), Please wait ...' % sample_title)
        self.plot_mode1(self.data_object.get_sample(sample_title))
        self.status_bar.showMessage('Plotting (%s), Done.' % sample_title)

    def plot_mode1(self, data):
        time_interval = self.spinbox_params1.value()
        amplitude_min = self.spinbox_params2.value()

        shape = self.data_object.get_shape(data)
        angle_interval = 360. / shape[0]
        pc = PolarConverter(x_range=time_interval, y_min=amplitude_min)

        # [Time, Amplitude] vectors
        angle = 0
        # big_plot = []
        for channel in data:
            polar_data = pc.polar_scatter_conversion(channel)
            r = polar_data[0]
            theta = np.ones([1, len(r)]) * angle * np.pi / 180.0
            size = np.abs(polar_data[1]) * FAC_AMP
            color = polar_data[2]

            # big_plot.append([theta, r, size, color])
            self.plt.plot_scatter(theta, r, size, color)
            angle += angle_interval

        # for dot in big_plot:
        #    self.plt.plot_scatter(dot[0], dot[1], dot[2], dot[3])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
