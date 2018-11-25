"""
Robert Vigorito
Shot Preparation
Setup folder directory and add shot renders
"""

import base_functions as bf
import os
import glob
import re
from pprint import pprint as pp
import shutil


class CreateShot(object):
    pattern = '((?i)[a-z ]+)([0-9]+)'
    show_config = ['Plates',
                   'Renders/Review/Comp',
                   'Renders/Review/Fx',
                   'Scripts',
                   'Source Files']

    def __init__(self, seq, shots, shot_dir_list):
        self.seq, self.shots, self.shot_dir_list = seq, shots, shot_dir_list
        self.shot_code = str()

        self.base_directory = bf.json_read_write()

    def _make_shot_dir(self):
        """
        Make the show config folder structure...
        """
        for directory in self.show_config:
            directory = os.path.join(self.base_directory, 'Comp', self.shot_code, directory).replace('\\', '/')
            bf.make_dir(directory)
        else:
            return True

    def _convert_old_file(self, old_shot_file):
        if old_shot_file.endswith('exr'):
            base_file = os.path.basename(old_shot_file)
            name, frame = re.findall(pattern=self.pattern, string=base_file)[0]
            name = name.lower().replace(' ', '_')
            frame = int(frame) + 1001
            return '{}/{}.{:04d}.exr'.format(name, name, frame)

    def _copy_shot_dir(self, index):
        shot_plate_dir = '{}Comp/{}/Plates'.format(self.base_directory, self.shot_code)
        old_file_list = glob.glob(self.shot_dir_list[index] + '/*')

        for old_shot_file in old_file_list:
            new_base_file = self._convert_old_file(old_shot_file)
            new_shot_file = '{}/{}'.format(shot_plate_dir, new_base_file)
            bf.make_dir(os.path.dirname(new_shot_file))
            if new_base_file and not os.path.exists(new_shot_file):
                shutil.copyfile(src=old_shot_file, dst=new_shot_file)

    def create_shots(self):
        for shot in xrange(shots):
            self.shot_code = '{:03d}_{:03d}'.format(seq, shot + 1)
            self._make_shot_dir()
            self._copy_shot_dir(shot)
        else:
            return True


if __name__ == '__main__':
    seq = 7
    shots = 2
    editor_shots = ["D:\Google Drive\Rise'n'shine\VFX Project\Shots\Remove sticker",
                    "D:\Google Drive\Rise'n'shine\VFX Project\Shots\Moose Winks",
                    ]

    cs = CreateShot(seq, shots, editor_shots)
    cs.create_shots()
