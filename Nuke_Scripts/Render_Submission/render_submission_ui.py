from Nuke_Scripts.Nuke_Functions import *
from PySide.QtCore import *
from getpass import getuser
from source_access import *
from PySide.QtGui import *
import os
import  sys

try:
    m = nuke.menu('Nuke').addMenu('Rise n Shine')
    m.addCommand("-", "", "")
    m.addCommand('Submit Render Version', 'from Render_Submission.render_submission_ui import *; run_app()', 'f2')
    m.addCommand("-", "", "")
except AttributeError:
    pass


class RenderSubmission(QDialog):
    def __init__(self):
        super(RenderSubmission, self).__init__(parent=QApplication.activeWindow())

        # Set ui size and window title
        self.setWindowTitle('Render Submission Tool Beta')
        self.setMinimumSize(350, 500)

        # Initiate google sheets
        self.google_sheets = GoogleSheet()

        # Create labels and user input
        label_1 = QLabel('Artist:')
        self.username = QLineEdit(getuser())

        # Create labels and add shot code
        label_2 = QLabel('Shot Code:')
        self.shot_code = QLineEdit('001_002')
        self.shot_code.textEdited.connect(self.set_combo_box)

        # If nuke is imported find shot code
        try:
            self.shot_code.setText(nuke.root()['name'].getValue().split('/')[-3])
        except AttributeError:
            pass
        except IndexError:
            pass
        # Assigning user google sync path
        self.google_drive = Drive_Dir().Read(getuser())
        self.review_directory = self.google_drive + 'Comp/{}/Renders/Review/'.format(self.shot_code.text())

        # Create label and pull down box for task job
        label_3 = QLabel('Job Task:')
        self.task = QComboBox()
        task_list = [folder_dir for folder_dir in os.listdir(self.review_directory)if os.path.isdir(self.review_directory + folder_dir)]
        self.task.addItems(task_list)
        self.task.activated.connect(self.set_combo_box)

        # Note content widget
        label_4 = QLabel('Submission Version:')
        self.review_version = QComboBox()
        self.note_content = QTextEdit()
        self.set_combo_box()

        # Push button submission and css style
        submission = QPushButton('Submit Review')
        submission.connect(SIGNAL('pressed()'), self.submit_notes)
        submission.setStyleSheet('*{height: 30px; border-radius: 10px; border: 1px solid}'
                                 ':hover {background-color: blue;}'
                                 ':pressed {background-color: white}')

        # Create grid layout and add listed widgets
        self.layout_1 = QGridLayout()
        # Add labels to the grid layout
        self.layout_1.addWidget(label_1, 0, 0, Qt.AlignRight)
        self.layout_1.addWidget(label_2, 1, 0, Qt.AlignRight)
        self.layout_1.addWidget(label_3, 2, 0, Qt.AlignRight)
        self.layout_1.addWidget(label_4, 3, 0)
        # Adding line edit to the layout
        self.layout_1.addWidget(self.username, 0, 1)
        self.layout_1.addWidget(self.shot_code, 1, 1)
        # Adding pull down bar to the layout
        self.layout_1.addWidget(self.task, 2, 1)
        self.layout_1.addWidget(self.review_version, 3, 1)
        # Adding text content box to layout
        self.layout_1.addWidget(self.note_content, 4, 0, 1, 0)
        # Adding submission button
        self.layout_1.addWidget(submission, 5, 0, 1, 0)

        # Assign master layout to self
        self.master_layout()

    def master_layout(self):
        master = QVBoxLayout()
        master.addLayout(self.layout_1)
        self.setLayout(master)

    def set_combo_box(self):
        try:
            self.review_version.clear()
            # Set review directory based of saved google drive location
            review_directory = '{}/{}'.format(self.review_directory, self.task.currentText())
            # Create a list of version files
            version_list = sorted([version for version in os.listdir(review_directory) if version.endswith('mov')])
            self.review_version.addItems(version_list)
            self.review_version.setCurrentIndex(len(version_list)-1)
        except WindowsError:
            pass

    def submit_notes(self):
        # Assign user input
        artist = self.username.text()
        content = self.note_content.toPlainText()
        shot_code = self.shot_code.text()
        review_version = self.review_version.currentText()
        # Send email review and set tracker status
        send_review(artist, shot_code, content, review_version)
        self.google_sheets.set_tracker_status(shot_code)
        self.close()


def run_app():

    for app in qApp.allWidgets():
        if type(app).__name__ == 'RenderSubmission':
            app.close()
    render_submission = RenderSubmission()
    render_submission.show()

    # app = QApplication(sys.argv)
    # render_submission = RenderSubmission()
    # render_submission.show()
    # sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()



