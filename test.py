# from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
# import sys

# class DynamicWidget(QWidget):
#     def __init__(self):
#         super().__init__()

#         # Main layout for the widget
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)

#         # Button to add new widgets
#         self.add_button = QPushButton("Add New Label")
#         self.add_button.clicked.connect(self.add_label)  # Connect button click to add_label function
#         self.layout.addWidget(self.add_button)

#         # Container layout to hold dynamically added widgets
#         self.dynamic_layout = QVBoxLayout()
#         self.layout.addLayout(self.dynamic_layout)  # Add to main layout

#     def add_label(self):
#         # Create a new label with custom text
#         label = QLabel("New Label")
#         self.dynamic_layout.addWidget(label)  # Add label to the dynamic layout

# # Main part of the application
# app = QApplication(sys.argv)
# window = DynamicWidget()
# window.show()
# app.exec_()

# import pyaudio

# def list_audio_input_devices():
#     p = pyaudio.PyAudio()
#     print("Available audio input devices:")
#     for i in range(p.get_device_count()):
#         device_info = p.get_device_info_by_index(i)
#         # Check if the device is an input device
#         if device_info.get("maxInputChannels") > 0:
#             if device_info.get('name') == 'Primary Sound Capture Driver':
#                 break
#             print(f"Index {i}: {device_info.get('name')}")
#     p.terminate()

# list_audio_input_devices()

import pyaudio

def get_output_devices():
    output_devices = []
    p = pyaudio.PyAudio()

    # Loop through each device and check for output capability
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)

        # Check if the device has output channels
        if device_info.get("maxOutputChannels") > 0:
            # Append device name to output devices list
            output_devices.append(device_info.get("name"))

            # Print device details
            print(f"Index {i}: {device_info.get('name')}")

    p.terminate()
    return output_devices

# Get all output devices
output_devices = get_output_devices()