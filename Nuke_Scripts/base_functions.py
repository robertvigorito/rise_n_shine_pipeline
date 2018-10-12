import os
import json
import nuke
from getpass import getuser


def json_write(file_path, data):
    with open(file_path, 'w') as open_write_file:
        json.dump(data, open_write_file, indent=4)


def json_read(file_path):
    with open(file_path, 'r') as open_read_file:
        data = json.load(open_read_file)
        return data


def json_read_write(value=None):
    json_file_path = os.path.dirname(__file__) + '/rise_n_shine.json'
    data = {getuser(): value}

    if os.path.exists(json_file_path):
        data = json_read(json_file_path)
    if value and data:
        data.update({getuser(): value})

    json_write(json_file_path, data)
    return data[getuser()]


def read_write_nuke_init(nuke_init_file, plugin_path_list):
    try:
        with open(nuke_init_file, 'r') as open_read_file:
            data = open_read_file.read()

        for path in plugin_path_list:
            path = 'nuke.pluginAddPath("{}")'.format(path)
            if not filter(lambda x: path == x, data.splitlines()):
                data += '\n{}'.format(path)

    except IOError:
        data = '\n'.join(['nuke.pluginAddPath("{}")'.format(path) for path in plugin_path_list])

    with open(nuke_init_file, 'w') as open_write_file:
        open_write_file.write(data)


def CreateReadNode(Folder_Path=None, Name=None, Format='.exr'):
    ## Define File Format
    Dir_Files = sorted([x for x in os.listdir(Folder_Path) if x.endswith(Format)])
    if Dir_Files and 'tmp' not in Folder_Path:
        ## Assign Name | Version if True
        if not Name:
            Name = Folder_Path.split('/')[-1]
            Version = len([x.name() for x in nuke.allNodes('Read') if Name in x.name()])
            if Version:
                Name += '_v%s' % Version
        ## Find First || Last Frame
        First_Frame = Dir_Files[0].split('.')[-2]
        Last_Frame = Dir_Files[-1].split('.')[-2]
        ## Assign File Path
        File_Path = Folder_Path + '/' + Dir_Files[0].replace(First_Frame, '%04d')
        ## Create Read Node
        Read_Node = nuke.nodes.Read(name=Name, file=File_Path, first=First_Frame, last=Last_Frame)
        return Read_Node
