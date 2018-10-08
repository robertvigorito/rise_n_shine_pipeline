import nuke
import logging
from getpass import getuser
import os

try:
    m = nuke.menu('Nuke').addMenu('Rise n Shine')
    m.addCommand('Add Google Drive Location', 'PipelineSetup()')
except AttributeError:
    logging.warning('Running outside of nuke!')


class PipelineSetup(object):
    def __init__(self):
        self.pipeline_paths_list = ['Pipeline/Nuke_Scripts/', 'Pipeline/', 'Pipeline/Gizmo', 'Pipeline/site_packages']
        self.nuke_init_file = 'C:/Users/{}/.nuke/init.py'.format(getuser())

        self.driver_location = nuke.getFilename('')
        self.pipeline_paths_list = [os.path.join(self.driver_location, path).replace('\\', '/')
                                    for path in self.pipeline_paths_list]

        if self.driver_location.endswith('VFX Project/'):
            self.append_nuke_path()
            self.load_and_write_paths()
        else:
            nuke.message('Invalid drive path, please selected the "VFX Project"... ')

    def append_nuke_path(self):
        for path in self.pipeline_paths_list:
            nuke.pluginAppendPath(path)

    def load_and_write_paths(self):
        import Nuke_Scripts.base_functions as bf
        execfile(os.path.join(self.driver_location, self.pipeline_paths_list[0], 'menu.py'))  # Load pipe menu
        execfile(os.path.join(self.driver_location, self.pipeline_paths_list[2], 'menu.py'))  # Load pipe Gizmos

        bf.read_write_nuke_init(self.nuke_init_file, self.pipeline_paths_list)
        bf.json_read_write(self.driver_location)