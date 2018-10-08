import json
import os
import nuke
import getpass

class Drive_Dir:
    def __init__(self):
        # Find Json location || Assign username
        self.Json_Path = os.path.dirname(__file__) + '/Rise n Shine.json'
        if os.path.exists(self.Json_Path):
            with open(self.Json_Path, 'r') as Json_Read:
                self.Dictionary = json.load(Json_Read)
        else:
            self.Dictionary = {}

    def Write(self ,Key ,Data = None):
        with open(self.Json_Path, 'w') as self.Json_Write:
            self.Dictionary[Key] = Data
            json.dump(self.Dictionary, self.Json_Write, indent=4)

    def Read(self, Key):
        Value = self.Dictionary[Key]
        return Value

def Create_Init(tool_Dir):
    # Find nuke init path and set plugin path
    init_Path = min([x for x in nuke.pluginPath() if getpass.getuser() in x]) + '/init.py'
    plugin_Path = 'nuke.pluginAddPath("%s")' % tool_Dir
    # Check if file Exist
    if os.path.exists(init_Path):
        with open(init_Path, 'r') as init:
            data = init.read()
            if plugin_Path not in data:
                data += '\n' + plugin_Path
    else:
        data = plugin_Path
    with open(init_Path, 'w') as init:
        init.write(data)

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


def import_mov(mov_file_path):
    # Import by the top right of the script
    xpos = [x.xpos() for x in nuke.allNodes() if x.Class() != 'Viewer']
    ypos = [x.ypos() for x in nuke.allNodes() if x.Class() != 'Viewer']

    if xpos or ypos:
        xpos = sorted(xpos)[-1] + 100
        ypos = sorted(ypos)[0]
    else:
        xpos, ypos = 0, 0

    # Create read Node from user text
    r = nuke.nodes.Read(xpos=xpos, ypos=ypos)
    r['file'].fromUserText(mov_file_path)
    print mov_file_path
    # Create time offset if there is an offset
    first_frame = nuke.root()['first_frame'].getValue()
    if first_frame != 1:
        t = nuke.nodes.TimeOffset(time_offset=first_frame, xpos=xpos, ypos=ypos + 100)
        t.setInput(0, r)
