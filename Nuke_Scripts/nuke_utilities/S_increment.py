import nuke
'''
Robert Vigorito
Increments Nuke Nodes in a horizontal formation
"Keeping Work Flow Mint!!"
'''

m = nuke.menu('Nuke').addMenu('Rise n Shine')
m.addCommand('Smart Increment Nodes/Right Smart Increment', 'S_increment.smartIncSide(value = False, incValue = 0)', 'ctrl+alt+right')
m.addCommand('Smart Increment Nodes/Left Smart Increment', 'S_increment.smartIncSide(value = True, incValue = 0)', 'ctrl+alt+left')
m.addCommand("Smart Increment Nodes/-", "", "")
m.addCommand('Smart Increment Nodes/Smart Increment Up', 'S_increment.smartRevert(S_increment.incAdd1(-25), S_increment.incAdd1(0))', 'ctrl+alt+up')
m.addCommand('Smart Increment Nodes/Smart Increment Down', 'S_increment.smartInc(S_increment.incAdd1(25))', 'ctrl+alt+down')

def smartIncSide(value = None, incValue = 0):
    ## Listing Selected Nodes
    sel = nuke.selectedNodes()
    if sel:
        ## Creating list Dictionary by xpos
        xpDict = {x.xpos() if not x.Class() == 'Dot' else x.xpos()-34 for x in sel}
        xpDict = {x:[y for y in sel if x == y.xpos() or x == y.xpos()-34] for x in xpDict}

        ## Calculating X increment
        if len(xpDict.keys()) > 1:
            xpList = sorted(xpDict, reverse = value)
            increment = (xpList[1] - xpList[0]) + incValue

        ## Organising miss aligned nodes
        a = 50 ## Average value
        for x in xpList:
            for y in xpList:
                if x != y:
                    if y < (x+a) and y > (x-a):
                        try:
                            xpDict[x] += xpDict[y]
                            xpList.remove(y)
                            if y in ypDict: del ypDict[y]
                        except:
                            pass

            ## Adjusting Nodes to equal distance in x
            for i,x in enumerate(xpList):
                if i != 0:
                    for y in xpDict[x]:
                        minValue = xpList[0] + (increment*i)
                        if y.Class() == 'Dot':
                            minValue += 34
                        y.setXpos(minValue)

## Setting up Globals for increment
x = 0
def incAdd1(i):
    global x
    if i != 0 and x <= 100:
        x += i
    else:
        print 'Global has been reset'
        x*=0
    return x-25

def smartInc(incAdd):
    ## Find the average from the ypos of the selected Nodes
    sel = nuke.selectedNodes()
    if sel:
        ## Creating Dictionary by the average ypos
        ypDict = list(set([(x.ypos()+(x.screenHeight()/2)) for x in sel]))
        ypDict = {x:[y for y in sel if x == (y.screenHeight()/2+y.ypos())] for x in ypDict}

        ## Listing sorted Dictionary and
        ypList = sorted(ypDict)

        ## Organising miss aligned nodes
        a = 25 ## Average value
        for x in ypList:
            for y in ypList:
                if x != y:
                    if y < (x+a) and y > (x-a):
                        try:
                            ypDict[x] += ypDict[y]
                            ypList.remove(y)
                            if y in ypDict: del ypDict[y]
                        except:
                            pass

        ## Finding the increment value
        if len(ypList)>1:
            inc = (ypList[1] - ypList[0]) + incAdd
        else:
            inc = 0

        ## Adjusting Nodes to equal distance in y
        for i,x in enumerate(ypList):
            if i != 0 :
                for y in ypDict[x]:
                    ypos = ypList[0] + (inc*i) - (y.screenHeight()/2)
                    y.setYpos(ypos)

def smartRevert(incAdd, reset):
    if nuke.selectedNodes():
        print incAdd
        nuke.undo()
    else:
        print reset
