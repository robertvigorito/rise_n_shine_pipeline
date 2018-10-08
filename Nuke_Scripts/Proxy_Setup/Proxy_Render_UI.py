import getpass
import sys
import os
sys.path.append(os.getcwd()[:-11])

from PySide.QtCore import *
from PySide.QtGui import *
from Nuke_Functions import *
from Proxy_Setup.Proxy_Render import *

try:
    if getpass.getuser() == 'Rob':
        m = nuke.menu('Nuke').addMenu('Rise n Shine')
        m.addCommand('Proxy Render', 'from Proxy_Setup.Proxy_Render_UI import *; run_proxy_ui()', 'shift+w')
except AttributeError:
    print 'Module loaded outside of Nuke...'


class ProxyUI(QDialog):
    def __init__(self):
        super(ProxyUI, self).__init__(parent=QApplication.activeWindow())
        self.setWindowTitle('Proxy Render Tool')
        self.setMinimumSize(300, 100)
        self.google_drive = Drive_Dir().Read(getpass.getuser())
        self.setLayout(self.layout1()[0])

    def layout1(self):
        label1 = QLabel('Shot Number:')
        label2 = QLabel('Render Name:')

        self.shot_number = QLineEdit()
        self.shot_name = QLineEdit()

        main_plate = QCheckBox('Main')
        proxy = QCheckBox('Proxy')
        main_plate.setChecked(0)
        proxy.setChecked(1)

        widget = QWidget()
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(main_plate)
        radio_layout.addWidget(proxy)
        widget.setLayout(radio_layout)

        run = QPushButton('Run')
        run.setFixedWidth(210)
        run.pressed.connect(self.run)

        layout = QGridLayout()
        layout.addWidget(widget, 0, 1)
        layout.addWidget(label1, 1, 0)
        layout.addWidget(self.shot_number, 1, 1)
        layout.addWidget(label2, 2, 0)
        layout.addWidget(self.shot_name, 2, 1)
        layout.addWidget(run, 3, 1)
        return layout, main_plate.isChecked(), proxy.isChecked()

    def create_folder_directory(self):
        # Assign shot directory
        google_drive = self.google_drive + 'Comp/{}/'.format(self.shot_number.text())
        # Create shot folder directory
        for folder in ['Plates', 'Scripts', 'Renders/Final', 'Renders/Review/Comp', 'Renders/Review/Fx', 'Source Files']:
            folder_directory = google_drive + folder
            if not os.path.exists(folder_directory):
                os.makedirs(folder_directory)

    def run(self):
        self.create_folder_directory()
        google_drive = self.google_drive + 'Comp/{}/Plates/'.format(self.shot_number.text())
        if os.path.exists(google_drive):
            shot_name = self.shot_name.text()
            if not shot_name:
                shot_name = 'Main Plate'
            proxy_render(google_drive, self.shot_number.text(), shot_name, self.layout1()[1], self.layout1()[2])


def run_proxy_ui():
    for app in qApp.allWidgets():
        if type(app).__name__ == 'Toolset':
            app.close()

    proxy_ui = ProxyUI()
    proxy_ui.show()

try:
    app = QApplication(sys.argv)
    ProxyUI = ProxyUI()
    ProxyUI.show()
    sys.exit(app.exec_())
except RuntimeError:
    print 'Running application within Nuke'