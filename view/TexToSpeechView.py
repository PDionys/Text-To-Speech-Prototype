from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PySide6.QtGui import QFont
from view.TTS_Widgets import *

class TexToSpeech:
    def __init__(self, bodyLayout, controller):
        
        self.bodyWidget = QWidget()
        self.bodyWidget.setObjectName(u"bodyWidget")
        self.ttsVLayout = QVBoxLayout()
        self.bodyWidget.setLayout(self.ttsVLayout)
        self.ttsVLayout.setContentsMargins(0, 0, 0, 0)
        self.ttsVLayout.setSpacing(2)

        self.textInputWidget = QWidget()
        self.textInputWidget.setStyleSheet(u'background-color: transparent;')

        self.textInputEdit = QTextEdit(self.textInputWidget)
        self.textInputEdit.setGeometry(10, 10, 890, 220)
        self.textInputEdit.setFont(QFont('Roboto', 14, QFont.Normal))
        self.textInputEdit.setStyleSheet(u'background-color: white; color: black;')
        self.textInputEdit.textChanged.connect(self.word_count)

        self.textInputButton = QPushButton(self.textInputWidget)
        self.textInputButton.setText('Завантажити файл')
        self.textInputButton.move(10, self.textInputEdit.height()+20)
        self.textInputButton.setStyleSheet(u"QPushButton{\nbackground-color: rgb(26, 58, 111);\nborder-radius: 5px;\ncolor: #FFFFFF;\nborder: 0px;}"
                                    "\nQPushButton:hover{\nbackground-color: rgb(39, 74, 132);\n}\nQPushButton:pressed{"
                                    "\nbackground-color: rgb(20, 42, 82);\n}")
        self.textInputButton.setFont(QFont('Roboto', 18, QFont.Bold))
        self.textInputButton.adjustSize()
        self.textInputButton.clicked.connect(lambda: self.read_text_from_file(controller))

        self.textWordCounterLabel = RobotoLabel(self.textInputWidget, 'Кількість слів: 0', 14, QFont.Bold, 
                                                "background-color: transparent; border: 0px; color: #3F3F3F;", 
                                                700, self.textInputEdit.height()+20)
        self.textWordCounterLabel.setFixedWidth(200)

        self.ttsVLayout.addWidget(self.textInputWidget)

        self.modelSettinngWidget = QWidget()
        self.modelSettinngWidget.setStyleSheet(u'background-color: red;border: 5px solid black;')
        self.ttsVLayout.addWidget(self.modelSettinngWidget)

        bodyLayout.addWidget(self.bodyWidget)
    
    def read_text_from_file(self, controller):
        content = controller.openTextFile()
        self.textInputEdit.setText(content)

    def word_count(self):
        content = self.textInputEdit.toPlainText()
        splitSlashN = content.split('\n')
        count = 0
        for ele in splitSlashN:
            split = ele.split(' ')
            for e in split:
                if e != '':
                    count+=1

        self.textWordCounterLabel.setText(f'Кількість слів: {count}') 