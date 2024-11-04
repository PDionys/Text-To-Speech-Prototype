from PySide6.QtWidgets import (QHBoxLayout, QVBoxLayout, QWidget, QLineEdit, QFrame, QPushButton, QScrollArea, QLabel)
from PySide6.QtGui import QFont
from view.TTS_Widgets import (TTS_Frame, RobotoLabel, SvgIcon)
from PySide6.QtCore import Slot, Qt
import os, json

class ProjectManagerView:
    FRAMES_STYLE = u"background-color: #E3EAF5;\n""border-radius: 10px;\n border: 2px solid #B0B8C5;"
    NEW_PROJECT_STYLE = u"background-color: #F0F0F0;\n border: 3px solid #2E3A59;\n border-radius: 5px;"
    SELECT_FOLDER_BUTTON_STYLE = u"QPushButton{\nbackground-color: #BDCEE8;\n border: 2px solid #97B2DB;\n}\n""QPushButton:hover{\nbackground-color: #E8D7BD;\nborder: 2px solid #DBC097;}\n""QPushButton:pressed{\nbackground-color: #CEA971;\nborder: 2px solid #C1924B;}"
    CREATE_PROJECT_BUTTON_STYLE = u"QPushButton{\nbackground-color: rgb(26, 58, 111);\nborder-radius: 5px;\ncolor: #FFFFFF;\nborder: 0px;}\nQPushButton:hover{\nbackground-color: rgb(39, 74, 132);\n}\nQPushButton:pressed{\nbackground-color: rgb(20, 42, 82);\n}"
    PROJECT_MANAGER_LINE_STYLE = u"background-color: transparent;\n border: 0px"
    LIGHT_FONT_STYLE = "background-color: transparent; color: #FFFFFF;"

    _existProjectsArray = []

    def setupUi(self, layout, controller, model):

        self.verticalLayoutWidget = QWidget()
        self.verticalLayoutWidget.setObjectName(u"projectManagerBody")

        self.projectManagerLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.projectManagerLayout.setSpacing(20)
        self.projectManagerLayout.setObjectName(u"projectManagerLayout")
        self.projectManagerLayout.setContentsMargins(0, 0, 0, 0)

        self.newLoadProject = QHBoxLayout()
        self.newLoadProject.setSpacing(15)
        self.newLoadProject.setObjectName(u"newLoadProject")

        self.newProjectFrame = TTS_Frame(None, u"newProjectFrame", self.FRAMES_STYLE, 30, 0, 10)
        self.newLoadProject.addWidget(self.newProjectFrame)
        self.NewProjectFrameSetUp(controller)

        self.loadProjectFrame = TTS_Frame(None, u"loadProjectFrame", self.FRAMES_STYLE, 30, 0, 10)
        self.newLoadProject.addWidget(self.loadProjectFrame)
        self.LoadProjectFrameSetUp(controller)

        self.projectManagerLayout.addLayout(self.newLoadProject)

        self.projectList = TTS_Frame(None, u"projectList", self.FRAMES_STYLE, 0, 0, 0)
        self.existProjectsScrollArea = QScrollArea(self.projectList)
        self.existProjectsScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.existProjectsScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.existProjectsScrollArea.setWidgetResizable(True)
        self.existProjectsScrollArea.setGeometry(14, 14, 885, 265)
        self.existProjectsScrollArea.setStyleSheet(u"background-color: #BDCEE8;\n border-radius: 0px;\n border: 0px;")
        self.ProjectListFrameSetUp(controller)
        self.projectManagerLayout.addWidget(self.projectList)

        layout.addWidget(self.verticalLayoutWidget)
        model.projectManagerModelNewPath_changed.connect(self.projectManagerModelNewPath_changed)
        model.projectManagerModelLoadPath_changed.connect(self.projectManagerModelLoadPath_changed)

    def NewProjectFrameSetUp(self, controller):
        textTopAnchorn = 17+4+18
        lineAnchorn = 55

        newProjectCreateLabel = RobotoLabel(self.newProjectFrame, "Створення нового проекту:", 18, QFont.Bold, 
                                            u"background-color: transparent;\n border: 0px;\n color: #3F3F3F;", 30, 4)
        newProjectNameFrame = self.CreateProjectManagerFrame(self.newProjectFrame, self.NEW_PROJECT_STYLE, 30, textTopAnchorn, 395, 53)
        newProjectNameLabel = RobotoLabel(newProjectNameFrame, "Назва проекту", 11, QFont.Normal, 
                                          u"background-color: transparent;\n border: 0px", 15, 4)
        newProjectNameLine = self.CreateProjectManagerLine(self.newProjectFrame, 43, lineAnchorn, 360, 35, self.PROJECT_MANAGER_LINE_STYLE, 
                                                           16, QFont.Normal, "Новий Проект")
        #===============================================
        newProjectPathFrame = self.CreateProjectManagerFrame(self.newProjectFrame, self.NEW_PROJECT_STYLE, 30, textTopAnchorn+53+15, 300, 53)
        newProjectPathLabel = RobotoLabel(newProjectPathFrame, "Де зберігати цей проект", 11, QFont.Normal, 
                                          u"background-color: transparent;\n border: 0px", 15, 4)
        chooseFolderButton = self.CreateProjectManagerButton(self.newProjectFrame, "newProjectButton", "Вказати папку", 30+300+5, 
                                                             textTopAnchorn+53+15, 90, 53, 8, QFont.Bold, self.SELECT_FOLDER_BUTTON_STYLE)
        chooseFolderButton.clicked.connect(lambda ch, buttonId = chooseFolderButton.objectName(): controller.ChangeProjectPath(buttonId))
        
        self.newProjectPathLine = self.CreateProjectManagerLine(self.newProjectFrame, 43, lineAnchorn+53+15, 280, 35, 
                                                                self.PROJECT_MANAGER_LINE_STYLE, 16, QFont.Normal, self.ConstructStandartPath())
        #============================================================
        createNewProjectButton = self.CreateProjectManagerButton(self.newProjectFrame, "createNewProjectButton", "Створити проект", 30, 
                                                             textTopAnchorn+(53*2)+15*2, 160, 53, 14, QFont.Normal, 
                                                             self.CREATE_PROJECT_BUTTON_STYLE)
        createNewProjectButton.clicked.connect(lambda ch, projectName = newProjectNameLine, projectPath = self.newProjectPathLine:
                                                controller.CreateNewProject(projectName, projectPath))
        createNewProjectButton.clicked.connect(lambda: self.UpdateProjectsList(controller))

    def LoadProjectFrameSetUp(self, controller):
        textTopAnchorn = 17+4+18
        lineAnchorn = 55

        loadProjectFrameLabel = RobotoLabel(self.loadProjectFrame, "Завантаження проекту:", 18, QFont.Bold, 
                                            u"background-color: transparent;\n border: 0px;\n color: #3F3F3F;", 30, 4)
        loadProjectPathFrame = self.CreateProjectManagerFrame(self.loadProjectFrame, self.NEW_PROJECT_STYLE, 30, textTopAnchorn, 300, 53)
        loadProjectNameLabel = RobotoLabel(loadProjectPathFrame, "Де зберігається проект", 11, QFont.Normal, 
                                          u"background-color: transparent;\n border: 0px", 15, 4)
        chooseFolderButton = self.CreateProjectManagerButton(self.loadProjectFrame, "loadProjectButton", "Вказати папку", 30+300+5, 
                                                             textTopAnchorn, 90, 53, 8, QFont.Bold, self.SELECT_FOLDER_BUTTON_STYLE)
        chooseFolderButton.clicked.connect(lambda ch, buttonId = chooseFolderButton.objectName(): controller.ChangeProjectPath(buttonId))
        self.loadProjectPathLine = self.CreateProjectManagerLine(self.loadProjectFrame, 43, lineAnchorn, 280, 35, self.PROJECT_MANAGER_LINE_STYLE, 16, QFont.Normal, "")

        openProjectButton = self.CreateProjectManagerButton(self.loadProjectFrame, "openProjectButton", "Відкрити проект", 30, 
                                                             textTopAnchorn+53+15, 160, 53, 14, QFont.Normal, 
                                                             self.CREATE_PROJECT_BUTTON_STYLE)
        openProjectButton.clicked.connect(lambda: self.AddNewDataToProjectList(self.loadProjectPathLine, controller))
        #TODO make connect to button

    def ProjectListFrameSetUp(self, controller):
        self.scrollAreaWidget = QWidget()
        vBox = QVBoxLayout()
        vBox.setSpacing(2)
        vBox.setContentsMargins(5, 5, 5, 5)

        with open('exist_projects.json', 'r') as f: 
            data = json.load(f)
        self._existProjectsArray.clear()
        for k,v in data.items():
            temp_widget = ExistProject(self.CREATE_PROJECT_BUTTON_STYLE, k, v, self.LIGHT_FONT_STYLE)
            temp_widget.deleteButton.clicked.connect(lambda ch, projectName = temp_widget.projectName.text(), 
                                                     projectPath = temp_widget.projectPath.text():
                                        self.DeleteExistProjectFromList(projectName, projectPath, controller))
            vBox.addWidget(temp_widget)
            self._existProjectsArray.append(temp_widget)
            
        if len(self._existProjectsArray) < 5:
            for i in range(0, 5-len(self._existProjectsArray)):
                blankFrame = QFrame()
                blankFrame.setMaximumHeight(49)
                blankFrame.setMinimumHeight(49)
                blankFrame.setStyleSheet(u"background-color: transparent;")

                vBox.addWidget(blankFrame)

        self.scrollAreaWidget.setLayout(vBox)

        self.existProjectsScrollArea.setWidget(self.scrollAreaWidget)
        


    def CreateProjectManagerFrame(self, parent, style, x, y, w, h):
        projectFrame = QFrame(parent)
        projectFrame.setStyleSheet(style)
        projectFrame.setGeometry(x, y, w, h)

        return projectFrame
    
    def CreateProjectManagerButton(self, parent, buttonId, text, x, y, w, h, fontSize, fontTypeface, style):
        projectButton = QPushButton(parent)
        projectButton.setObjectName(buttonId)
        projectButton.setGeometry(x, y, w, h)
        projectButton.setFont(QFont("Roboto", fontSize, fontTypeface))
        projectButton.setText(text)
        projectButton.setStyleSheet(style)
        
        return projectButton
    
    def CreateProjectManagerLine(self, parent, x, y, w, h, style, fontSize, fontTypeface, text):
        projectLine = QLineEdit(parent)
        projectLine.setGeometry(x, y, w, h)
        projectLine.setStyleSheet(style)
        projectLine.setFont(QFont("Roboto", fontSize, fontTypeface))
        projectLine.setText(text)

        return projectLine

    def ConstructStandartPath(self):
        username = os.getlogin()
        standartPath = 'C:\\Users\\' + username + '\\Documents\\TTS Projects'
        return standartPath
    
    def DeleteExistProjectFromList(self, projectName, projectPath, controller):
        controller.DeleteExistProjectFromJSON(projectName, projectPath)
        self.UpdateProjectsList(controller)
    def AddNewDataToProjectList(self, path, controller):
        pathSplit = path.text().split('/')
        projectPath = ''
        for i in range(0, len(pathSplit)):
            if i == 0:
                projectPath = pathSplit[i] + '/'
            elif i == len(pathSplit)-2:
                projectPath += pathSplit[i]
            elif i < len(pathSplit)-1:
                projectPath += pathSplit[i] + '/'
            
        controller.AddNewDataToProjectList(pathSplit[len(pathSplit)-1], projectPath)
        self.UpdateProjectsList(controller)

    def UpdateProjectsList(self, controller):
        self.scrollAreaWidget.deleteLater()
        self._existProjectsArray.clear()
        self.ProjectListFrameSetUp(controller)
    
    @Slot(str)
    def projectManagerModelNewPath_changed(self, path):
        self.newProjectPathLine.setText(path)
    @Slot(str)
    def projectManagerModelLoadPath_changed(self, path):
        self.loadProjectPathLine.setText(path)


class ExistProject(QPushButton):
    def __init__(self, buttonStyle, projectNameText, projectPathText, labelStyle):
        super(ExistProject, self).__init__()

        self.setMinimumHeight(49)
        self.setMaximumHeight(49)

        self.setStyleSheet(buttonStyle)
        self.projectName = RobotoLabel(self, projectNameText, 9, QFont.Bold, labelStyle, 5, 5)
        self.projectPath = RobotoLabel(self, projectPathText, 14, QFont.Normal, labelStyle, 5, 5+9+5)

        self.deleteButton = QPushButton(self)
        self.deleteButton.setGeometry(self.width()+175, 5, 39, 39)
        self.deleteButton.setStyleSheet(u'QPushButton{background-color: #b7433e;\n border: 3px solid #a23b37;}\n'
                                        'QPushButton:hover{background-color: #c8615d;}\n QPushButton:pressed{background-color: #85312d;}')
        icon = SvgIcon(self.deleteButton, 'resources\shadow_minus_39dp_FFFFFF_FILL0_wght400_GRAD0_opsz40.svg', 39, 39, 0, 0, 
                       "background-color: transparent;")

        