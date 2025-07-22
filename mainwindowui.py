# -*- coding: utf-8 -*-
import resource
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtWidgets import QAction, QHeaderView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 700)
        MainWindow.setWindowIcon(QIcon(':/sync.PNG'))

        # ---- Central widget: table + scrollbar ----
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self._configure_main_table()
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)

        self.verticalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.gridLayout.addWidget(self.verticalScrollBar, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        # ---- Menubar ----
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menu     = self.menubar.addMenu("")  # File
        self.menu_2   = self.menubar.addMenu("")  # Edit
        self.menu_3   = self.menubar.addMenu("")  # View
        self.menu_4   = self.menubar.addMenu("")  # Tools
        self.menuHelp = self.menubar.addMenu("")  # Help
        MainWindow.setMenuBar(self.menubar)

        # ---- Statusbar ----
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # ---- Toolbar ----
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(self.toolBar)
        self._create_toolbar_buttons(MainWindow)

        # ---- File menu actions ----
        self.actionopen     = QtWidgets.QAction(MainWindow)
        self.actionopen.setObjectName("actionopen")
        self.actionSave_File = QtWidgets.QAction(MainWindow)
        self.actionSave_File.setObjectName("actionSave_File")
        self.actionFilter   = QtWidgets.QAction(MainWindow)
        self.actionFilter.setObjectName("actionFilter")

        self.menu.addAction(self.actionopen)
        self.menu.addAction(self.actionSave_File)

        # ensure “Filter” 也在工具栏末尾
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionFilter)

        # add menus to menubar in order
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        # ---- Dock widget for filters ----
        self._create_dock_widget(MainWindow)

        # ---- Translations & signal-slot connections ----
        self.retranslateUi(MainWindow)
        # 按钮槽均已在 _create_toolbar_buttons 中连接
        # 其余按钮:
        self.toolButton.clicked.connect(self.addDockTableData)
        self.toolButton_2.clicked.connect(self.deleteDockTableData)
        self.toolButton_3.clicked.connect(self.clearDockTableData)
        self.toolButton_4.clicked.connect(self.loadKeywordJsonFile)
        self.toolButton_5.clicked.connect(self.saveKeywordJsonFile)
        self.toolButton_6.clicked.connect(self.applyKeywordJsonFileNew)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def _configure_main_table(self):
        """配置 central widget 中的 tableWidget"""
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(self.tableWidget.SelectRows)
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        # 固定列宽
        widths = {0:60, 2:60, 3:60, 4:60, 5:200, 6:1000}
        for col, w in widths.items():
            self.tableWidget.setColumnWidth(col, w)
        # 表头占位
        for i in range(7):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)


    def _create_toolbar_buttons(self, MainWindow):
        """创建并连接工具栏按钮（保持原来 9 个图标顺序不变）"""
        # 每项： (icon_path, tooltip_text, slot_method_name)
        buttons = [
            (':/filter.PNG',    "Filter window",         'dockWidgetShow'),
            (':/clear.PNG',     "clean all display sync+ log", 'clearData'),
            (':/renew.PNG',     "recovery sync+ log",    'displayAllData'),
            (':/find.PNG',      "find target by keyword",'keyworddisplay'),
            (':/highlight.PNG', "HighLight key word",    'layoutSearch'),
            (':/previous.PNG',  "find previous keyword", 'layoutSearchPrevious'),
            (':/next.PNG',      "find next keyword",     'layoutSearchNext'),
            (':/mark.PNG',      "Marks the selected row",'markSelectedRow'),
            (':/cancelmark.PNG',"Cancel Marks",          'CancelMarkSelectedRow'),
        ]
        for icon, tip, slot in buttons:
            act = QAction(QIcon(icon), "", MainWindow)
            act.setStatusTip(tip)
            act.setCheckable(True)
            # 连接到 MainWindowFunction 中对应的槽
            act.triggered.connect(getattr(MainWindow, slot))
            self.toolBar.addAction(act)


    def _create_dock_widget(self, MainWindow):
        """构建左侧 DockWidget（原样保留布局与控件名称）"""
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setObjectName("dockWidget")
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget)

        # 容器
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.dockWidget.setWidget(self.dockWidgetContents_2)

        # 嵌套 widget + layouts
        self.widget = QtWidgets.QWidget(self.dockWidgetContents_2)
        self.widget.setGeometry(QtCore.QRect(0, 10, 400, 550))
        self.widget.setObjectName("widget")
        vl_main = QtWidgets.QVBoxLayout(self.widget)
        vl_main.setContentsMargins(0,0,0,0)

        # 输入行
        self.lineEdit    = QtWidgets.QLineEdit(self.widget); self.lineEdit.setPlaceholderText("Date")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.widget); self.lineEdit_11.setPlaceholderText("TimeStamp")
        self.lineEdit_2  = QtWidgets.QLineEdit(self.widget); self.lineEdit_2.setPlaceholderText("Process")
        self.lineEdit_3  = QtWidgets.QLineEdit(self.widget); self.lineEdit_3.setPlaceholderText("Thread")
        self.lineEdit_4  = QtWidgets.QLineEdit(self.widget); self.lineEdit_4.setPlaceholderText("Level")
        self.lineEdit_9  = QtWidgets.QLineEdit(self.widget); self.lineEdit_9.setPlaceholderText("Tag")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.widget); self.lineEdit_10.setPlaceholderText("Message")

        for le in (self.lineEdit, self.lineEdit_11, self.lineEdit_2,
                   self.lineEdit_3, self.lineEdit_4, self.lineEdit_9,
                   self.lineEdit_10):
            vl_main.addWidget(le)

        # 上方三个按钮：Add/Delete/Clear
        hl1 = QtWidgets.QHBoxLayout()
        self.toolButton   = QtWidgets.QToolButton(self.widget)
        self.toolButton_2 = QtWidgets.QToolButton(self.widget)
        self.toolButton_3 = QtWidgets.QToolButton(self.widget)
        for tb in (self.toolButton, self.toolButton_2, self.toolButton_3):
            hl1.addWidget(tb)
        vl_main.addLayout(hl1)

        # Dock 表格
        self.dockTableWidget = QtWidgets.QTableWidget(self.widget)
        self.dockTableWidget.setObjectName("dockTableWidget")
        self.dockTableWidget.setColumnCount(8)
        self.dockTableWidget.setRowCount(0)
        # 列宽 & 隐藏
        col_w = {0:30,1:5,2:5,3:60,4:60,5:40,6:30,7:170}
        for c,w in col_w.items():
            self.dockTableWidget.setColumnWidth(c,w)
        self.dockTableWidget.hideColumn(1)
        self.dockTableWidget.hideColumn(2)
        # 表头占位
        for i in range(8):
            item = QtWidgets.QTableWidgetItem()
            self.dockTableWidget.setHorizontalHeaderItem(i, item)
        vl_main.addWidget(self.dockTableWidget)

        # 下方三个按钮：Load/Save/Apply Filters
        hl2 = QtWidgets.QHBoxLayout()
        self.toolButton_4 = QtWidgets.QToolButton(self.widget)
        self.toolButton_5 = QtWidgets.QToolButton(self.widget)
        self.toolButton_6 = QtWidgets.QToolButton(self.widget)
        for tb in (self.toolButton_4, self.toolButton_5, self.toolButton_6):
            hl2.addWidget(tb)
        vl_main.addLayout(hl2)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sync+ Logging Tool"))

        # 主表头
        headers = ["Date","Timestamp","Process","Thread","Level","Tag","Message"]
        for i, h in enumerate(headers):
            self.tableWidget.horizontalHeaderItem(i).setText(_translate("MainWindow", h))

        # 菜单
        self.menu.setTitle(_translate("MainWindow", "File"))
        self.menu_2.setTitle(_translate("MainWindow", "Edit"))
        self.menu_3.setTitle(_translate("MainWindow", "View"))
        self.menu_4.setTitle(_translate("MainWindow", "Tools"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))

        # File 菜单项
        self.actionopen.setText(_translate("MainWindow", "Open File"))
        self.actionSave_File.setText(_translate("MainWindow", "Save File"))
        self.actionFilter.setText(_translate("MainWindow", "TODO"))

        # 工具栏按钮文本保持原图标即可，不额外设置

        # Dock 表头
        dock_headers = ["Use","Date","TimeStamp","Process","Thread","Level","Tag","Message"]
        for i, h in enumerate(dock_headers):
            self.dockTableWidget.horizontalHeaderItem(i).setText(_translate("MainWindow", h))

        # toolButtons 文本
        self.toolButton.setText(_translate("MainWindow", "Add"))
        self.toolButton_2.setText(_translate("MainWindow", "Delete"))
        self.toolButton_3.setText(_translate("MainWindow", "Clear"))
        self.toolButton_4.setText(_translate("MainWindow", "Load Filters"))
        self.toolButton_5.setText(_translate("MainWindow", "Save Filters"))
        self.toolButton_6.setText(_translate("MainWindow", "Apply Filters"))


# ---- 不要再定义其他方法（如重复的 resizeEvent） ----
