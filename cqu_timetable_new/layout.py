# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindowEghyFy.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(560, 244)
        MainWindow.setMinimumSize(QSize(482, 244))
        MainWindow.setMaximumSize(QSize(560, 300))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.startDate = QLineEdit(self.centralwidget)
        self.startDate.setObjectName(u"startDate")

        self.verticalLayout.addWidget(self.startDate)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.fileSelectText = QLineEdit(self.centralwidget)
        self.fileSelectText.setObjectName(u"fileSelectText")

        self.horizontalLayout.addWidget(self.fileSelectText)

        self.BFileSelect = QPushButton(self.centralwidget)
        self.BFileSelect.setObjectName(u"BFileSelect")
        self.BFileSelect.setMinimumSize(QSize(30, 0))
        self.BFileSelect.setMaximumSize(QSize(50, 16777215))
        self.BFileSelect.setCheckable(False)

        self.horizontalLayout.addWidget(self.BFileSelect)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.fileSaveText = QLineEdit(self.centralwidget)
        self.fileSaveText.setObjectName(u"fileSaveText")

        self.horizontalLayout_2.addWidget(self.fileSaveText)

        self.BFileSave = QPushButton(self.centralwidget)
        self.BFileSave.setObjectName(u"BFileSave")
        self.BFileSave.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.BFileSave)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.alarmCheck = QCheckBox(self.centralwidget)
        self.alarmCheck.setObjectName(u"alarmCheck")

        self.horizontalLayout_4.addWidget(self.alarmCheck)

        self.durationText = QLineEdit(self.centralwidget)
        self.durationText.setObjectName(u"durationText")

        self.horizontalLayout_4.addWidget(self.durationText)

        self.BBrowser = QPushButton(self.centralwidget)
        self.BBrowser.setObjectName(u"BBrowser")

        self.horizontalLayout_4.addWidget(self.BBrowser)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.Bhelp = QPushButton(self.centralwidget)
        self.Bhelp.setObjectName(u"Bhelp")
        self.Bhelp.setCheckable(False)

        self.horizontalLayout_3.addWidget(self.Bhelp)

        self.runOnBox = QDialogButtonBox(self.centralwidget)
        self.runOnBox.setObjectName(u"runOnBox")
        self.runOnBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.horizontalLayout_3.addWidget(self.runOnBox)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u8bfe\u8868\u8f6c\u6362\u5de5\u5177", None))
#if QT_CONFIG(tooltip)
        self.startDate.setToolTip(QCoreApplication.translate("MainWindow", u"\u4ec0\u4e48\u65f6\u95f4\u884c\u8bfe\u8bf7\u770b\u6821\u5386", None))
#endif // QT_CONFIG(tooltip)
        self.startDate.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u586b\u5199\u884c\u8bfe\u65e5\u671f\uff0c\u5982 20210301", None))
        self.fileSelectText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u9009\u62e9\u8bfe\u8868\u6587\u4ef6\u8def\u5f84\uff0c\u8bf7\u52ff\u5305\u542b\u4e2d\u6587", None))
        self.BFileSelect.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.fileSaveText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u9009\u62e9\u4fdd\u5b58\u8bfe\u8868\u6587\u4ef6\u7684\u8def\u5f84", None))
        self.BFileSave.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.alarmCheck.setToolTip(QCoreApplication.translate("MainWindow", u"\u90e8\u5206\u673a\u578b\u53ef\u80fd\u5e76\u4e0d\u751f\u6548", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.alarmCheck.setWhatsThis(QCoreApplication.translate("MainWindow", u"\u90e8\u5206\u673a\u578b\u53ef\u80fd\u5e76\u4e0d\u751f\u6548", None))
#endif // QT_CONFIG(whatsthis)
        self.alarmCheck.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u9192\u5f00\u542f", u"\u90e8\u5206\u673a\u578b\u53ef\u80fd\u4e0d\u751f\u6548"))
#if QT_CONFIG(tooltip)
        self.durationText.setToolTip(QCoreApplication.translate("MainWindow", u"\u4ec5\u5f53\u5f00\u542f\u63d0\u9192\u540e\u751f\u6548", None))
#endif // QT_CONFIG(tooltip)
        self.durationText.setText("")
        self.durationText.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u63d0\u9192\u63d0\u524d\u65f6\u95f4\uff08\u5206\u949f\uff09", None))
        self.BBrowser.setText(QCoreApplication.translate("MainWindow", u"\u524d\u5f80 my.cqu.edu.cn", None))
        self.Bhelp.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u8bf4\u660e", None))
    # retranslateUi

