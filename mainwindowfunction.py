# -*- coding: utf-8 -*-
# Android Logging Tool
# This tool help tester analyse Android Logging
# Version : beta

import logging
import json

import pandas as pd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QAbstractItemView
from keywordwindowfunction import highlightSearchWindow, KeyWordWindow
from dataprocessing import DataProcess
from mainwindowui import Ui_MainWindow
from pandas import DataFrame, isnull

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

global fname
filter_key = ""
te_data = []


def check_line_include_keyword(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    i = set1.intersection(set2)
    if [list2[_] for _ in range(len(list2)) if list2[_] in list1[6]]:
        return True
    elif 0 != len(i):
        return True
    else:
        return False


class MainWindowFunction(QMainWindow, Ui_MainWindow, DataProcess):
    rowCount = 0  # 单页可以显示的数据条数

    def __init__(self):
        super(MainWindowFunction, self).__init__()
        self.setupUi(self)
        self.searchwindow = highlightSearchWindow()
        self.keywordwindow = KeyWordWindow()
        self.signalsemit()
        self.dockWidget.close()

    def signalsemit(self):
        # save file
        self.actionSave_File.triggered.connect(self.handlesave)
        # open log file
        self.actionopen.triggered.connect(self.openfile)
        # check scroll bar value change
        self.verticalScrollBar.valueChanged.connect(self.pddatadisplay)

    def openfile(self):
        """
        open sync+ log file
        @return:
        """
        _translate = QtCore.QCoreApplication.translate
        fname = QFileDialog.getOpenFileName(self, 'Open file', '*.txt;*.log')
        if len(fname[0]) == 0:
            return
        with open(fname[0], "r", encoding="utf-8", errors="ignore") as infile:
            for line in infile:
                data = self.parse_linedata(line)
                if not data:
                    continue
                else:
                    row = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row)
                    te_data.append({
                        "Date": data[0],
                        "TimeStamp": data[1],
                        "Process": data[2],
                        "Thread": data[3],
                        "Level": data[4],
                        "Tag": data[5],
                        "Message": data[6],
                    })
        self.setdata(pd.DataFrame(te_data))

    def handlesave(self):
        """
        save log file
        @return:
        """
        _translate = QtCore.QCoreApplication.translate
        filename = QFileDialog.getSaveFileName(self, 'save file', '', '*.txt;*.log')
        # pyqt bug : if you cancel save file and software will crash
        if len(filename[0]) == 0:
            return
        with open(filename[0], 'w') as f:
            for row in range(self.tableWidget.rowCount()):
                if self.tableWidget.isRowHidden(row):
                    continue
                else:
                    row_data = []
                    ret = 0
                    for column in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(row, column)
                        if item is not None and ret < 5:
                            row_data.append(item.text())
                            ret = ret + 1
                        elif item is not None and ret == 5:
                            row_data.append(item.text() + ': ')
                        elif item is None and ret == 5:
                            row_data.append(' : ')
                    f.write("   ".join(row_data))
                    f.write("\n")
        f.close()

    def layoutSearch(self):
        """
        new sub-window for highlight keyword
        """
        self.searchwindow.show()
        self.searchwindow._signal.connect(self.quickDataLocation)

    def displayAllData(self):
        """
        display all log data
        """
        self.clearData()
        self.setdata(pd.DataFrame(te_data))
        self.verticalScrollBar.show()

    def clearData(self):
        """
        clean all logdata
        """
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()

    def displayFilterData(self, filter):
        """
        display Filter Data
        """
        rows = self.tableWidget.rowCount()
        for _ in range(int(rows)):
            self.tableWidget.setRowHidden(_, True)
        items = self.tableWidget.findItems(filter, Qt.MatchContains)
        for _ in range(len(items)):
            item = items[_].row()
            self.tableWidget.setRowHidden(item, False)

    def quickDataLocation(self, filter):
        """
        go to highlight data location
        """
        global filter_key
        filter_key = filter
        items1 = self.tableWidget.findItems(filter, Qt.MatchContains)
        for item1 in items1:
            item1.setForeground(QBrush(QColor(0, 0, 255)))  # blue
        self.tableWidget.setCurrentCell(0, 6)

    def layoutSearchNext(self):
        """
        go to next highlight dara
        """
        global filter_key
        items1 = self.tableWidget.findItems(filter_key, Qt.MatchContains)
        row = 0
        colum = 0
        for item1 in items1:
            currentRow = self.tableWidget.currentRow()
            row = item1.row()
            colum = item1.column()
            if currentRow < row:
                break
        self.tableWidget.setCurrentCell(row, colum)

    def layoutSearchPrevious(self):
        """
        go to previous highlight dara
        @return:
        """
        global filter_key
        items1 = self.tableWidget.findItems(filter_key, Qt.MatchContains)
        lens = len(items1) - 1
        row = 0
        colum = 0
        for _ in range(lens, -1, -1):
            currentRow = self.tableWidget.currentRow()
            row = items1[_].row()
            colum = items1[_].column()
            if currentRow > row:
                break
        self.tableWidget.setCurrentCell(row, colum)

    def markSelectedRow(self):
        """
        mark row highlight background
        @return:
        """
        self.tableWidget.currentItem().setBackground(QBrush(QColor(200, 200, 0)))
        row = self.tableWidget.currentItem().row()
        for colum in range(0, 7):
            item = self.tableWidget.item(row, colum)
            item.setBackground(QBrush(QColor(200, 200, 0)))

    def CancelMarkSelectedRow(self):
        """
        cancel mark row highlight background
        @return:
        """
        self.tableWidget.currentItem().setBackground(QBrush(QColor(255, 255, 255)))
        row = self.tableWidget.currentItem().row()
        for colum in range(0, 7):
            item = self.tableWidget.item(row, colum)
            item.setBackground(QBrush(QColor(255, 255, 255)))

    def keyworddisplay(self):
        """
        display keyword filter window
        @return:
        """
        self.keywordwindow.show()
        self.keywordwindow._signal.connect(self.displayKeywordData)

    def displayKeywordData(self, keyword):
        """
        display  filter data in main window
        @return:
        """
        rows = self.tableWidget.rowCount()
        for _ in range(int(rows)):
            current_row_name = self.tableWidget.item(_, 6).text()
            if any(word if word in current_row_name else False for word in keyword):
                self.tableWidget.setRowHidden(_, False)
            else:
                self.tableWidget.setRowHidden(_, True)

    def dockWidgetShow(self):
        """
        dock widget window show
        @return:
        """
        if self.dockWidget.show():
            return
        else:
            self.dockWidget.show()
            self.tableWidget.setColumnWidth(6, 500)

    def resizeEvent(self, event):
        width1 = int(event.size().width() * 0.3)
        self.resizeDocks([self.dockWidget], [width1], QtCore.Qt.Horizontal)

    def addDockTableData(self):
        """
        lineEdit = Date
        lineEdit_11 = Time Stamp
        lineEdit_2 = Process
        lineEdit_3 = Thread
        lineEdit_4 = Level
        lineEdit_9 = Module
        lineEdit_10 = Message
        """
        solt_dict = []
        solt_dict.append(self.lineEdit.text())
        solt_dict.append(self.lineEdit_11.text())
        solt_dict.append(self.lineEdit_2.text())
        solt_dict.append(self.lineEdit_3.text())
        solt_dict.append(self.lineEdit_4.text())
        solt_dict.append(self.lineEdit_9.text())
        solt_dict.append(self.lineEdit_10.text())

        row = self.dockTableWidget.rowCount()
        self.dockTableWidget.insertRow(row)
        self.check = QtWidgets.QTableWidgetItem()
        self.check.setCheckState(QtCore.Qt.Checked)
        self.dockTableWidget.setItem(row, 0, self.check)
        for _ in range(0, 7):
            item = QTableWidgetItem(solt_dict[_])
            self.dockTableWidget.setItem(row, _ + 1, item)
        self.dockTableWidget.setShowGrid(False)
        self.dockTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.lineDataClear()

    def lineDataClear(self):
        """
        clear Dock Table data after add into parameter
        @return:
        """
        self.lineEdit.clear()
        self.lineEdit_11.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_9.clear()
        self.lineEdit_10.clear()

    def deleteDockTableData(self):
        """
        delete dock table row which mouse choose
        @return:
        """
        currentrow = self.dockTableWidget.currentRow()  # 获取当前鼠标点击了第几行
        self.dockTableWidget.removeRow(currentrow)

    def clearDockTableData(self):
        """
        clear all dock table data
        @return:
        """
        self.dockTableWidget.setRowCount(0)
        self.dockTableWidget.clearContents()

    def loadKeywordJsonFile(self):
        """
        load keyword json file
        @return:
        """
        _translate = QtCore.QCoreApplication.translate
        fname = QFileDialog.getOpenFileName(self, 'Open file', '*.json')
        if len(fname[0]) == 0:
            return
        with open(fname[0], "r", encoding="utf-8", errors="ignore") as infile:
            try:
                info = json.load(infile)
                for _ in range(len(info)):
                    row = self.dockTableWidget.rowCount()
                    self.dockTableWidget.insertRow(row)
                    self.check = QtWidgets.QTableWidgetItem()
                    self.check.setCheckState(QtCore.Qt.Checked)
                    self.dockTableWidget.setItem(row, 0, self.check)
                    tmp_lst = []
                    for key, value in info[_].items():
                        tmp_lst.append(value)
                    for i in range(0, 7):
                        item = QTableWidgetItem(tmp_lst[i])
                        self.dockTableWidget.setItem(row, i + 1, item)
            except:
                infile.close()
        self.dockTableWidget.setShowGrid(False)
        self.dockTableWidget.verticalHeader().setDefaultSectionSize(10)

    def readDockTableWidgetData(self):
        """
        read all dock table widget data
        @return:
        """
        lst = []
        for row in range(self.dockTableWidget.rowCount()):
            save_dict = {}
            # use status == Null skip this keyword
            if 0 == self.dockTableWidget.item(row, 0).checkState():
                continue
            save_dict['Date'] = self.dockTableWidget.item(row, 1).text()
            save_dict['TimeStamp'] = self.dockTableWidget.item(row, 2).text()
            save_dict['Process'] = self.dockTableWidget.item(row, 3).text()
            save_dict['Thread'] = self.dockTableWidget.item(row, 4).text()
            save_dict['Level'] = self.dockTableWidget.item(row, 5).text()
            save_dict['Tag'] = self.dockTableWidget.item(row, 6).text()
            save_dict['Message'] = self.dockTableWidget.item(row, 7).text()
            lst.append(save_dict)
        return lst

    def saveKeywordJsonFile(self):
        """
        save all keyword json file for use configuration
        @return:
        """
        _translate = QtCore.QCoreApplication.translate
        filename = QFileDialog.getSaveFileName(self, 'save file', '', '*.json')
        save_lst = []
        if len(filename[0]) == 0:
            return
        with open(filename[0], 'w') as f:
            for row in range(self.dockTableWidget.rowCount()):
                save_dict = {}
                save_dict['Date'] = self.dockTableWidget.item(row, 1).text()
                save_dict['TimeStamp'] = self.dockTableWidget.item(row, 2).text()
                save_dict['Process'] = self.dockTableWidget.item(row, 3).text()
                save_dict['Thread'] = self.dockTableWidget.item(row, 4).text()
                save_dict['Level'] = self.dockTableWidget.item(row, 5).text()
                save_dict['Tag'] = self.dockTableWidget.item(row, 6).text()
                save_dict['Message'] = self.dockTableWidget.item(row, 7).text()
                save_lst.append(save_dict)
            json.dump(save_lst, f, indent=4)
        f.close()

    def applyKeywordJsonFile(self):
        """
        apply keyword for loading log and display filter data
        @return:
        """
        keyword = self.readDockTableWidgetData()
        cmp = []
        for _ in range(len(keyword)):
            for value in keyword[_].values():
                if 0 == len(value):
                    continue
                else:
                    cmp.append(value)
        rows = self.tableWidget.rowCount()
        for _ in range(int(rows)):
            data = [self.tableWidget.item(_, i).text() for i in range(7)]
            if check_line_include_keyword(data, cmp):
                self.tableWidget.setRowHidden(_, False)
            else:
                self.tableWidget.setRowHidden(_, True)

    def applyKeywordJsonFileNew(self):
        """
        handle keyword match loading log
        @return:
        """
        import datetime
        starttime = datetime.datetime.now()
        self.clearData()
        keyword = self.readDockTableWidgetData()
        for i in range(len(te_data)):
            for j in range(len(keyword)):
                keys = set(keyword[j].values()) - set(te_data[i].values())
                if ((len(keyword[j]['Message']) == 0 and 1 == int(len(keys))) or
                        (len(keyword[j]['Message']) != 0 and 0 == len(keyword[j]['Tag']) and
                         keyword[j]['Message'] in te_data[i]['Message']) or
                        (len(keyword[j]['Message']) != 0 and keyword[j]['Message'] in te_data[i]['Message'] and
                         (keyword[j]['Tag'] == te_data[i]['Tag'] or keyword[j]['Level'] == te_data[i]['Level'] or
                          keyword[j]['Thread'] == te_data[i]['Thread'] or keyword[j]['Process'] == te_data[i][
                              'Process']))):
                    row = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row)
                    tmp = 0
                    for value in te_data[i].values():
                        item = QTableWidgetItem(value)
                        self.tableWidget.setItem(row, tmp, item)
                        tmp = tmp + 1
        self.verticalScrollBar.hide()
        endtime = datetime.datetime.now()
        print((endtime - starttime).seconds)

    def setdata(self, df: DataFrame):
        self.df = df
        self.calculaterowparams()
        self.pddatadisplay()

    def calculaterowparams(self):
        if any(self.df):
            rowHeight = self.tableWidget.rowHeight(0)
            rowHeight = 30 if rowHeight == 0 else rowHeight
            tableHeight = self.tableWidget.height()
            self.rowCount = int(tableHeight / rowHeight) - 1
            self.tableWidget.setRowCount(self.rowCount)
            scrollbar_count = int(self.df.index.size / self.rowCount)
            self.verticalScrollBar.setMaximum(scrollbar_count * 9)

    def pddatadisplay(self):
        if any(self.df):
            df_columns = self.df.columns.size
            df_header = self.df.columns.values.tolist()
            self.tableWidget.setColumnCount(df_columns)
            self.tableWidget.setHorizontalHeaderLabels(df_header)
            start_row = int(self.verticalScrollBar.value() / 9 * self.rowCount)
            end_row = int((self.verticalScrollBar.value() / 9 + 1) * self.rowCount)
            for row in range(start_row, end_row):
                for column in range(df_columns):
                    value = ''
                    if row < self.df.index.size:
                        value = '' if isnull(self.df.iloc[row, column]) else str(self.df.iloc[row, column])
                    tempItem = QTableWidgetItem(value)
                    self.tableWidget.setItem((row - start_row), column, tempItem)
                    if self.tableWidget.item((row - start_row), column) is True:
                        self.tableWidget.item((row - start_row), column).setTextAlignment(Qt.AlignLeft)
