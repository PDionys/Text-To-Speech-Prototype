from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
import sys

class DynamicWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout for the widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Button to add new widgets
        self.add_button = QPushButton("Add New Label")
        self.add_button.clicked.connect(self.add_label)  # Connect button click to add_label function
        self.layout.addWidget(self.add_button)

        # Container layout to hold dynamically added widgets
        self.dynamic_layout = QVBoxLayout()
        self.layout.addLayout(self.dynamic_layout)  # Add to main layout

    def add_label(self):
        # Create a new label with custom text
        label = QLabel("New Label")
        self.dynamic_layout.addWidget(label)  # Add label to the dynamic layout

# Main part of the application
app = QApplication(sys.argv)
window = DynamicWidget()
window.show()
app.exec_()