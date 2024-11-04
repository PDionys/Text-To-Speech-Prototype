from PySide6.QtWidgets import (QFrame, QWidget, QSplitter, QLabel, QHBoxLayout)
from PySide6.QtCore import (Qt, QSize, QTimer)
from view.TTS_Widgets import *
import threading, pyaudio, wave

class VoiceRecordingView():

    def __init__(self, bodyLayout, widget, controller):
        self.isRecording = False
        self.audio_thread = None

        self.bodyWidget = QWidget()
        self.bodyWidget.setObjectName(u"bodyWidget")

        self.voiceRecordingFrame = Header(self.bodyWidget, u"voiceRecordingFrame", 0, 0, widget.width(), widget.height()/3, 
                                          u"background-color: rgb(250, 249, 246);", 20, 1, 1)
        
        #Заглушка для отображения волны звука
        self.waveLine = QFrame(self.voiceRecordingFrame)
        self.waveLine.setObjectName(u"waveLine")
        self.waveLine.setGeometry(10, 10, widget.width()-10, self.voiceRecordingFrame.height()/2)
        self.waveLine.setStyleSheet(u"background-color: #E3EAF5;")

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

        self.playStopButton = self.RecordButtonSetUp(u"playStopButton", 50, u"QPushButton{background-color: gray; border-radius: 25px;}"
                                                     "QPushButton:hover{background-color: #C0C0C0;}QPushButton:pressed{background-color: #696969;}"
                                                     )
        playStopIcon = SvgIcon(self.playStopButton, 'resources\\restart_alt_40dp_FFFFFF_FILL0_wght400_GRAD0_opsz40.svg', 40, 40, 5, 5, 
                               u"background-color: transparent;")
        self.horizontalLayout.addWidget(self.playStopButton)

        self.recordButton = self.RecordButtonSetUp(u"recordButton", 50, u"QPushButton{background-color: #C80000 ; border-radius: 25px;}"
                                                     "QPushButton:hover{background-color: #FF0000;}QPushButton:pressed{background-color: #900000;}"
                                                     )
        self.recordButton.clicked.connect(lambda: self.start_stop_timer(controller))
        self.recordIcon = SvgIcon(self.recordButton, 'resources\\mic_40dp_FFFFFF_FILL0_wght400_GRAD0_opsz40.svg', 40, 40, 5, 5, 
                               u"background-color: transparent;")
        self.horizontalLayout.addWidget(self.recordButton)

        self.resetRecordingButton = self.RecordButtonSetUp(u"resetRecordingButton", 50, u"QPushButton{background-color: gray; border-radius: 25px;}"
                                                     "QPushButton:hover{background-color: #C0C0C0;}QPushButton:pressed{background-color: #696969;}"
                                                     )
        resetRecordingIcon = SvgIcon(self.resetRecordingButton, 'resources\\play_pause_40dp_FFFFFF_FILL0_wght400_GRAD0_opsz40.svg', 40, 40, 5, 5, 
                               u"background-color: transparent;")
        self.horizontalLayout.addWidget(self.resetRecordingButton)
        self.recordingButtonWidget.setLayout(self.horizontalLayout)

        self.timer = QTimer(self.bodyWidget)
        self.timer.timeout.connect(self.update_time)
        self.time_elapsed = 0
        
        bodyLayout.addWidget(self.bodyWidget)

    def RecordButtonSetUp(self, name, size, style):
        button = QPushButton()
        button.setObjectName(name)
        button.setMinimumSize(QSize(size, size))
        button.setMaximumSize(QSize(size, size))
        button.setStyleSheet(style)
        # SvgIcon(button, path, size - 10, size - 10, 5, 5, u"background-color: transparent;")

        return button
    
    def start_stop_timer(self, controller):
        if self.isRecording:
            self.isRecording = False
            self.timer.stop()
            self.recordIcon.load('resources\\mic_40dp_FFFFFF_FILL0_wght400_GRAD0_opsz40.svg')
            self.audio_thread.join()
        else:
            self.isRecording = True
            self.timer.start(100)
            self.recordIcon.load('resources\\stop_circle_40dp_FFFFFF_FILL0_wght400_GRAD0_opsz40.svg')
            self.audio_thread = threading.Thread(target = self.record_audio)
            self.audio_thread.start()

    def update_time(self):
        self.time_elapsed += 100
        minutes = (self.time_elapsed // 60000) % 60
        seconds = (self.time_elapsed // 1000) % 60
        milliseconds  = (self.time_elapsed % 1000)
        self.timerLabel.setText(f"{minutes:02}:{seconds:02}:{milliseconds:02}")
    
    def record_audio(self, filename="output.wav", rate=44100, chunk=1024):
        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=chunk)
        frames = []
        print('Recording...')

        while self.isRecording:
            data = stream.read(chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

        print('Finished recording.')