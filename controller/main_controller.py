from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog, QMessageBox
import os, json
import pyaudio
import wave

class MainController(QObject):
    def __init__(self, model):
        super().__init__()

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
            # QMessageBox.critical(self, "Error", "Error 222", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.NoButton)
            msBox = QMessageBox()
            msBox.setText(f"Failed to create folder: {str(e)}")
            msBox.setWindowTitle("Error")
            msBox.exec()

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

    def record_audio(self, filename="output.wav", rate=44100, chunk=1024, is_recording = False):
        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=chunk)
        frames = []
        print('Recording...')

        while is_recording:
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