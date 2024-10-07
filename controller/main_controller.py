from PySide6.QtCore import QObject

class MainController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model

    def ChangeHeaderIcon(self, text, icon):
        self._model.darkIcon = icon
        self._model.headerText = text