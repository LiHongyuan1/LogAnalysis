# -*- coding: utf-8 -*-
# Android Logging Tool
# This tool help tester analyse Android Logging
# Version : beta
# Version V1.0

from PyQt5 import QtCore, QtWidgets

class SearchWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(399, 300)

        # 保留 widget 属性，指向 Dialog 本身
        self.widget = Dialog

        # 主垂直布局
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # 水平布局：Label + TextEdit
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.textEdit = QtWidgets.QTextEdit(self.widget)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)

        self.verticalLayout.addLayout(self.horizontalLayout)

        # 按钮区：Cancel 与 Ok
        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        # 文本翻译与信号连接保持不变
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Search    "))
