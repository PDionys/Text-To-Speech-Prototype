from PySide6.QtCore import QObject, Signal
from model.short_cut_button_model import ShortCutButtonModel
from model.ProjectManagerModel import ProjectManagerModel

class MainWindowModel(QObject):
    icon_changed = Signal(str)
    header_text_change = Signal(str)
    projectManagerModelNewPath_changed = Signal(str)
    projectManagerModelLoadPath_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self._darkIcon = 'resources\\create_new_folder_30dp_3F3F3F_FILL0_wght400_GRAD0_opsz24.svg'
        self._headerText = 'Project Manager'
        self._shortCutButtonsModel = [ShortCutButtonModel('resources\\text_to_speech_30dp_FFFFFF_FILL0_wght400_GRAD0_opsz24.svg', 'Text-to-Speech',
                                                'resources\\text_to_speech_30dp_3F3F3F_FILL0_wght400_GRAD0_opsz24.svg'),
                        ShortCutButtonModel('resources\\model_training_30dp_FFFFFF_FILL0_wght400_GRAD0_opsz24.svg', 'Model Training', 
                                            'resources\\model_training_30dp_3F3F3F_FILL0_wght400_GRAD0_opsz24.svg'),
                        ShortCutButtonModel('resources\\discover_tune_30dp_FFFFFF_FILL0_wght400_GRAD0_opsz24.svg', 'Tuning Output', 
                                            'resources\\discover_tune_30dp_3F3F3F_FILL0_wght400_GRAD0_opsz24.svg'),
                        ShortCutButtonModel('resources\\graphic_eq_30dp_FFFFFF_FILL0_wght400_GRAD0_opsz24.svg', 'Recording Data', 
                                            'resources\\graphic_eq_30dp_3F3F3F_FILL0_wght400_GRAD0_opsz24.svg'), 
                        ShortCutButtonModel('resources\\create_new_folder_30dp_FFFFFF_FILL0_wght400_GRAD0_opsz24.svg', 'Project Manager',
                                            'resources\\create_new_folder_30dp_3F3F3F_FILL0_wght400_GRAD0_opsz24.svg')]
        self._projectManagerModel = ProjectManagerModel()

    @property
    def darkIcon(self):
        return self._darkIcon
    @darkIcon.setter
    def darkIcon(self, iconPath):
        self._darkIcon = iconPath
        self.icon_changed.emit(iconPath)
    
    @property
    def headerText(self):
        return self._headerText
    @headerText.setter
    def headerText(self, text):
        self._headerText = text
        self.header_text_change.emit(text)

    @property
    def projectManagerModelPath(self):
        return self._projectManagerModel.projectPath
    
    def projectManagerModelNewPath(self, path, id):
        self._projectManagerModel.projectPath = path
        if id:
            self.projectManagerModelNewPath_changed.emit(path)
        else:
            self.projectManagerModelLoadPath_changed.emit(path)