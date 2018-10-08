import os
import nuke
import sys
from getpass import *
from Nuke_Functions import *


n = nuke.menu('Nuke').addMenu('Rise n Shine')
n.addCommand('-', '-')
n.addCommand('Open Node File Path', 'from nuke_quick_scripts.quick_function import *;open_file_directory()', 'shift+e')
n.addCommand('Open Google Drive',
             'from nuke_quick_scripts.quick_function import *; OpenDirectory().open_drive_directory()')
n.addCommand('Open Shot Directory',
             'from nuke_quick_scripts.quick_function import *; OpenDirectory().open_shot_directory()')


def open_file_directory():
    """
    Quick script to open the folder location of nuke nodes that have a file knob
    :return: No return value
    """
    try:
        # Find nuke file path and open os window
        sel = nuke.selectedNode()
        if sel['file']:
            folder_directory = '/'.join(sel['file'].getValue().split('/')[:-1])
            os.startfile(folder_directory)
    except NameError:
        nuke.message('Node doesnt have a file path...')
    except ValueError:
        nuke.message('Please select a node with a file path...')
    except WindowsError:
        nuke.message('Folder Directory doesnt exist...')


class OpenDirectory:
    def __init__(self):
        # Retrieve Google Drive location from username
        try:
            self.google_drive_directory = Drive_Dir().Read(getuser())
        except KeyError:
            nuke.message('Can not find Google Drive location path, please try adding location path!')

        # Assign shot code of loaded nuke scene
        try:
            self.shot_code = nuke.root()['name'].getValue().split('/')[-1][:-8]
        except AttributeError:
            self.shot_code = ''
            print 'Function ran outside of nuke'

    # Open Google Drive Directory
    def open_drive_directory(self):
        os.startfile(self.google_drive_directory)

    # Open shot directory within Google Drive directory
    def open_shot_directory(self):
        shot_directory = self.google_drive_directory + 'Comp/' + self.shot_code
        os.startfile(shot_directory)

