from PySide6.QtWidgets import (QFrame, QWidget, QLabel, QHBoxLayout, QGridLayout, QComboBox, QTextEdit, QLineEdit)
from PySide6.QtGui import (QPainter, QPen)
from PySide6.QtCore import (QSize, QTimer, QPropertyAnimation)
from view.TTS_Widgets import *
from view.utility.VocieRecordingSettingsView import *
import numpy as np

class VoiceRecordingView():

    def __init__(self, bodyLayout, widget, controller):
        self.settingsButtons = []
        self.bodyWidget = QWidget()
        self.bodyWidget.setObjectName(u"bodyWidget")

        self.voiceRecordingFrame = Header(self.bodyWidget, u"voiceRecordingFrame", 0, 0, widget.width(), widget.height()/3, 
                                          u"background-color: rgb(250, 249, 246);", 20, 1, 1)
        
        #Заглушка для отображения волны звука
        self.waveLine = QFrame(self.voiceRecordingFrame)
        self.waveLine.setObjectName(u"waveLine")
        self.waveLine.setGeometry(10, 10, widget.width()-30, self.voiceRecordingFrame.height()/2)
        self.waveLine.setStyleSheet(u"background-color: rgb(30, 30, 30);border: 5px solid #3C3C3C;")
        self.waveFormWidget = WaveformWidget(self.waveLine, widget.width()-30, self.voiceRecordingFrame.height()/2)

        self.timerLabel = QLabel(self.voiceRecordingFrame)
        self.timerLabel.setObjectName(u"timerLabel")
        self.timerLabel.setFont(QFont("Roboto", 22, QFont.Normal))
        self.timerLabel.setText("00:00:00")
        self.timerLabel.adjustSize()
        self.timerLabel.move(widget.width()/2-180/3, self.voiceRecordingFrame.height()/2+10)
        
        self.recordingButtonWidget = QWidget(self.voiceRecordingFrame)
        self.recordingButtonWidget.setGeometry(widget.width()/2-180/2, self.voiceRecordingFrame.height()/2+10+30, 180, 60)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.resetRecordingButton = self.RecordButtonSetUp(u"playStopButton", 50, u"QPushButton{background-color: gray; border-radius: 25px;}"
                                                     "QPushButton:hover{background-color: #C0C0C0;}QPushButton:pressed{background-color: #696969;}"
                                                     )
        resetRecordingIcon = SvgIcon(self.resetRecordingButton, 'resources\\restart_alt_40dp_FFFFFF_FILL0_wght400_GRAD0_opsz40.svg', 40, 40, 5, 5, 
                               u"background-color: transparent;")
        self.resetRecordingButton.clicked.connect(lambda: self.reset_recording(controller))
        self.horizontalLayout.addWidget(self.resetRecordingButton)

        self.recordButton = self.RecordButtonSetUp(u"recordButton", 50, u"QPushButton{background-color: #C80000 ; border-radius: 25px;}"
                                                     "QPushButton:hover{background-color: #FF0000;}QPushButton:pressed{background-color: #900000;}"
                                                     )
        self.recordButton.clicked.connect(lambda: self.start_stop_timer(controller))
        self.recordIcon = SvgIcon(self.recordButton, 'resources\\mic_40dp_FFFFFF_FILL0_wght400_GRAD0_opsz40.svg', 40, 40, 5, 5, 
                               u"background-color: transparent;")
        self.horizontalLayout.addWidget(self.recordButton)

        self.playStopButton = self.RecordButtonSetUp(u"resetRecordingButton", 50, u"QPushButton{background-color: gray; border-radius: 25px;}"
                                                     "QPushButton:hover{background-color: #C0C0C0;}QPushButton:pressed{background-color: #696969;}"
                                                     )
        playStopIcon = SvgIcon(self.playStopButton, 'resources\\play_pause_40dp_FFFFFF_FILL0_wght400_GRAD0_opsz40.svg', 40, 40, 5, 5, 
                               u"background-color: transparent;")
        self.playStopButton.clicked.connect(lambda: self.start_stop_playing(controller))
        self.horizontalLayout.addWidget(self.playStopButton)
        self.recordingButtonWidget.setLayout(self.horizontalLayout)

        self.timer = QTimer(self.bodyWidget)
        self.timer.timeout.connect(self.update_time)
        self.time_elapsed = 0

        self.settingBodyQWidget = QWidget(self.bodyWidget)
        self.settingBodyQWidget.setStyleSheet(u"background-color: transparent;")
        self.settingBodyQWidget.setGeometry(0, widget.height()/3 + 10, widget.width()-20-175, (widget.height()/3)*2-30)
        self.settingBodyLayout = QHBoxLayout()
        self.settingBodyLayout.setContentsMargins(0,0,0,0)
        self.settingBodyQWidget.setLayout(self.settingBodyLayout)

        self.settingsButtonFrame = QFrame(self.bodyWidget)
        self.settingsButtonFrame.setStyleSheet(u"background-color: transparent;")
        self.settingsButtonFrame.setGeometry(widget.width() - 195, widget.height()/3 + 10, 175, 175)
        self.settingsButtonGridLayout = QGridLayout(self.settingsButtonFrame)
        self.settingsButtonGridLayout.setContentsMargins(5, 5, 5, 5)
        self.settingsButtonGridLayout.setSpacing(5)
        self.SettingsButtonSetUp(widget, controller)

        controller.audio_data_signal.connect(self.waveFormWidget.update_waveform)
        
        bodyLayout.addWidget(self.bodyWidget)

    def SettingsButtonSetUp(self, widget, controller):
        for i in range(0, 2):
            for j in range(0, 2):
                self.settingsButtons.append(self.RecordButtonSetUp(controller.getSettingsButtonsId(i, j), 80, 
                                                                   u"QPushButton{background-color: #BEBEBE;border-radius: 10px;"
                                                                   "border: 5px solid #A9A9A9;}QPushButton:hover{background-color: #D3D3D3;}"
                                                                   "QPushButton:pressed{background-color: #A9A9A9;}"))
                self.settingsButtons[j+(2*i)].clicked.connect(lambda ch, id = self.settingsButtons[j+(2*i)].objectName(): self.open_setting(id, controller))
                SvgIcon(self.settingsButtons[j+(2*i)], controller.getSettingsButtonsIcon(j+(2*i)), 70, 70, 5, 5, "background-color: transparent;")
                self.settingsButtonGridLayout.addWidget(self.settingsButtons[j+(2*i)], i, j, 1, 1)


    def RecordButtonSetUp(self, name, size, style):
        button = QPushButton()
        button.setObjectName(name)
        button.setMinimumSize(QSize(size, size))
        button.setMaximumSize(QSize(size, size))
        button.setStyleSheet(style)
        # SvgIcon(button, path, size - 10, size - 10, 5, 5, u"background-color: transparent;")

        return button
    
    def start_stop_timer(self, controller):
        if controller.is_recording:
            self.timer.stop()
            self.recordIcon.load('resources\\mic_40dp_FFFFFF_FILL0_wght400_GRAD0_opsz40.svg')
            controller.stop_recording()
            # self.waveFormWidget.load_waveform('output.wav')
        else:
            self.timer.start(100)
            self.recordIcon.load('resources\\stop_circle_40dp_FFFFFF_FILL0_wght400_GRAD0_opsz40.svg')
            controller.start_recording()
    
    def reset_recording(self, controller):
        if not controller.is_recording:
            self.timer.stop()
            self.time_elapsed = 0
            self.timerLabel.setText("00:00:00")
            self.recordIcon.load('resources\\mic_40dp_FFFFFF_FILL0_wght400_GRAD0_opsz40.svg')

            controller.reset_recording()
            self.waveFormWidget.clear_waveform()

    def start_stop_playing(self, controller):
        if not controller.is_recording:
            if controller.is_playing:
                controller.stop_playback()
            else:
                controller.play_sound()

    def update_time(self):
        self.time_elapsed += 100
        minutes = (self.time_elapsed // 60000) % 60
        seconds = (self.time_elapsed // 1000) % 60
        milliseconds  = (self.time_elapsed % 1000)
        self.timerLabel.setText(f"{minutes:02}:{seconds:02}:{milliseconds:02}")
    
    def open_setting(self, buttonId, controller):
        while self.settingBodyLayout.count():
            item = self.settingBodyLayout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        body = QFrame(self.settingBodyQWidget)
        body.setStyleSheet(u"background-color: #E3EAF5;\n""border-radius: 10px;\n border: 4px solid #B0B8C5;")
        self.settingBodyLayout.addWidget(body)

        self.setup_setting_content(buttonId, body, controller)
    
    def setup_setting_content(self, id, parent, controller):
        if id == 'save':
            self.settingView = Save(parent, controller)
        elif id == 'settings':
            self.settingView = Settings(parent, controller)
        elif id == 'equalizer':
            self.settingView = Equalizer(parent, controller)

class WaveformWidget(QWidget):
    def __init__(self, parent, w, h):
        super().__init__(parent)

        self.audio_data = np.array([])
        self.setGeometry(5, 5, w-10, h-10)

    def update_waveform(self, new_data):
        self.audio_data = np.concatenate((self.audio_data, new_data))
        self.update()
    
    def clear_waveform(self):
        self.audio_data = np.array([])
        self.update()
    
    def paintEvent(self, event):
        if self.audio_data.size == 0:
            return
        
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(30, 30, 30))

        pen = QPen(QColor(0, 255, 0))
        pen.setWidth(2)
        painter.setPen(pen)

        midY = self.height()/2
        maxAmplitude = np.max(np.abs(self.audio_data)) or 1
        verticalScale = self.height() / (maxAmplitude * 2)

        step = max(1, len(self.audio_data) // self.width())
        scaledAudioData = self.audio_data[::step]

        waveformPoints = [
            (i * self.width() / len (scaledAudioData), midY - sample * verticalScale)
            for i, sample in enumerate(scaledAudioData)
        ]

        for i in range(1, len(waveformPoints)):
            painter.drawLine(
                waveformPoints[i - 1][0], waveformPoints[i - 1][1],
                waveformPoints[i][0], waveformPoints[i][1]
            )