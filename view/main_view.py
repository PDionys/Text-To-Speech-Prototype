from view.ui_main_window import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Slot

class MainView(QMainWindow):
    def __init__(self, model, controller):
        super(MainView, self).__init__()

        self._model = model
        self._main_controller = controller

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, self._model.darkIcon, self._model._headerText, self._model._shortCutButtonsModel)

        for b in self.ui._shortCutButton:
            shortCutButtonText = b._buttonLabel.text()
            shortCutButtonDarkIcon = b._darkIcon
            b.clicked.connect(lambda ch, text = shortCutButtonText, icon = shortCutButtonDarkIcon: self._main_controller.ChangeHeaderIcon(text, icon))

        self._model.icon_changed.connect(self.icon_changed)
        self._model.header_text_change.connect(self.header_text_change)

    @Slot(str)
    def icon_changed(self, icon):
        self.ui._headerIcon.load(icon)

    @Slot(str)
    def header_text_change(self, text):
        self.ui._headerLabel.setText(text)
        self.ui._headerLabel.adjustSize()