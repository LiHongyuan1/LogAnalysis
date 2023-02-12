# -*- coding: utf-8 -*-
# Android Logging Tool
# This tool help tester analyse Android Logging
# Version : beta
import sys

from PyQt5.QtWidgets import QApplication

from dataprocessing import DataProcess
from mainwindowfunction import MainWindowFunction

if __name__ == '__main__':
    DataProcess = DataProcess()
    syncapp = QApplication(sys.argv)
    synclogtool = MainWindowFunction()
    synclogtool.show()
    sys.exit(syncapp.exec())
