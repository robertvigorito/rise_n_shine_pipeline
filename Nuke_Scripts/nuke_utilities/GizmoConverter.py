import nuke, time

try:
    from PySide.QtGui import *
except ImportError:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *


m = nuke.menu('Nuke').addMenu('Rise n Shine')
m.addCommand("-", "-")
m.addCommand("Convert Gizmo to Group", "from Nuke_Scripts.nuke_utilities import GizmoConverter; GizmoConverter.runGC()")

def ConvertGroup(x):
    GizmoVal = x.name(), x.xpos(), x.ypos(), x['tile_color'].value()
    ## If there are selected inputs
    inputs = [x.input(inputs).name() for inputs in range(x.inputs())]
    ## Convert to Group
    try:
        Group = x.makeGroup()
        ## Set Outputs
        [y.setInput(i, Group) for y in nuke.allNodes() for i in range(y.inputs()) if y.input(i) == x]
        ## Delete Gizmo
        nuke.delete(x)
        ## Set inputs
        [Group.setInput(i, nuke.toNode(input)) for i, input in enumerate(inputs)]
        ## Transfer Gizmo value to Group Node
        Group['name'].setValue(GizmoVal[0]), Group.setXYpos(GizmoVal[1], GizmoVal[2]), Group['tile_color'].setValue(GizmoVal[3])

        return Group

    except:
        pass

class G_Converter(QDialog):
    def __init__(self):
        super(G_Converter, self).__init__(parent = QApplication.activeWindow())

        self.setWindowTitle('Gizmo Converter')
        self.ProgressionBar()

    def ProgressionBar(self):
        self.progress = QProgressBar()
        self.progress.setFixedSize(500,50)
        lay = QHBoxLayout()
        lay.addWidget(self.progress)
        self.setLayout(lay)

    def setProgress(self, value):
        self.progress.setValue(value)
        if value >= 100:
            time.sleep(.5)
            self.close()

def runGC():
    try:
        value = len([x for x in nuke.allNodes() if x.knob('gizmo_file')])
        inc = 100.00 / value
        g = G_Converter()
        g.show()
        
        i = 1
        for x in nuke.allNodes():
            if x.knob('gizmo_file'):
                prog_Value = round(i * inc)
                ConvertGroup(x)
                g.setProgress(prog_Value)
                i += 1
    except:
        nuke.message('No Gizmos detected in script!!')