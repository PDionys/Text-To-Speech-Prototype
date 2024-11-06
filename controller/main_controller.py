from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog, QMessageBox
import os, json, threading
import pyaudio
import wave
import numpy as np
from pydub import AudioSegment

class MainController(QObject):
    audio_data_signal = Signal(np.ndarray)

    def __init__(self, model):
        super().__init__()
        self.is_recording = False
        self.is_playing = False
        self.audio_thread = None
        self.frames = []

        self._model = model

    def ChangeHeaderIcon(self, text, icon):
        self._model.darkIcon = icon
        self._model.headerText = text
    
    def ChangeProjectPath(self, buttonId):
        folder = QFileDialog.getExistingDirectory()
        if buttonId == "newProjectButton":
            self._model.projectManagerModelNewPath(folder, 1)
        elif buttonId == "loadProjectButton":
            self._model.projectManagerModelNewPath(folder, 0)

    
    #TODO make message box
    def CreateNewProject(self, projectName, projectPath):
        newProject = os.path.join(projectPath.text(), projectName.text())
        try:
            if os.path.exists(projectPath.text()) and os.path.isdir(projectPath.text()):
                os.makedirs(newProject)
            else:
                os.makedirs(projectPath.text())
                os.makedirs(newProject)

            self.AddNewDataToProjectList(projectName.text(), projectPath.text())
        except Exception as e:
            self.write_message(f"Failed to create folder: {str(e)}", "Error")

    def DeleteExistProjectFromJSON(self, projectName, projectPath):
        with open('exist_projects.json', 'r') as f:
            data = json.load(f)
        data.pop(projectName)
        with open('exist_projects.json', 'w') as f:
            json.dump(data, f, indent=4)

    def AddNewDataToProjectList(self, projectName, projectPath):
        newProjectData = {
                projectName : projectPath
            }

        with open('exist_projects.json', 'r+') as f:
            data_to_append = json.load(f)
            data_to_append.update(newProjectData)
            f.seek(0)
            json.dump(data_to_append, f, indent=4)
            f.truncate()
    
    def start_recording(self):
        self.is_recording = True
        # self.frames = []
        self.audio_thread = threading.Thread(target=self.record_audio)
        self.audio_thread.start()
    
    def stop_recording(self):
        self.is_recording = False
        if self.audio_thread:
            self.audio_thread.join()

    def reset_recording(self):
        # self.save_audio()
        self.frames = []
    
    
    def record_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=self._model._recordingModel.rate, input=True, input_device_index=self._model._recordingModel.microphone
                        , frames_per_buffer=1024)

        print("Recording...")
        while self.is_recording:
            data = stream.read(1024)
            self.frames.append(data)
            audio_chunk = np.frombuffer(data, dtype=np.int16)
            self.audio_data_signal.emit(audio_chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()
        
        print("Recording stopped.")

    def play_sound(self):
        if self.is_playing:
            return  

        self.is_playing = True
        self.audio_thread = threading.Thread(target=self.play_audio)
        self.audio_thread.start()

    def stop_playback(self):
        self.is_playing = False

    def play_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, 
                        output_device_index=self._model._recordingModel.outputDevice)

        print("Playing audio...")
        for frame in self.frames:
            if not self.is_playing:
                break
            stream.write(frame) 

        stream.stop_stream()
        stream.close()
        p.terminate()
        self.is_playing = False
        print("Audio playback finished.")
    
    def save_audio(self, combo_box, file_name):
        name = ''
        if self.frames != []:
            name += file_name.text() + '.wav'
            if combo_box.currentIndex() == 0:
                with wave.open(name, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
                    wf.setframerate(44100)
                    wf.writeframes(b''.join(self.frames))
            self.write_message('Файл учпішно створено!', 'Info')
    
    def resample_audio(self, speed_factor=1.0):
        speed_factor = (200 - speed_factor)/100
        self._model._recordingModel.rate = int(44100*speed_factor)
    def change_volum(self):
        with wave.open('fast.wav', 'rb') as wf:
            # Get parameters from the file (sample width, channels, rate, etc.)
            self._model._recordingModel.rate = wf.getframerate()  # Sample rate
            self._model._recordingModel.microphone = wf.getnchannels()  # Number of channels (1 for mono)
            sample_width = wf.getsampwidth()  # Sample width (e.g., 2 bytes for 16-bit)
            
            # Initialize the frames list
            self.frames = []
            
            # Read the audio data in chunks and store it in frames
            chunk_size = 1024  # Define how much data to read at a time (this is the same as frames_per_buffer)
            while True:
                data = wf.readframes(chunk_size)
                if not data:
                    break  # No more data to read
                self.frames.append(data)
                
                # Optionally, convert the frame data to a numpy array for processing
                audio_chunk = np.frombuffer(data, dtype=np.int16)  # Assuming 16-bit PCM data
                self.audio_data_signal.emit(audio_chunk)  # Emit or process the audio data
                
        # print(f"Audio loaded from {filename} with {len(self.frames)} frames.")
        
    
    def getSettingsButtonsId(self, i, j):
        return self._model._recordingModel.settingsButtonsID[i][j]
    def getSettingsButtonsIcon(self, i):
        return self._model._recordingModel.settingsButtonsIcon[i]
    def setSavingMethods(self):
        return self._model._recordingModel.saveMethods
    def setAviableMicrophone(self):
        microphones = []

        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info.get("maxInputChannels") > 0:
                if i == 0:
                    continue
                else:
                    if device_info.get('name') == 'Primary Sound Capture Driver':
                        break
                    microphones.append(device_info.get('name'))
                    # print(microphones[i-1])
        p.terminate()
        return microphones
    def setAviableOutputDevice(self):
        output_devices = []
        p = pyaudio.PyAudio()

        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)

            if device_info.get("maxOutputChannels") > 0:
                if device_info.get("name") == 'Microsoft Sound Mapper - Output':
                    continue
                elif device_info.get("name") == 'Primary Sound Driver':
                    break
                output_devices.append(device_info.get("name"))

        p.terminate()
        return output_devices
    
    def write_message(self, text, title):
        msBox = QMessageBox()
        msBox.setText(text)
        msBox.setWindowTitle(title)
        msBox.exec()

    def change_microphone(self, combo):
        index = combo.currentIndex()
        self._model._recordingModel.microphone = index+1
    def change_output_device(self, combo):
        index = combo.currentIndex()
        self._model._recordingModel.outputDevice = index+4

    def make_adjustement(self, tempo, volume, pan):
        self.resample_audio(int(tempo.text()))
        self.change_volum()