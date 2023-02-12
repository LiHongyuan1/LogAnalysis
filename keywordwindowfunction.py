# -*- coding: utf-8 -*-
# Android Logging Tool
# This tool help tester analyse Android Logging
# Version : beta

import logging

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QComboBox, QLineEdit, QListWidgetItem, QListWidget, QCheckBox, \
    QMainWindow, QDialog, QWidget

from modulekeywordwindowui import FilterWindow
from searchwindowui import SearchWindow

lst = []
select_key = ""


class ModuleFilterWindow(QMainWindow, FilterWindow):
    # 定义信号
    _signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(ModuleFilterWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.pushButton.clicked.connect(self.slot1)

    def slot1(self):
        data_str = self.lineEdit_4.text()
        # 发送信号
        self._signal.emit(data_str)
        self.close()


class highlightSearchWindow(QDialog, SearchWindow):
    # 定义信号
    _signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(highlightSearchWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.buttonBox.clicked.connect(self.slot1)

    def slot1(self):
        data_str = self.textEdit.toPlainText()
        self._signal.emit(data_str)
        self.close()


class ComboCheckBox(QComboBox):
    def __init__(self, items: list):
        """
        initial function
        :param items: the items of the list
        """

        super(ComboCheckBox, self).__init__()
        self.items = ["全选"] + items  # items list
        self.box_list = []  # selected items
        self.text = QLineEdit()  # use to selected items
        self.state = 0  # use to record state
        q = QListWidget()
        for i in range(len(self.items)):
            self.box_list.append(QCheckBox())
            self.box_list[i].setText(self.items[i])
            item = QListWidgetItem(q)
            q.setItemWidget(item, self.box_list[i])
            if i == 0:
                self.box_list[i].stateChanged.connect(self.all_selected)
            else:
                self.box_list[i].stateChanged.connect(self.show_selected)
        self.text.setReadOnly(True)
        self.setLineEdit(self.text)
        self.setModel(q.model())
        self.setView(q)

    def all_selected(self):
        """
        decide whether to check all
        return:
        """
        if self.state == 0:
            self.state = 1
            for i in range(1, len(self.items)):
                self.box_list[i].setChecked(True)
        else:
            self.state = 0
            for i in range(1, len(self.items)):
                self.box_list[i].setChecked(False)
        self.show_selected()

    def get_selected(self) -> list:
        """
        get selected items
        :return:
        """
        ret = []
        for i in range(1, len(self.items)):
            if self.box_list[i].isChecked():
                ret.append(self.box_list[i].text())
        return ret

    def show_selected(self):
        """
        show selected items
        :return:
        """
        global select_key
        self.text.clear()
        ret = '; '.join(self.get_selected())
        self.text.setText(ret)
        select_key = ret


class KeyWordWindow(QWidget):
    # 定义信号
    _signal = QtCore.pyqtSignal(list)

    def __init__(self):
        global lst
        super(KeyWordWindow, self).__init__()
        self.init_data()
        self.setWindowTitle('KeyWord')
        self.resize(600, 400)
        self.module = QComboBox()
        self.module.addItem("--Choose Module")
        for data in self.data_json:
            self.module.addItem(data['Module'])
        self.module.currentTextChanged.connect(self.slot_module_click)
        # layout = QVBoxLayout()
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(360, 220, 156, 200))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.accept_event)
        self.buttonBox.rejected.connect(self.cancel_event)
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.module, 0, 0, 1, 1)
        # self.layout.addWidget(self.buttonBox, 0, 1, 1, 1)

    def init_data(self):
        self.data_json = [
            {
                "Module": "AAR",
                "Keywords": [
                    {
                        "Keyword": "AARDataController"
                    }, {
                        "Keyword": "AARMainFragment"
                    }, {
                        "Keyword": "com.baidu.xiaoduos.launcher"
                    }, {
                        "Keyword": "logcat|grep \"\\-\\-LanDun\""
                    }
                ]
            },
            {
                "Module": "Account",
                "Keywords": [
                    {
                        "Keyword": "FaceOS_"
                    }, {
                        "Keyword": "AccountApp"
                    }, {
                        "Keyword": "com.ford.sync.fcs"
                    }
                ]
            }]

    # 读取json数据
    # with open("old.json", 'r', encoding='utf-8') as data:
    #   self.data_json = json.loads(data.read(), encoding='utf-8')

    def slot_module_click(self):
        global lst
        try:
            lst.clear()
            current_module = self.module.currentText()
            if current_module.startswith('--') is False:
                for data in self.data_json:
                    if data['Module'] == current_module:
                        # self.keyword.clear()
                        self.current_keyword_data = data['Keywords']
                        for c in data['Keywords']:
                            # self.keyword.addItem(c['Keyword'])
                            lst.append(c['Keyword'])
            else:
                self.keyword.clear()
        except:
            logging.exception("Load Module error")
        self.keyword = ComboCheckBox(lst)
        self.layout.addWidget(self.keyword, 0, 1, 1, 1)

    def accept_event(self):
        data_str = select_key.split(";")
        # 发送信号
        self._signal.emit(data_str)
        self.close()

    def cancel_event(self):
        self.close()
