from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QLabel, QPushButton
from PySide6.QtCore import QRect
from PySide6.QtGui import QColor, QFont
from PySide6.QtSvgWidgets import QSvgWidget

class CustomWidget:
    def SetCustomWidgetProperty(self, objectName, xGeometry, yGeometry, gWidth, gHeight, style):
        self.setObjectName(objectName)
        self.setGeometry(QRect(xGeometry, yGeometry, gWidth, gHeight))
        self.setStyleSheet(style)
    
    def SetShadowEffect(self, blureRadius, xOffset, yOffset):
        self.headerShadowEffect = QGraphicsDropShadowEffect()
        self.headerShadowEffect.setBlurRadius(blureRadius)
        self.headerShadowEffect.setOffset(xOffset, yOffset)
        self.headerShadowEffect.setColor(QColor(0, 0, 0))
        self.setGraphicsEffect(self.headerShadowEffect)

class Header(QFrame, CustomWidget):
    def __init__(self, centralWidget, objectName, xGeometry, yGeometry, gWidth, gHeight, style, blureRadius, xOffset, yOffset):
        super(Header, self).__init__(centralWidget)

        self.SetCustomWidgetProperty(objectName, xGeometry, yGeometry, gWidth, gHeight, style)
        self.setFrameShape(QFrame.NoFrame)
        self.SetShadowEffect(blureRadius, xOffset, yOffset)

class ShortCutTab(QFrame, CustomWidget):
    def __init__(self, centralWidget, objectName, xGeometry, yGeometry, gWidth, gHeight, style):
        super(ShortCutTab, self).__init__(centralWidget)

        self.SetCustomWidgetProperty(objectName, xGeometry, yGeometry, gWidth, gHeight, style)
        self.setFrameShape(QFrame.NoFrame)
        # self.SetShadowEffect(blureRadius, xOffset, yOffset)

class RobotoLabel(QLabel):
    def __init__(self, parentWidget, labelText, fontSize, fontTypeface , fontStyle, xMove, yMove):
        super(RobotoLabel, self).__init__(parentWidget)

        self.setText(labelText)
        self.setFont(QFont("Roboto", fontSize, fontTypeface))
        self.setStyleSheet(fontStyle)
        self.move(xMove, yMove)

class SvgIcon(QSvgWidget):
    def __init__(self, parentWidget, imgPath, imgWidth, imgHeight, xMove, yMove, imgStyle):
        super(SvgIcon, self).__init__(parentWidget)

        self.load(imgPath)
        self.setFixedSize(imgWidth, imgHeight)
        self.move(xMove, yMove)
        # self._headerIcon.setGeometry(QRect((headerHeight-headerHeight/1.5)/2, (headerHeight-headerHeight/1.5)/2, headerHeight/1.5, headerHeight/1.5))
        self.setStyleSheet(imgStyle)

class ShortCutButton(QPushButton, CustomWidget):
    def __init__(self, parentWidget, objectName, xGeometry, yGeometry, gWidth, gHeight, style, 
                 imgPath, imgWidth, imgHeight, xImgMove, yImgMove, imgStyle,
                 labelText, fontSize, fontTypeface , fontStyle, xFontMove, yFontMove,
                 darkIcon):
        super(ShortCutButton, self).__init__(parentWidget)

        self.SetCustomWidgetProperty(objectName, xGeometry, yGeometry, gWidth, gHeight, style)

        self._buttonIcon = SvgIcon(self, imgPath, imgWidth, imgHeight, xImgMove, yImgMove, imgStyle)
        self._buttonLabel = RobotoLabel(self, labelText, fontSize, fontTypeface , fontStyle, xFontMove, yFontMove)
        self._darkIcon = darkIcon

class TTS_Frame(QFrame, CustomWidget):
    def __init__(self, parentWidget, objectName, style, blureRadius, xOffset, yOffset):
        super(TTS_Frame, self).__init__(parentWidget)

        self.SetCustomWidgetProperty(objectName, 0, 0, 0, 0, style)
        self.SetShadowEffect(blureRadius, xOffset, yOffset)