import sys
import threading
import pyaudio
import wave
import numpy as np
from PySide6.QtCore import Qt, QObject
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class AudioController(QObject):
    def __init__(self, filename="output.wav", rate=44100, chunk=1024):
        super().__init__()
        self.filename = filename
        self.rate = rate
        self.chunk = chunk
        self.is_recording = False
        self.audio_thread = None
        self.frames = []  # Store recorded frames here

    def start_recording(self):
        self.is_recording = True
        self.frames = []  # Clear any old audio data
        self.audio_thread = threading.Thread(target=self.record_audio)
        self.audio_thread.start()

    def stop_recording(self):
        self.is_recording = False
        if self.audio_thread:
            self.audio_thread.join()
        # Save the recording to a file
        self.save_audio()

    def record_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=self.rate, input=True, frames_per_buffer=self.chunk)

        print("Recording...")
        while self.is_recording:
            data = stream.read(self.chunk)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Recording stopped.")

    def save_audio(self):
        # Write the recorded frames to a WAV file
        with wave.open(self.filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

class WaveformWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.audio_data = np.array([])  # No waveform data initially
        self.setMinimumHeight(100)  # Set widget height

    def load_waveform(self, filename):
        # Load waveform data from a WAV file
        with wave.open(filename, "rb") as wf:
            frames = wf.readframes(wf.getnframes())
            self.audio_data = np.frombuffer(frames, dtype=np.int16)
        self.update()  # Trigger a repaint with the new data

    def paintEvent(self, event):
        if self.audio_data.size == 0:
            return  # No data to draw

        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(30, 30, 30))  # Background color

        pen = QPen(QColor(0, 255, 0))
        pen.setWidth(2)
        painter.setPen(pen)

        mid_y = self.height() / 2
        max_amplitude = np.max(np.abs(self.audio_data)) or 1  # Prevent division by zero

        # Calculate the vertical scaling factor
        vertical_scale = self.height() / (2 * max_amplitude)

        # Sample points based on the width of the widget
        step = max(1, len(self.audio_data) // self.width())
        scaled_audio_data = self.audio_data[::step]

        # Calculate the points for the waveform with horizontal scaling
        waveform_points = [
            (i * self.width() / len(scaled_audio_data), mid_y - sample * vertical_scale)
            for i, sample in enumerate(scaled_audio_data)
        ]

        # Draw the waveform line
        for i in range(1, len(waveform_points)):
            painter.drawLine(
                waveform_points[i - 1][0], waveform_points[i - 1][1],
                waveform_points[i][0], waveform_points[i][1]
            )

class VoiceRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # Initialize AudioController
        self.audio_controller = AudioController()

    def init_ui(self):
        self.setWindowTitle("Voice Recorder with Final Waveform")
        layout = QVBoxLayout()

        self.record_button = QPushButton("Record")
        self.record_button.clicked.connect(self.toggle_recording)
        layout.addWidget(self.record_button)

        # Waveform display
        self.waveform_widget = WaveformWidget()
        layout.addWidget(self.waveform_widget)

        self.setLayout(layout)

    def toggle_recording(self):
        if not self.audio_controller.is_recording:
            self.audio_controller.start_recording()
            self.record_button.setText("Stop")
        else:
            self.audio_controller.stop_recording()
            self.record_button.setText("Record")
            # Load the recorded audio file into the waveform widget
            self.waveform_widget.load_waveform(self.audio_controller.filename)

app = QApplication(sys.argv)
window = VoiceRecorder()
window.show()
sys.exit(app.exec())
