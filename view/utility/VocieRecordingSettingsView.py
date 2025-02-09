from view.TTS_Widgets import (RobotoLabel)
from PySide6.QtWidgets import (QComboBox, QLineEdit, QTextEdit, QPushButton, QSlider, QGroupBox, QCheckBox, QWidget, QSpinBox)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Slot

class Save:
    def __init__(self, parent, controller):
        self.saveLabel = RobotoLabel(parent, 'Який тип збереження:', 24, QFont.Normal, "background-color: transparent; border: 0px; color: #3F3F3F;", 10, 10)
        self.saveComboBox = QComboBox(parent)
        self.saveComboBox.setStyleSheet(u"background-color: white; color: black;")
        self.saveComboBox.setFont(QFont('Roboto', 16, QFont.Normal))
        self.saveComboBox.move(10, 44+10)
        self.saveComboBox.addItems(controller.setSavingMethods())
        self.saveComboBox.activated.connect(lambda ch, combo = self.saveComboBox: self.onComboBoxActivated(combo, parent))
        self.saveName = QLineEdit(parent)
        self.saveName.setStyleSheet(u"background-color: white; color: black;")
        self.saveName.setGeometry(10+360, 44+10, 350, 35)
        self.saveName.setFont(QFont('Roboto', 16, QFont.Normal))
        self.saveName.setText('Назва файлу')
        self.saveTextEdit = QTextEdit(parent)
        self.saveTextEdit.setStyleSheet(u"background-color: white; color: black;")
        self.saveTextEdit.setGeometry(10, 95, 0, 0)
        self.saveTextEdit.setFont(QFont('Roboto', 14, QFont.Normal))
        self.saveButton = QPushButton(parent)
        self.saveButton.setStyleSheet(u"QPushButton{\nbackground-color: rgb(26, 58, 111);\nborder-radius: 5px;\ncolor: #FFFFFF;\nborder: 0px;}"
                                    "\nQPushButton:hover{\nbackground-color: rgb(39, 74, 132);\n}\nQPushButton:pressed{"
                                    "\nbackground-color: rgb(20, 42, 82);\n}")
        self.saveButton.setText('Зберегти')
        self.saveButton.setFont(QFont('Roboto', 18, QFont.Normal))
        self.saveButton.adjustSize
        self.saveButton.move(10, 95)
        self.saveButton.clicked.connect(lambda ch, combo = self.saveComboBox, fileName = self.saveName: controller.save_audio(combo, fileName))

    def onComboBoxActivated(self, combobox, parent):
        if combobox.currentIndex() == 0:
            self.saveTextEdit.setGeometry(10, 95, 0, 0)
            self.saveButton.move(10, 95)
        elif combobox.currentIndex() == 1:
            self.saveTextEdit.setGeometry(10, 95, parent.width()-20, parent.height()-95-50)
            self.saveButton.move(10, 95+self.saveTextEdit.height()+10)

class Settings:
    def __init__(self, parent, controller):
        self.inputLabel = RobotoLabel(parent, 'Пристрій вводу:', 24, QFont.Normal, "background-color: transparent; border: 0px; color: #3F3F3F;"
                                         , 10, 10)
        self.inputComboBox = QComboBox(parent)
        self.inputComboBox.setStyleSheet(u"background-color: white; color: black;")
        self.inputComboBox.setFont(QFont('Roboto', 16, QFont.Normal))
        self.inputComboBox.move(10, 44+10)
        self.inputComboBox.addItems(controller.setAviableMicrophone())
        self.inputComboBox.activated.connect(lambda ch, combo = self.inputComboBox: controller.change_microphone(combo))

        self.outputLabel = RobotoLabel(parent, 'Пристрій виводу:', 24, QFont.Normal, "background-color: transparent; border: 0px; color: #3F3F3F;"
                                         , 10, self.inputComboBox.geometry().y()+35)
        self.outputCombobox = QComboBox(parent)
        self.outputCombobox.setStyleSheet(u"background-color: white; color: black;")
        self.outputCombobox.setFont(QFont('Roboto', 16, QFont.Normal))
        self.outputCombobox.move(10, self.outputLabel.geometry().y()+45)
        self.outputCombobox.addItems(controller.setAviableOutputDevice())
        self.outputCombobox.activated.connect(lambda ch, combo = self.outputCombobox: controller.change_output_device(combo))

class Equalizer:
    def __init__(self, parent, controller, waveform):
        self.tempoLabel = RobotoLabel(parent, 'Темп:', 18, QFont.Bold, 
                                      "background-color: transparent; border: 0px; color: #3F3F3F;", 10, 10)
        self.tempoLineEdit = QLineEdit(parent)
        self.tempoLineEdit.move(10, self.tempoLabel.geometry().y()+35)
        self.tempoLineEdit.setText('100')
        self.tempoLineEdit.setFont(QFont('Roboto', 16, QFont.Normal))
        self.tempoLineEdit.setStyleSheet(u'background-color: white; color: black;')
        self.tempoLineEdit.adjustSize()

        self.volumeLabel = RobotoLabel(parent, "Гучність звуку:", 18, QFont.Bold, 
                                      "background-color: transparent; border: 0px; color: #3F3F3F;", self.tempoLineEdit.width() + 20, 10)
        self.volumeSlider = QSlider(Qt.Horizontal, parent)
        self.volumeSlider.setGeometry(self.tempoLineEdit.width() + 20, self.volumeLabel.geometry().y()+35, 200, 
                                      self.tempoLineEdit.height())
        self.volumeSlider.setStyleSheet("background-color: transparent; border: 0px;")
        self.volumeSlider.setMinimum(-36)
        self.volumeSlider.setMaximum(36)
        self.volumeSlider.setValue(0)
        # self.volumeSlider.valueChanged.connect(self.adjust_volume)
        
        self.panLabel = RobotoLabel(parent, 'Панорамувати:', 18, QFont.Bold, 
                                      "background-color: transparent; border: 0px; color: #3F3F3F;", 
                                      self.volumeSlider.width()+self.volumeSlider.geometry().x() + 20, 10)
        self.left = RobotoLabel(parent, 'L', 12, QFont.Bold, 
                                      "background-color: transparent; border: 0px; color: #3F3F3F;", 
                                      self.volumeSlider.width()+self.volumeSlider.geometry().x() + 20, self.volumeLabel.geometry().y()+35)
        self.panSlider = QSlider(Qt.Horizontal, parent)
        self.panSlider.setGeometry(self.left.geometry().x() + 10, self.volumeLabel.geometry().y()+35, 170, 
                                      self.tempoLineEdit.height())
        self.panSlider.setStyleSheet("background-color: transparent; border: 0px;")
        self.panSlider.setMinimum(0)
        self.panSlider.setMaximum(100)
        self.panSlider.setValue(50)
        # self.panSlider.valueChanged.connect(self.adjust_volume)
        self.right = RobotoLabel(parent, 'R', 12, QFont.Bold, 
                                      "background-color: transparent; border: 0px; color: #3F3F3F;", 
                                      self.panSlider.geometry().x() + self.panSlider.width(), self.volumeLabel.geometry().y()+35)
        
        self.equalizerButton = QPushButton(parent)
        self.equalizerButton.setStyleSheet(u"QPushButton{\nbackground-color: rgb(26, 58, 111);\nborder-radius: 5px;\ncolor: #FFFFFF;\nborder: 0px;}"
                                    "\nQPushButton:hover{\nbackground-color: rgb(39, 74, 132);\n}\nQPushButton:pressed{"
                                    "\nbackground-color: rgb(20, 42, 82);\n}")
        self.equalizerButton.setText('Застосувати')
        self.equalizerButton.setFont(QFont('Roboto', 18, QFont.Normal))
        self.equalizerButton.adjustSize()
        self.equalizerButton.move(10, self.tempoLineEdit.geometry().y() + 45)
        self.equalizerButton.clicked.connect(lambda ch, tempo = self.tempoLineEdit, volume = self.volumeSlider, 
                                             pan = self.panSlider: self.adjust_sound(controller, waveform, tempo, volume, pan))
    
    def adjust_sound(self, controller, waveform, tempo, volume, pan):
        # waveform.clear_waveform()
        controller.make_adjustement(tempo, volume, pan)
    
class Effects:
    def __init__(self, parent, controller):
        self.effectsRadioButton = [
            self.create_radio_button(parent, 'pitch'),
            self.create_radio_button(parent, 'reverb'),
            self.create_radio_button(parent, 'robotic')
        ]
        self.effectsGroupBox = [
            self.create_group_box(parent, 'pitch-box', 'Зміщення висоти'),
            self.create_group_box(parent, 'reverb-box', 'Ехо та реверберація'),
            self.create_group_box(parent, 'robotic-box', 'Роботизований ефект'),
        ]
        self.effectsParameters = [
            [
                RobotoLabel(None, 'Величина зміщення висоти (півтони):', 14, QFont.Bold, "background-color: transparent; border: 0px; color: #3F3F3F;", 10, 20),
                self.create_spin_box(400, 20, 'pitch-amount', 12, -12),
                RobotoLabel(None, 'Точне налаштування (центи):', 14, QFont.Bold, "background-color: transparent; border: 0px; color: #3F3F3F;", 10, 45),
                self.create_spin_box(310, 45, 'fine-tuning', 99, 0),
                RobotoLabel(None, '%', 14, QFont.Bold, "background-color: transparent; border: 0px; color: #3F3F3F;", 360, 45)
            ],
            [
                RobotoLabel(None, 'Інтенсивність реверберації:', 14, QFont.Bold, "background-color: transparent; border: 0px; color: #3F3F3F;", 10, 20),
                self.create_spin_box(300, 20, 'reverb-intensity', 100, 0),
                RobotoLabel(None, '%', 14, QFont.Bold, "background-color: transparent; border: 0px; color: #3F3F3F;", 360, 20),
                RobotoLabel(None, 'Згасання:', 14, QFont.Bold, "background-color: transparent; border: 0px; color: #3F3F3F;", 10, 45),
                self.create_spin_box(110, 45, 'reverb-decay', 100, 0),
                RobotoLabel(None, '%', 14, QFont.Bold, "background-color: transparent; border: 0px; color: #3F3F3F;", 170, 45),
            ],
            [
                RobotoLabel(None, 'Коефіцієнт висоти тону:', 14, QFont.Bold, "background-color: transparent; border: 0px; color: #3F3F3F;", 10, 20),
                self.create_spin_box(260, 20, 'pitch-factor', 200, 30),
                RobotoLabel(None, '%', 14, QFont.Bold, "background-color: transparent; border: 0px; color: #3F3F3F;", 320, 20),
                RobotoLabel(None, 'Частота тремоло:', 14, QFont.Bold, "background-color: transparent; border: 0px; color: #3F3F3F;", 10, 45),
                self.create_spin_box(190, 45, 'tremolo-frequency', 30, 1),
                RobotoLabel(None, 'Hz', 14, QFont.Bold, "background-color: transparent; border: 0px; color: #3F3F3F;", 240, 45),
                RobotoLabel(None, 'Глибина тремоло:', 14, QFont.Bold, "background-color: transparent; border: 0px; color: #3F3F3F;", 10, 70),
                self.create_spin_box(195, 70, 'tremolo-depth', 100, 0),
                RobotoLabel(None, '%', 14, QFont.Bold, "background-color: transparent; border: 0px; color: #3F3F3F;", 255, 70),
            ]
        ]

        for i in range(0, len(self.effectsGroupBox)):
            self.effectsRadioButton[i].move(10, (self.effectsGroupBox[i].height()*i+10)+10*i)
            self.effectsGroupBox[i].move(30, (self.effectsGroupBox[i].height()*i+10)+10*i)
            for j in range(0, len(self.effectsParameters[i])):
                self.effectsParameters[i][j].setParent(self.effectsGroupBox[i])
        
        self.effectsApplyButton = QPushButton(parent)
        self.effectsApplyButton.setStyleSheet(u"QPushButton{\nbackground-color: rgb(26, 58, 111);\nborder-radius: 5px;\ncolor: #FFFFFF;\nborder: 0px;}"
                                    "\nQPushButton:hover{\nbackground-color: rgb(39, 74, 132);\n}\nQPushButton:pressed{"
                                    "\nbackground-color: rgb(20, 42, 82);\n}")
        self.effectsApplyButton.setText('Застосувати')
        self.effectsApplyButton.setFont(QFont('Roboto', 18, QFont.Normal))
        self.effectsApplyButton.adjustSize()
        self.effectsApplyButton.move(10, len(self.effectsGroupBox)*self.effectsGroupBox[0].height() + 10 + 10*len(self.effectsGroupBox))
        self.effectsApplyButton.clicked.connect(lambda ch, radio = self.effectsRadioButton, group = self.effectsGroupBox,
                                                parameters = self.effectsParameters: controller.apply_effects(radio, group, parameters))
    
    def create_radio_button(self, parent, name):
        checkBox = QCheckBox(parent)
        checkBox.setObjectName(name)
        checkBox.setStyleSheet(u'background-color: transparent; border: 0px;')
        checkBox.setText('')
        # checkBox.move(x, y)
        return checkBox
    def create_group_box(self, parent, name, text):
        groupBox = QGroupBox(parent)
        groupBox.setObjectName(name)
        # groupBox.setStyleSheet(u'background-color: white; color: black; border: 2px')
        groupBox.setFont(QFont('Roboto', 14, QFont.Bold))
        groupBox.setTitle(text)
        groupBox.setGeometry(0, 0, 500, 100)
        return groupBox
    def create_spin_box(self, x, y, name, max, min):
        spinBox = QSpinBox()
        spinBox.setObjectName(name)
        spinBox.move(x, y)
        spinBox.setMaximum(max)
        spinBox.setMinimum(min)
        spinBox.setValue(0)
        spinBox.setFont(QFont('Roboto', 14, QFont.Bold))
        spinBox.setStyleSheet(u'background-color: white; color: black; border: 0px;')
        spinBox.adjustSize()
        return spinBox
