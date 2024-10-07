import sys
from PySide6.QtWidgets import QApplication
from view.main_view import MainView
from controller.main_controller import MainController
from model.main_model import MainWindowModel

class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        self.mainWindowModel = MainWindowModel()
        self.mainController = MainController(self.mainWindowModel)
        self.mainView = MainView(self.mainWindowModel, self.mainController)
        self.mainView.show()

if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec())