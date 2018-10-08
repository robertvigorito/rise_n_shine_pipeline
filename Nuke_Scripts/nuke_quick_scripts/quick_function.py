import os
import nuke
import sys
import Nuke_Scripts.base_functions as bf


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
        try:
            self.google_drive_directory = bf.json_read_write()
        except KeyError:
            nuke.message('Can not find Google Drive location path, please try adding location path!')

        # Assign shot code of loaded nuke scene
        try:
            self.shot_code = nuke.root()['name'].getValue().split('/')[-1][:-8]
        except AttributeError:
            self.shot_code = ''
            print 'Function ran outside of nuke'

    def open_drive_directory(self):
        os.startfile(self.google_drive_directory)

    def open_shot_directory(self):
        shot_directory = self.google_drive_directory + 'Comp/' + self.shot_code
        os.startfile(shot_directory)

