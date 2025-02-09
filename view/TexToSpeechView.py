from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QSlider, QProgressBar, QLineEdit, QComboBox
from PySide6.QtGui import QFont, Qt, QMovie
from view.TTS_Widgets import *
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import Qt, QUrl, QTimer
import json

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
        self.modelSettinngWidget.setStyleSheet(u'background-color: transparent;')
        self.modelSettingsFrame = QFrame(self.modelSettinngWidget)
        self.modelSettingsFrame.setGeometry(10, 10, self.modelSettinngWidget.width()/2+150, self.modelSettinngWidget.height()/2+50)
        self.modelSettingsFrame.setStyleSheet(u"background-color: #E3EAF5;\n""border-radius: 10px;\n border: 2px solid #B0B8C5;")
        fileNameLabel = RobotoLabel(self.modelSettingsFrame, 'Введіть назву файлу для збереження результату:', 12, QFont.Bold, 
                    "background-color: transparent; border: 0px;", 10, 10)
        self.fileNameLineEdit = QLineEdit(self.modelSettingsFrame)
        self.fileNameLineEdit.move(10, fileNameLabel.height()+10)
        self.fileNameLineEdit.setStyleSheet(u"background-color: white; color: black;")
        self.fileNameLineEdit.setFont(QFont('Roboto', 12, QFont.Normal))
        modelChoose = RobotoLabel(self.modelSettingsFrame, 'Оберіть модель для трансформації тексту в голос:', 12, QFont.Bold, 
                    "background-color: transparent; border: 0px;", 10, self.fileNameLineEdit.y()+self.fileNameLineEdit.height()+10)
        self.modelComboBox = QComboBox(self.modelSettingsFrame)
        self.modelComboBox.setStyleSheet(u"background-color: white; color: black;")
        self.modelComboBox.setFont(QFont('Roboto', 12, QFont.Normal))
        self.modelComboBox.move(10, modelChoose.y()+modelChoose.height())
        self.modelComboBox.addItems(self.load_models_list())
        speakerLable = RobotoLabel(self.modelSettingsFrame, 'Виберіть приклад голосу, який потрібно відтворити:', 12, QFont.Bold,
                                   "background-color: transparent; border: 0px;", 10, self.modelComboBox.y()+self.modelComboBox.height()+10)
        self.speaker_wav = QLineEdit(self.modelSettingsFrame)
        self.speaker_wav.setGeometry(10, speakerLable.y()+speakerLable.height(), self.modelSettingsFrame.width()/1.5, 25)
        self.speaker_wav.setStyleSheet(u"background-color: white; color: black;")
        self.speaker_wav.setFont(QFont('Roboto', 12, QFont.Normal))
        self.speaker_wavButton = QPushButton(self.modelSettingsFrame)
        self.speaker_wavButton.move(self.speaker_wav.x()+self.speaker_wav.width()+10, self.speaker_wav.y())
        self.speaker_wavButton.setFont(QFont("Roboto", 12, QFont.Bold))
        self.speaker_wavButton.setText("Вказати файл")
        self.speaker_wavButton.setStyleSheet(u"QPushButton{\nbackground-color: #BDCEE8;\n border: 2px solid #97B2DB;\n}\n""QPushButton:hover{\nbackground-color: #E8D7BD;\nborder: 2px solid #DBC097;}\n""QPushButton:pressed{\nbackground-color: #CEA971;\nborder: 2px solid #C1924B;}")
        self.speaker_wavButton.clicked.connect(lambda: self.set_speaker_wav(controller))
        splitLabel = RobotoLabel(self.modelSettingsFrame, 'Розділяти речення під час вимовлення:', 12, QFont.Bold,
                                 "background-color: transparent; border: 0px;", 10, self.speaker_wav.y()+self.speaker_wav.height()+10)
        self.splitComboBox = QComboBox(self.modelSettingsFrame)
        self.splitComboBox.setStyleSheet(u"background-color: white; color: black;")
        self.splitComboBox.setFont(QFont('Roboto', 12, QFont.Normal))
        self.splitComboBox.move(10, splitLabel.y()+splitLabel.height())
        self.splitComboBox.addItems(['Так', 'Ні'])
        

        self.outputPlayerWidget = QWidget(self.modelSettinngWidget)
        self.outputPlayerWidget.setGeometry(self.modelSettinngWidget.width()/2+170, 10, self.modelSettinngWidget.width()/2+100, self.modelSettinngWidget.height()/4)
        self.outputPlayerWidget.setStyleSheet(u'background-color: rgb(30, 30, 30);border: 5px solid #3C3C3C;')
        self.media_player = QMediaPlayer(self.outputPlayerWidget)
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        # self.media_player.setSource(QUrl.fromLocalFile('temp.wav'))
        self.slider = QSlider(Qt.Horizontal, self.outputPlayerWidget)
        self.slider.setRange(0, 0)
        self.slider.setGeometry(5, 5, self.outputPlayerWidget.width()-10, self.outputPlayerWidget.height()/2-10)
        self.slider.setStyleSheet(u'background-color: transparent;border: 0px;')
        self.slider.sliderMoved.connect(self.set_position)
        self.playStopButton = QPushButton(self.outputPlayerWidget)
        self.playStopButton.setGeometry(self.outputPlayerWidget.width()/2-10, self.outputPlayerWidget.height()/2, 50, 50)
        self.playStopButton.setStyleSheet(u"QPushButton{background-color: #9EDF9C ; border-radius: 25px; border: 0px;}"
                                                     "QPushButton:hover{background-color: #C2FFC7;}"
                                                     "QPushButton:pressed{background-color: #62825D;}")
        SvgIcon(self.playStopButton, 'resources\\play_pause_40dp_FFFFFF_FILL0_wght400_GRAD0_opsz40.svg', 50, 50, 0, 0, 
                'background-color: transparent;border: 0px;')
        self.playStopButton.clicked.connect(self.toggle_play)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.progressBar = QProgressBar(self.modelSettinngWidget)
        self.progressBar.setRange(0, 100)
        self.progressBar.setGeometry(self.outputPlayerWidget.x(), self.outputPlayerWidget.y()+self.outputPlayerWidget.height()+10, 
                                     self.outputPlayerWidget.width()+30, 20)
        self.progressBar.setFormat('')
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.update_progress_bar(controller))


        self.saveButton = QPushButton(self.modelSettinngWidget)
        self.saveButton.setStyleSheet(u"QPushButton{\nbackground-color: rgb(26, 58, 111);\nborder-radius: 5px;\ncolor: #FFFFFF;\nborder: 0px;}\nQPushButton:hover{\nbackground-color: rgb(39, 74, 132);\n}\nQPushButton:pressed{\nbackground-color: rgb(20, 42, 82);\n}")
        self.saveButton.setGeometry(self.modelSettinngWidget.width()/2+170, self.progressBar.y()+self.progressBar.height()+10, 60,60)
        self.saveButton.clicked.connect(lambda: self.saveOutPut(controller))
        SvgIcon(self.saveButton, 'resources\\save_70dp_FFFFFF_FILL0_wght400_GRAD0_opsz48.svg', 60, 60, 0, 0, 'background-color: transparent;')
        self.loadingLabel = RobotoLabel(self.modelSettinngWidget, 'Завантаження ', 18, QFont.Bold, 
                                        "background-color: transparent; border: 0px; color: #3F3F3F;", 
                                        self.saveButton.x()+self.saveButton.width()+10, 
                                        self.progressBar.y()+self.progressBar.height()+10)
        self.loadingGif = QLabel(self.modelSettinngWidget)
        self.loadingGif.setGeometry(self.loadingLabel.x()+60, self.progressBar.y()+self.progressBar.height()+10+30,
                                    60,60)
        # self.loadingGif.move(self.saveButton.x()+self.saveButton.width()+10, self.progressBar.y()+self.progressBar.height()+10+20)
        self.move = QMovie('resources\Spinner@1x-1.0s-200px-200px.gif')
        self.loadingGif.setMovie(self.move)
        self.loadingGif.hide()
        self.loadingLabel.hide()
        self.convertButton = QPushButton(self.modelSettinngWidget)
        self.convertButton.setStyleSheet(u"QPushButton{\nbackground-color: rgb(26, 58, 111);\nborder-radius: 5px;\ncolor: #FFFFFF;\nborder: 0px;}\nQPushButton:hover{\nbackground-color: rgb(39, 74, 132);\n}\nQPushButton:pressed{\nbackground-color: rgb(20, 42, 82);\n}")
        self.convertButton.setGeometry(self.modelSettinngWidget.width()/2+170+self.modelSettinngWidget.width()/2-50, 
                                       self.progressBar.y()+self.progressBar.height()+10, 150, 60)
        self.convertButton.setText('Перетворити')
        self.convertButton.setFont(QFont('Roboto', 18, QFont.Normal))
        self.convertButton.clicked.connect(lambda ch, line = self.textInputEdit, model = self.modelComboBox, save = self.fileNameLineEdit,
                                           split = self.splitComboBox, speaker = self.speaker_wav:
                                           controller.start_to_covert(line, model, save, split, speaker))
        self.ttsVLayout.addWidget(self.modelSettinngWidget)

        bodyLayout.addWidget(self.bodyWidget)
        controller.tts_signal.connect(self.start_progress)
        controller.start_tts_signal.connect(self.start_loading)
    
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
    
    def toggle_play(self):
        if self.media_player.playbackState() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()
    
    def set_position(self, position):
        self.media_player.setPosition(position)
    
    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
    
    def start_progress(self, execution_time):
        self.loadingGif.hide()
        self.move.stop()
        self.loadingLabel.hide()
        self.execution_time = int(execution_time/3)
        self.count_timer = 0
        self.progressBar.setValue(0)
        self.timer.start(1000)
    
    def update_progress_bar(self, controller):
        self.count_timer += 1
        progress = self.count_timer/self.execution_time
        current_progres = self.progressBar.value()
        if current_progres < 100:
            self.progressBar.setValue(int(progress*100))
        else:
            self.media_player.setSource(QUrl.fromLocalFile('temp.wav'))
            controller.load_frames()
            self.timer.stop()
    
    def start_loading(self, trigger):
        self.loadingGif.show()
        self.move.start()
        self.loadingLabel.show()

    def load_models_list(self):
        with open('tts_models.json', 'r') as f:
            data = json.load(f)
        
        keys_list = list(data.keys())
        return keys_list
    
    def saveOutPut(self, controller):
        controller.save(self.fileNameLineEdit.text()+'.wav')

    def set_speaker_wav(self, controller):
        controller.get_voice_sample()
        # print(controller.speaker_wav)
        self.speaker_wav.setText(controller.speaker_wav)