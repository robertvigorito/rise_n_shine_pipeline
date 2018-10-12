import os
import nuke
import math
import sys
import Nuke_Scripts.base_functions as bf


n = nuke.menu('Nuke').addMenu('Rise n Shine')
n.addCommand('-', '-')
n.addCommand('Open Node File Path', 'from nuke_quick_scripts.quick_function import *;open_file_directory()', 'shift+e')
n.addCommand('Open Google Drive',
             'from nuke_quick_scripts.quick_function import *; OpenDirectory().open_drive_directory()')
n.addCommand('Open Shot Directory',
             'from nuke_quick_scripts.quick_function import *; OpenDirectory().open_shot_directory()')
n.addCommand('-', '-')
n.addCommand('Reload Read Nodes', 'from nuke_quick_scripts.quick_function import *; reload_read_nodes()')
n.addCommand('Smart Frame Hold', 'from nuke_quick_scripts.quick_function import *; frame_hold()', 'shift+f')
n.addCommand('Create V-Ray Camera', 'from nuke_quick_scripts.quick_function import *; createExrCamVray()')


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


def reload_read_nodes():
    for x in nuke.allNodes('Read'):
        x.setSelected(True)
        x['reload'].execute()


def frame_hold():
    frame = nuke.frame()
    sel = nuke.selectedNodes()

    if sel:
        frame_hold_node = nuke.nodes.FrameHold()
        frame_hold_node.setInput(0,sel[-1])
        frame_hold_node['first_frame'].setValue(float(frame))
        [x.setSelected(False) for x in nuke.selectedNodes()]
        frame_hold_node['selected'].setValue(True)
        [x.setInput(z, frame_hold_node)for x in sel[-1].dependent() for z in range(x.inputs()) if x.input(z) == sel[-1]]
    else:
        frame_hold_node = nuke.createNode('FrameHold', 'first_frame %s' % frame)

    return frame_hold_node


def createExrCamVray():

    ## Assign Selected Node
    node = nuke.selectedNode()
    mDat = node.metadata()
    reqFields = ['exr/camera%s' % i for i in ('FocalLength', 'Aperture', 'Transform')]
    if not set( reqFields ).issubset( mDat ):
        return
    fRange = node.frameRange()
    cam = nuke.createNode( 'Camera2' )
    cam['useMatrix'].setValue( False )
    for k in ( 'focal', 'haperture', 'translate', 'rotate'):
        cam[k].setAnimated()
    for curTask, frame in enumerate( fRange ):
        val = node.metadata( 'exr/cameraAperture', frame) # get horizontal aperture
        fov = node.metadata( 'exr/cameraFov', frame) # get camera FOV
        focal = val / (2 * math.tan(math.radians(fov)/2.0)) # convert the fov and aperture into focal length
        cam['focal'].setValueAt(float(focal),frame)
        cam['haperture'].setValueAt(float(val),frame)
        matrixCamera = node.metadata( 'exr/cameraTransform', frame) # get camera transform data

        #Create a matrix to shove the original data into
        matrixCreated = nuke.math.Matrix4()
        for k,v in enumerate(matrixCamera):
            matrixCreated[k] = v
        matrixCreated.rotateX(math.radians(-90)) # this is needed for VRay.  It's a counter clockwise rotation
        translate = matrixCreated.transform(nuke.math.Vector3(0,0,0))  # Get a vector that represents the camera translation
        rotate = matrixCreated.rotationsZXY() # give us xyz rotations from cam matrix (must be converted to degrees)
        cam['translate'].setValueAt(float(translate.x),frame,0)
        cam['translate'].setValueAt(float(translate.y),frame,1)
        cam['translate'].setValueAt(float(translate.z),frame,2)
        cam['rotate'].setValueAt(float(math.degrees(rotate[0])),frame,0)
        cam['rotate'].setValueAt(float(math.degrees(rotate[1])),frame,1)
        cam['rotate'].setValueAt(float(math.degrees(rotate[2])),frame,2)