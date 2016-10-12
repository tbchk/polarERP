#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QPushButton

from PlotterCanvas import MyMplCanvas as Plotter
from DataManager import DataObject
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QWidget


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
        open_action = QAction(QIcon('Resources/Icons/fileopen.png'), 'Open &ERP data', self)
        open_action.setStatusTip('Open Data')
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

        panel_layout = QVBoxLayout()
        panel_layout.addWidget(self.label_panel_title)
        panel_layout.addWidget(self.samples_list_widget)
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
        self.show()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
