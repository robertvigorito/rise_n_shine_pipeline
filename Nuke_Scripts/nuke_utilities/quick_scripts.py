import nuke
import math

m = nuke.menu('Nuke').addMenu('Rise n Shine')
m.addCommand('-', '-')
m.addCommand('Reload Read Nodes', 'import Nuke_Scripts.nuke_utilities; quick_scripts.reload_read_nodes()')
m.addCommand('Smart Frame Hold', 'import Nuke_Scripts.nuke_utilities; quick_scripts.frame_hold()', 'shift+f')
m.addCommand('Create V-Ray Camera', 'import Nuke_Scripts.nuke_utilities; quick_scripts.createExrCamVray()')


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