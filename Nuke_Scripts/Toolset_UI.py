import os
import sys
import nuke
from PySide.QtGui import *
from PySide.QtCore import *
import nukescripts
import Nuke_Scripts.base_functions as bf

m = nuke.menu('Nuke').addMenu('Rise n Shine')
m.addCommand("-", "", "")
m.addCommand('Save Toolset', 'import Toolset_UI; Toolset_UI.Run()')
m.addCommand("-", "", "")
nukescripts.toolsets.refreshToolsetsMenu()


class Toolset(QDialog):
    def __init__(self):
        super(Toolset, self).__init__(parent=QApplication.activeWindow())
        self.setWindowTitle('Save Toolset')
        self.setFixedSize(350, 195)
        self.setStyleSheet('QDialog {background : #262c35}')
        self.Toolset_Dir = ''
        self.Toolset_Dir = os.path.join(bf.json_read_write(), 'Pipeline/ToolSets/')
        self.Toolset_List = [x for x in os.listdir(self.Toolset_Dir) if os.path.isdir(self.Toolset_Dir + x)] + [
            'Create Folder']
        self.master()

    def widget1(self):
        Widget = QDialog()
        Widget.setStyleSheet('QDialog{ background: #302f2f; border: 1px double black}')
        Label = QLabel('Toolset Directory: ')
        self.ComboBox = QComboBox()
        self.ComboBox.setFixedSize(125, 20)
        self.ComboBox.addItems(self.Toolset_List)
        self.ComboBox.currentIndexChanged.connect(self.Hidden)
        Label1 = QLabel('Toolset Name: ')
        Label1.setAlignment(Qt.AlignRight)
        self.Text = QLineEdit()

        self.Labe12 = QLabel('Folder Name: ')
        self.Labe12.setAlignment(Qt.AlignRight)
        self.Dir_Text = QLineEdit()
        self.Labe12.setHidden(1)
        self.Dir_Text.setHidden(1)

        Layout = QGridLayout()
        Layout.addWidget(Label, 0, 0)
        Layout.addWidget(self.ComboBox, 0, 1)
        Layout.addWidget(self.Labe12, 1, 0)
        Layout.addWidget(self.Dir_Text, 1, 1)
        Layout.addWidget(Label1, 2, 0)
        Layout.addWidget(self.Text, 2, 1)
        Layout.setContentsMargins(15, 0, 15, 0)

        Widget.setLayout(Layout)
        return Widget

    def Layout1(self):
        Save = QPushButton('Save')
        Cancel = QPushButton('Cancel')
        Save.pressed.connect(self.SaveFunction)
        Cancel.pressed.connect(self.close)

        Layout = QHBoxLayout()
        Layout.setContentsMargins(0, 5, 0, 5)
        Layout.addWidget(Save), Layout.addWidget(Cancel)
        return Layout

    def Hidden(self):
        if self.ComboBox.currentText() == 'Create Folder':
            self.Labe12.setHidden(0), self.Dir_Text.setHidden(0)
        else:
            self.Labe12.setHidden(1), self.Dir_Text.setHidden(1)

    def SaveFunction(self):
        File_Name = self.Text.text()
        if File_Name:
            if self.ComboBox.currentText() == 'Create Folder':
                Folder_Dir = self.Toolset_Dir + self.Dir_Text.text()
                os.makedirs(Folder_Dir)
            else:
                Folder_Dir = self.Toolset_Dir + self.ComboBox.currentText()
            File_Name = Folder_Dir + '/' + File_Name + '.nk'
            if os.path.exists(File_Name):
                if not nuke.ask('Would you like to replace {} Toolset?'.format(self.Text.text())):
                    self.close()

            nuke.nodeCopy(File_Name)
            nukescripts.toolsets.refreshToolsetsMenu()
            self.close()

    def master(self):
        Master = QVBoxLayout()
        Master.addSpacing(5)
        Master.addWidget(self.widget1())
        Master.addSpacing(5)
        Master.addLayout(self.Layout1())
        self.setLayout(Master)


def Run():
    for app in qApp.allWidgets():
        if type(app).__name__ == 'Toolset':
            app.close()

    Tool = Toolset()
    Tool.show()