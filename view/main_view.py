from view.ui_main_window import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Slot
from view.ProjectManagerView import ProjectManagerView
from view.VoiceRecordingView import VoiceRecordingView
from view.TexToSpeechView import TexToSpeech

class MainView(QMainWindow):
    def __init__(self, model, controller):
        super(MainView, self).__init__()

        self._model = model
        self._main_controller = controller

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, self._model.darkIcon, self._model._headerText, self._model._shortCutButtonsModel)
        self.ui._body.setupUi(self.ui.bodyLayout, self._main_controller, self._model)

        for b in self.ui._shortCutButton:
            shortCutButtonText = b._buttonLabel.text()
            shortCutButtonDarkIcon = b._darkIcon
            b.clicked.connect(lambda ch, text = shortCutButtonText, icon = shortCutButtonDarkIcon: self._main_controller.ChangeHeaderIcon(text, icon))

        self._model.icon_changed.connect(self.icon_changed)
        self._model.header_text_change.connect(self.header_text_change)
        self._model.header_text_change.connect(self.body_delete)
        self._model.header_text_change.connect(self.body_set)

    @Slot(str)
    def icon_changed(self, icon):
        self.ui._headerIcon.load(icon)

    @Slot(str)
    def header_text_change(self, text):
        self.ui._headerLabel.setText(text)
        self.ui._headerLabel.adjustSize() 

    @Slot(str)
    def body_delete(self):
        while self.ui.bodyLayout.count():
            item = self.ui.bodyLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    @Slot(str)
    def body_set(self):
        if self._model.headerText == "Project Manager":
            self.ui._body = ProjectManagerView()
            self.ui._body.setupUi(self.ui.bodyLayout, self._main_controller, self._model)
        elif self._model.headerText == "Recording Data":
            self.ui._body = VoiceRecordingView(self.ui.bodyLayout, self.ui.verticalLayoutWidget, self._main_controller)
        elif self._model.headerText == "Text-to-Speech":
            self.ui._body = TexToSpeech(self.ui.bodyLayout, self._main_controller)