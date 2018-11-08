import os
import nuke
import sys
import base_functions as bf
try:
    from PySide.QtGui import *
except ImportError:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *

m = nuke.menu('Nuke').addMenu('Rise n Shine')
m.addCommand('Shot Loader', 'import RNS_Shot_Loader;RNS_Shot_Loader.run() ', 'f1')


def shot_creator(shot_directory, shot_number):
    # Clear current Nuke script
    [nuke.delete(x) for x in nuke.allNodes() if x.Class() != 'Viewer']
    print shot_directory + 'Comp/{}/Plates/'.format(shot_number)
    # Import Plate folders
    for directory, folder, files in os.walk(shot_directory + 'Comp/{}/Plates/'.format(shot_number)):
        if not folder:
            bf.CreateReadNode(directory)
    # Assign shot number and shot directory
    shot_directory += 'Comp/{}/Scripts/{}_v001.nk'.format(shot_number, shot_number)

    # Set default settings - HD
    nuke.Root()['format'].setValue("HD_1080")
    nuke.scriptSaveAs(shot_directory)

    # Set frame range
    last_frame = sorted([x['last'].getValue() for x in nuke.allNodes('Read')])
    if not last_frame:
        last_frame = 1100
    else:
        last_frame = last_frame[-1]

    nuke.Root()['first_frame'].setValue(1001)
    nuke.Root()['last_frame'].setValue(last_frame)
    nuke.Root()['lock_range'].setValue(1)


class ShotLoader(QDialog):
    def __init__(self):
        super(ShotLoader, self).__init__(parent=QApplication.activeWindow())
        self.setWindowTitle('Shot Loader')
        self.setMinimumSize(100, 400)
        # Set variables
        self.shot_dic = {}
        self.google_drive = bf.json_read_write()
        self.scene_location = self.google_drive + 'Comp/'
        # Load master Layer
        self.master()
        # if there is a recent file
        if self.google_drive in nuke.recentFile(1):
            self.shot_number.setText(nuke.recentFile(1).split('/')[-1][:-8])
            self.load_shot(nuke.recentFile(1).split('/')[-1][:-8])

    def layout1(self):
        layout = QHBoxLayout()
        label = QLabel('Shot Number:')
        self.shot_number = QLineEdit()
        self.shot_number.setPlaceholderText('Insert shot number...')
        self.shot_number.textChanged.connect(self.load_shot)
        layout.addWidget(label)
        layout.addWidget(self.shot_number)
        return layout

    def layout2(self):
        layout = QVBoxLayout()
        label = QLabel('sync to {}...'.format(self.google_drive))
        label.setStyleSheet('color : gray ; font-size : 10px')
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        run = QPushButton('Run')
        run.pressed.connect(self.run)
        layout.addWidget(label)
        layout.addWidget(self.list_widget)
        layout.addSpacing(15)
        layout.addWidget(run)
        return layout

    def load_shot(self, x):
        self.scene_path = self.scene_location + x + '/Scripts/'
        self.list_widget.clear()
        if os.path.exists(self.scene_path):
            scene_list = sorted([y for y in os.listdir(self.scene_path) if y.endswith('.nk')])
            if scene_list:
                self.list_widget.addItems(['Create Template'] + scene_list)
            else:
                self.list_widget.addItem('Create Template')
        else:
            self.list_widget.addItem('Path does not exist!!')
            
    def run(self):
        if self.list_widget.selectedItems():
            if self.list_widget.currentItem().text() == 'Create Template':
                shot_creator(self.google_drive, self.shot_number.text())
            else:
                nuke.scriptOpen(self.scene_path + self.list_widget.currentItem().text())
            self.close()
        else:
            message = QMessageBox()
            message.setText('No scene file was selected!')
            message.exec_()
            self.close()
        
    def master(self):
        master = QVBoxLayout()
        master.addLayout(self.layout1())
        master.addLayout(self.layout2())
        master.setContentsMargins(25, 10, 25, 25)
        self.setLayout(master)
     
        
def run():
    for app in qApp.allWidgets():
        if type(app).__name__ == 'ShotLoader':
            app.close()
    shot_loader = ShotLoader()
    shot_loader.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    shot_loader = ShotLoader()
    shot_loader.show()
    sys.exit(app.exec_())
