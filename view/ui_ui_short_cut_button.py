from PySide6.QtWidgets import QPushButton, QLabel
from PySide6.QtCore import QRect
from PySide6.QtGui import QFont
from PySide6.QtSvgWidgets import QSvgWidget

class Ui_ShortCutButton(QPushButton):
    def __init__(self, widget, shortCutsWidth, buttonHeight, padding, labelHeight, i, iconPath, buttonText, darkIcon):
        super(Ui_ShortCutButton, self).__init__(widget)

        self.setObjectName(u"_shortCutButton")
        self.setGeometry(QRect(padding, labelHeight+i, shortCutsWidth-padding*2, buttonHeight))
        self.setStyleSheet(u"QPushButton{\n"
"background-color: rgb(26, 58, 111);\n"
"border-radius: 5px\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(39, 74, 132);\n"
"}\n"
"QPushButton:pressed{\n"
"	background-color: rgb(20, 42, 82);\n"
"}")
        self._buttonIcon = QSvgWidget(self)
        self._buttonIcon.load(iconPath)
        self._buttonIcon.setFixedSize(buttonHeight/1.5, buttonHeight/1.5)
        self._buttonIcon.setGeometry(QRect(5, 6, buttonHeight/1.5, buttonHeight/1.5))
        self._buttonIcon.setStyleSheet("background-color: transparent;")

        self._buttonLabel = QLabel(self)
        self._buttonLabel.setText(buttonText)
        self._buttonLabel.setFont(QFont("Roboto", 14, QFont.Normal))
        self._buttonLabel.setStyleSheet("background-color: transparent; color: #FFFFFF;")
        self._buttonLabel.move(10+buttonHeight/1.5, 6)

        self._darkIcon = darkIcon