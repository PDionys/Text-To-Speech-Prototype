from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog, QMessageBox
import os, json, threading
import pyaudio
import wave
import numpy as np
from scipy.signal import convolve
from pydub import AudioSegment
from scipy.io import wavfile

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
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, input_device_index=self._model._recordingModel.microphone
                        , frames_per_buffer=1024)

        # print("Recording...")
        while self.is_recording:
            data = stream.read(1024)
            self.frames.append(data)
            audio_chunk = np.frombuffer(data, dtype=np.int16)
            self.audio_data_signal.emit(audio_chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # print("Recording stopped.")

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
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=self._model._recordingModel.rate, output=True, 
                        output_device_index=self._model._recordingModel.outputDevice)

        # print("Playing audio...")
        for frame in self.frames:
            if not self.is_playing:
                break
            stream.write(frame) 

        stream.stop_stream()
        stream.close()
        p.terminate()
        self.is_playing = False
        # print("Audio playback finished.")
    
    def save_audio(self, combo_box, file_name):
        name = ''
        if self.frames != []:
            name += file_name.text() + '.wav'
            if combo_box.currentIndex() == 0:
                self.save(name)
            self.write_message('Файл учпішно створено!', 'Info')
    def save(self, name):
        with wave.open(name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(self._model._recordingModel.rate)
            wf.writeframes(b''.join(self.frames))
    
    def resample_audio(self, speed_factor=1.0):
        # speed_factor = (200 - speed_factor)/100
        speed_factor = speed_factor/100
        self._model._recordingModel.rate = int(44100*speed_factor)
    def change_volum(self, volume):
        if self.frames != []:
            self.save('temp.wav')
            sound = AudioSegment.from_file("temp.wav")
            louder_song = sound + volume
            louder_song.export("temp.wav", format='wav')
            self.load_frames()

    def pitch_shift(self, parameters):
        for i in range(0, len(parameters)):
            parameter = parameters[i].objectName()
            if parameter == 'pitch-amount':
                semitones = parameters[i].value()
            elif parameter == 'fine-tuning':
                cents = parameters[i].value()
        if self.frames != []:
            self.save('temp.wav')
            sound = AudioSegment.from_file('temp.wav', format='wav')
            total_shift = semitones + (cents / 100)
            new_sample_rate = int(sound.frame_rate * (2.0 ** (total_shift / 12)))
            pitch_shifted_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
            pitch_shifted_sound = pitch_shifted_sound.set_frame_rate(44100)
            pitch_shifted_sound.export("temp.wav", format="wav")
            self.load_frames()
    
    def add_reverb(self, parameters):
        for i in range(0, len(parameters)):
            parameter = parameters[i].objectName()
            if parameter == 'reverb-intensity':
                reverb_intensity = parameters[i].value() / 100
            elif parameter == 'reverb-decay':
                decay = parameters[i].value() / 100
        if self.frames != []:
            self.save('temp.wav')
            audio = AudioSegment.from_file('temp.wav')
            samples = np.array(audio.get_array_of_samples())
            impulse_response = np.zeros(int(len(samples) * reverb_intensity))
            impulse_response[0] = 1
            impulse_response[int(len(impulse_response) / 2)] = decay
            reverberated_samples = convolve(samples, impulse_response, mode='full')
            reverb_audio = audio._spawn(reverberated_samples[:len(samples)].astype(np.int16).tobytes())
            reverb_audio.export('temp.wav', format="wav")
            self.load_frames()
    
    def make_robotic_voice(self, parameters):
        for i in range(0, len(parameters)):
            parameter = parameters[i].objectName()
            if parameter == 'pitch-factor':
                pitch_factor = parameters[i].value() / 100
            elif parameter == 'tremolo-frequency':
                tremolo_frequency = parameters[i].value()
            elif parameter == 'tremolo-depth':
                tremolo_depth = parameters[i].value() / 100
        if self.frames != []:
            self.save('temp.wav')
            sample_rate, audio_data = wavfile.read('temp.wav')
            shifted_audio = np.interp(
                np.arange(0, len(audio_data), pitch_factor),
                np.arange(0, len(audio_data)),
                audio_data
            ).astype(audio_data.dtype)
            tremolo = (1 - tremolo_depth) + tremolo_depth * np.sin(2 * np.pi * tremolo_frequency * np.arange(len(shifted_audio)) / sample_rate)
            robotic_audio = (shifted_audio * tremolo).astype(np.int16)
            wavfile.write('temp.wav', sample_rate, robotic_audio)
            self.load_frames()


    def load_frames(self):
        with wave.open('temp.wav', 'rb') as wf:
            self._model._recordingModel.rate = wf.getframerate()
            self._model._recordingModel.microphone = wf.getnchannels()
            sample_width = wf.getsampwidth()
            
            self.frames = []
            
            chunk_size = 1024
            while True:
                data = wf.readframes(chunk_size)
                if not data:
                    break
                self.frames.append(data)
                
                audio_chunk = np.frombuffer(data, dtype=np.int16)
                # self.audio_data_signal.emit(audio_chunk)
        
    
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
        self.change_volum(volume.value())
    
    def apply_effects(self, radio, group, parameters):
        for i in range(0, len(group)):
            if radio[i].isChecked():
                effect = group[i].objectName()
                if effect == 'pitch-box':
                    self.pitch_shift(parameters[i])
                elif effect == 'reverb-box':
                    self.add_reverb(parameters[i])
                elif effect == 'robotic-box':
                    self.make_robotic_voice(parameters[i])
    
    def openTextFile(self):
        # string = ''
        file = QFileDialog.getOpenFileName()
        if file[0].endswith('.txt'):
            with open(file[0], 'r') as f:
                content = f.read()
        
        # split = content.split('\n')
        # for i in range(0, len(split)):
        #     if i == len(split)-1:
        #         string += split[i]
        #     else:
        #         string += split[i] + ' \n'

        return content