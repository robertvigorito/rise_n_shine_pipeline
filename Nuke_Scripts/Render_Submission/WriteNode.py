import os
import nuke
import base_functions as bf

try:
    m = nuke.menu('Nuke').addMenu('Rise n Shine')
    m.addCommand('-', '-', '')
    m.addCommand('Review Render', 'from Render_Submission.WriteNode import *;WriteNode().pro_res_write()', 'alt+f1')
    m.addCommand('Final Render', 'from Render_Submission.WriteNode import *;WriteNode().exr_write()', 'alt+f2')
    m.addCommand('Pre Comp Render', 'from Render_Submission.WriteNode import *;WriteNode().pre_comp_write()', 'alt+f3')
    m.addCommand('-', '-', '')
except AttributeError:
    pass



class WriteNode:
    def __init__(self):
        project_name = nuke.Root()['name'].getValue()
        shot_code = nuke.root().name().rsplit('/')[5]
        google_drive = bf.json_read_write()

        if project_name:
            self.mov_file_path = project_name.replace('Scripts', 'Renders/Review/Comp')[:-3] + '.mov'
            self.exr_file_path = os.path.join(google_drive, 'Final/{}/{}.%04d.exr'.format(shot_code, shot_code))
        else:
            self.mov_file_path, self.exr_file_path = '', ''

    def pro_res_write(self):
        write_node = nuke.createNode('Write', 'name Mov_Render file_type mov codec 3 colorspace srgb')
        write_node['file'].setValue(self.mov_file_path)
        write_node['create_directories'].setValue(1)

        if write_node.inputs():
            write_node.setYpos(write_node.ypos() + 100)

    def exr_write(self):
        write_node = nuke.createNode('Write', 'name Exr_Render file_type exr')
        write_node['file'].setValue(self.exr_file_path)
        write_node['create_directories'].setValue(1)

        if write_node.inputs():
            write_node.setYpos(write_node.ypos() + 100)

    @staticmethod
    def pre_comp_write():
        """
        Create a pre comp write node based off user name input
        :return: Write node
        """
        try:
            # Gather user input name and assign file path
            name = nuke.getInput('Please state the name of the precomp render?')
            name = ''.join(['_' if x is ' ' else x for x in name])

            # Assigning file path and adding in user input naming
            file_name = '/'.join(nuke.root().name().split('/')[:-2]) + '/Renders/Precomp/{}/{}.%04d.exr'.format(name, name)
            pre_comp_node = nuke.createNode('Write', 'name {}_Precomp channels all'.format(name))
            pre_comp_node['create_directories'].setValue(1), pre_comp_node['file'].setValue(file_name)
            return pre_comp_node
        except TypeError:
            print 'No input entered...'

# String testing
if __name__ == '__main__':
    google_drive = "C:/Users/Ben/Google Drive/Rise'n'shine/VFX Project/"
    shot_code = "C:/Users/Ben/Google Drive/Rise'n'shine/VFX Project/Comp/006_000/Scripts/006_000_v007.nk".rsplit('/')[-3]
    print os.path.join(google_drive, 'Final/{}/{}.%04d.exr'.format(shot_code, shot_code))