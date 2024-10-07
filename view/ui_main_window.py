# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowJxIkhn.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize)
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QFont
from screeninfo import get_monitors
from view.TTS_Widgets import (Header, RobotoLabel, ShortCutTab, SvgIcon, ShortCutButton)

class Ui_MainWindow(object):
    #TODO Make another file with configuration or structuring this
    SHORTCUTS_STYLE = u"background-color: rgb(220, 230, 241);\n border-radius: 5px"
    HEADER_STYLE = u"background-color: rgb(250, 249, 246);\n"
    SHORTCUT_PADDING = 20
    SHORTCUT_HEIGHT = 40
    SHORTCUT_MARGIN = SHORTCUT_HEIGHT + 5
    LABEL_HEIGHT = 30
    SHORTCUT_LABEL_MARGIN = LABEL_HEIGHT + 10
    BLURE_RADIUS = 20
    SHORTCUT_BUTTON_STYLE = u"QPushButton{\nbackground-color: rgb(26, 58, 111);\nborder-radius: 5px\n}\nQPushButton:hover{\nbackground-color: rgb(39, 74, 132);\n}\nQPushButton:pressed{\nbackground-color: rgb(20, 42, 82);\n}"

    _shortCutButton = []

    def setupUi(self, MainWindow, starterIcon, starterHeaderText, shortCutButtonsModel):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

        for monitor in get_monitors():
            monitorWidth = int(monitor.width/1.5)
            monitorHeight = int(monitor.height/1.5)
        headerHeight = int(monitorHeight * 0.1)
        shortCutsWidth = int(monitorWidth * 0.25)
        shortCutsHeight = 626 #TODO Calculate for different screen resolution

        MainWindow.setFixedSize(QSize(monitorWidth, monitorHeight))
        MainWindow.setStyleSheet(u"background-color: rgb(250, 249, 246);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self._header = Header(self.centralwidget, u"_header", 0, 0, monitorWidth, headerHeight, self.HEADER_STYLE, self.BLURE_RADIUS, 1, 1)

        self._headerIcon = SvgIcon(self._header, starterIcon, 
                                   headerHeight-10, headerHeight-10, 5, 5, "background-color: transparent;")

        self._headerLabel = RobotoLabel(self._header, starterHeaderText, 24, QFont.Bold, "background-color: transparent; color: #3F3F3F;", 
                                        headerHeight, headerHeight/4.5)

        self._shortCutsTab = ShortCutTab(self.centralwidget, u"_shortCutsTab", 10, 85, shortCutsWidth, shortCutsHeight, self.SHORTCUTS_STYLE)
        
        self._navigationLabel = RobotoLabel(self._shortCutsTab, "Навігація:", 18, QFont.Bold, "background-color: transparent; color: #3F3F3F;", 
                                            self.SHORTCUT_PADDING, self.SHORTCUT_PADDING)

        for i in range(len(shortCutButtonsModel)):
            padding = (i*self.SHORTCUT_MARGIN) + self.SHORTCUT_PADDING
            button = ShortCutButton(self._shortCutsTab, u"_shortCutButton", self.SHORTCUT_PADDING, self.SHORTCUT_LABEL_MARGIN+padding, 
                                    shortCutsWidth-self.SHORTCUT_PADDING*2, self.SHORTCUT_HEIGHT, self.SHORTCUT_BUTTON_STYLE, 
                                    shortCutButtonsModel[i].getIcon(), self.SHORTCUT_HEIGHT/1.5, self.SHORTCUT_HEIGHT/1.5, 5, 6, "background-color: transparent;",
                                    shortCutButtonsModel[i].getText(), 14, QFont.Normal, "background-color: transparent; color: #FFFFFF;", 10+self.SHORTCUT_HEIGHT/1.5, 6,
                                    shortCutButtonsModel[i].getDarkIcon())
            self._shortCutButton.append(button)
     
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Text-To-Speech Gen", None))
    # retranslateUi