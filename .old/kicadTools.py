
import pcbnew
import numpy as np

# https://community.element14.com/technologies/open-source-hardware/b/blog/posts/problem-solving-with-kicad-7-and-python-getting-data-and-moving-components-on-circuit-boards

# exec(open('kicadTools.py').read())
'''
def rotate_resistors(board):
    for module in board.GetModules():
        if module.GetValue().startswith("R"):  # Assuming resistor component values start with "R"
            # Rotate the resistor module 90 degrees clockwise
            #module.Rotate(pcbnew.wxPoint(0, 0), 900)  # 900 = 90 degrees CW
'''    

def setRefDesSilkVisibility(board, referenceDesignatorList, visible):
    for ref in referenceDesignatorList:
        footprint = board.FindFootprintByReference(ref)
        refDes = footprint.Reference() 
        refDes.SetVisible(visible)

def rotateComponent(board, referenceDesignator, rotationAngleDEG):
    footprint = board.FindFootprintByReference(referenceDesignator)
    footprint.SetOrientationDegrees(rotationAngleDEG)

def placeComponent(board, referenceDesignator,x,y,rotationAngleDEG):
    footprint = board.FindFootprintByReference(referenceDesignator)
    rotateComponent(board,referenceDesignator,rotationAngleDEG)
    #footprint.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPoint(x,y)))
    footprint.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPoint(x*1e6,y*1e6)))
    #footprint.Rotate(pcbnew.VECTOR2I(x,y),pcbnew.EDA_ANGLE(rotationAngle*10, pcbnew.DEGREES_T))
    
def palceComponentRelativeToPoint(board, referenceDesignator,x,y,x_p,y_p,rotationAngleDEG):
    footprint = board.FindFootprintByReference(referenceDesignator)
    rotateComponent(board,referenceDesignator,rotationAngleDEG)
    #footprint.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPoint(x,y)))
    footprint.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPoint((x+x_p)*1e6,(y+y_p)*1e6)))

def placeComponentsInCircle(
        board,
        referenceDesignators,
        x_c,
        y_c,
        radius,
        relativeComponentOrientationDEG,
        initialPlacementAngleDEG,
        clockwise):
    
    N = len(referenceDesignators)
    angleStep_rad = 2 * np.pi / N
    angleIndex_rad = np.deg2rad(initialPlacementAngleDEG)

    if clockwise:
        angleStep_rad *= -1

    for component in referenceDesignators:
        x_p = radius * np.sin(angleIndex_rad) + x_c
        y_p = radius * np.cos(angleIndex_rad) + y_c
        placeComponent(board, component, x_p, y_p,np.rad2deg(angleIndex_rad)+relativeComponentOrientationDEG)
        angleIndex_rad += angleStep_rad


board = pcbnew.GetBoard()

board.GetFootprints()

footprints = board.GetFootprints()
if 0:
    for fp in footprints:
        fp.Move(pcbnew.VECTOR2I(pcbnew.wxPoint(100e6,100e6)))

if 0:
    for fp in footprints:
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPoint(100e6,100e6)))

#placeComponent(board,"R1",5,5,45)
#placeComponent(board,"R2",5,10,45)
#placeComponent(board,"R3",5,15,45)
#palceComponentRelativeToPoint(board,"R4",5,-5,130,131.3750,45)
componentList = []
for i in range(1, 17):
    componentList.append(f'R{i}')

placeComponentsInCircle(board,componentList,160,160,20,90,0)

pcbnew.Refresh()

#resistor.Rotate(wxPoint(0,0), 90 * 10)
'''
for netname, net in nets.items():
    print("netcode: {}, name: {}".format(net.GetNet(), netname))

for module in board.GetModules():
    print("Module: ", module.GetReference())

'''