#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PlotterCanvas import MyMplCanvas as Plotter
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QWidget


# noinspection PyArgumentList
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.status_bar = QStatusBar()
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

        # Set the main window content ==================================================================================
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        h_box = QHBoxLayout()
        central_widget.setLayout(h_box)
        h_box.addWidget(self.plt)

        # Set window parameters
        self.status_bar.showMessage("Welcome to ERP Visualization Tool")
        self.setGeometry(0, 0, 600, 400)
        self.setWindowTitle('Visual ERP')
        self.show()

    def menu_open(self):
        print("open")

    def menu_about(self):
        print("Acerca de")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
