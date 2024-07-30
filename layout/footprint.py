import pcbnew
import numpy as np
import kicadpy as kp
import tools.mathUtils as mu

def setToFront(
        referenceDesignator_s,
        front = True):
    #TODO: to be tested
    # Check if referenceDesignator_s is a string, convert to list if true
    if isinstance(referenceDesignator_s, str):
        referenceDesignator_s = [referenceDesignator_s]

    for refDes in referenceDesignator_s:
        footprint = kp._board.FindFootprintByReference(refDes)
        if front:
            footprint.SetLayerAndFlip(pcbnew.F_Cu)
        else:
            footprint.SetLayerAndFlip(pcbnew.B_Cu)
    kp.utils.autoRefresh()

def isInFront(
    referenceDesignator):
    #TODO: to be tested
    footprint = kp._board.FindFootprintByReference(referenceDesignator)
    return not(footprint.IsFlipped())

def setReferencedesignatorSilkVisible(
        referenceDesignator_s,
        visible):
    #TODO: to be tested
    # Check if referenceDesignator_s is a string, convert to list if true
    if isinstance(referenceDesignator_s, str):
        referenceDesignator_s = [referenceDesignator_s]

    for ref in referenceDesignator_s:
        footprint = kp._board.FindFootprintByReference(ref)
        refDes = footprint.Reference() 
        refDes.SetVisible(visible)
    
    kp.utils.autoRefresh()

def setOrientation(
        referenceDesignator_s,
        angle_DEG):
    #TODO: to be tested
    # Check if referenceDesignator_s is a string, convert to list if true
    if isinstance(referenceDesignator_s, str):
        referenceDesignator_s = [referenceDesignator_s]
    
    for refDes in referenceDesignator_s:
        footprint = kp._board.FindFootprintByReference(refDes)
        footprint.SetOrientationDegrees(angle_DEG)
    
    kp.utils.autoRefresh()

def getRotationInDEG(
        referenceDesignator):
    #TODO: to be tested
    footprint = kp._board.FindFootprintByReference(referenceDesignator)
    return footprint.GetOrientation().AsDegrees()

def rotate(
        referenceDesignator_s,
        rel_angle_DEG):
    #TODO: to be tested
    # Check if referenceDesignator_s is a string, convert to list if true
    if isinstance(referenceDesignator_s, str):
        referenceDesignator_s = [referenceDesignator_s]
    
    for refDes in referenceDesignator_s:
        footprint = kp._board.FindFootprintByReference(refDes)
        rel_angle_DEG += footprint.GetOrientation().AsDegrees()
        footprint.SetOrientationDegrees(rel_angle_DEG)
    
    kp.utils.autoRefresh()

def setPosition(
        referenceDesignator,
        x_mm,
        y_mm,
        formatCartesian = True):
    #TODO: to be tested
    footprint = kp._board.FindFootprintByReference(referenceDesignator)
    
    if formatCartesian:
        y_mm *= -1

    footprint.SetPosition(pcbnew.VECTOR2I(int(x_mm*1e6),int(y_mm*1e6)))
    kp.utils.autoRefresh()

def setPositionPolar(
        referenceDesignator,
        center_x_mm,
        center_y_mm,
        angle_DEG,
        radius_mm,
        formatCartesian = True):
    #TODO: to be tested
    x,y = mu.pol2cartDEG(angle_DEG,radius_mm,formatCartesian)
    x += center_x_mm
    y += center_y_mm

    setPosition(referenceDesignator,x,y,formatCartesian)


def move(
        referenceDesignator_s,
        rel_x_mm,
        rel_y_mm,
        rel_rotationAngle_DEG,
        formatCartesian = True):
    #TODO: to be tested
    # Check if referenceDesignator_s is a string, convert to list if true
    if isinstance(referenceDesignator_s, str):
        referenceDesignator_s = [referenceDesignator_s]
    
    for refDes in referenceDesignator_s:
        footprint = kp._board.FindFootprintByReference(refDes)
        orientation_angle = footprint.GetOrientation().AsDegrees() + rel_rotationAngle_DEG
        pos = footprint.GetPosition()
        x = pcbnew.ToMM(pos.x) + rel_x_mm
        y = pcbnew.ToMM(pos.y) + rel_y_mm
        footprint.SetOrientationDegrees(orientation_angle)
        footprint.SetPosition(pcbnew.VECTOR2I(pcbnew.wxPoint(x*1e6,y*1e6)))

def movePolar():
    # TODO implement
    print("movePolar")

def polarPlacePartList(
        boardObject,
        list):
    #TODO: to be tested
    ''' Place all component in a list in polar system

    The list must consist of the following structure.
    [[reference Designator, center x mm, center y mm, radius DEG, angle DEG, part Rotation angel DEG, set to front],
     [...],
     ...]
    
    '''
    
    for part in list:
        polarPlacePart(boardObject,part[0], part[1], part[2], part[3],part[4],-part[5], part[6])


def placeInCircle(
        referenceDesignators,
        center_x_mm,
        center_y_mm,
        radius_mm,
        relativeComponentOrientation_DEG,
        initialPlacementAngle_DEG,
        clockwise,
        formatCartesian = True):
    #TODO: to be tested
    N = len(referenceDesignators)
    angleStep_rad = 2 * np.pi / N
    angleIndex_rad = np.deg2rad(initialPlacementAngle_DEG)

    for component in referenceDesignators:
        # TODO: replace angleIndex_rad with angleIndex_rad + np.pi()
        #x_p = radius * np.sin(angleIndex_rad + 0.5*np.pi) + x_c
        #y_p = radius * -np.cos(angleIndex_rad + 0.5*np.pi) + y_c
        x_p, y_p = mu.pol2cartDEG(np.rad2deg(angleIndex_rad),radius_mm,formatCartesian)

        x_p += center_x_mm
        y_p += center_y_mm
        
        setPosition(
            component,
            x_p,
            y_p,
            formatCartesian)
        
        setOrientation(component,relativeComponentOrientation_DEG+(np.rad2deg(angleIndex_rad)))
        
        if clockwise:
            angleIndex_rad -= angleStep_rad
            continue
        angleIndex_rad += angleStep_rad

def getPadCoordinate(
        referenceDesignator,
        padNumber):
    #TODO: to be tested
    if isinstance(padNumber, int):
        padNumber = str(int)

    footprint = kp._board.FindFootprintByReference(referenceDesignator)
    for pad in footprint.Pads():
        if pad.GetNumber() == padNumber:
            pos = pad.GetPosition()
            x = pcbnew.ToMM(pos.x)
            y = pcbnew.ToMM(pos.y)
            return x, y
    return None

# TODO: cleanup + finish
# make it such that one can also index multible footprints
# for refDes in referenceDesignator_s:
#   for pin in pin_s:
#       ...
def addTrackStubToPin(
    boardObject,
    referenceDesignator,
    pinNumber,
    distanceToPinOrigin_mm,
    trackWidth_mm):
    #TODO: to be tested
    # find out if pin is right, left, abve or below the origin of the part
    footprint = kp._board.FindFootprintByReference(referenceDesignator)
    
    # cache part orientation
    partOrientation = footprint.GetOrientation().AsDegrees()
    
    # undo any rotation for absolute determinaton of pin location
    setOrientation(referenceDesignator,0)
    
    x,y = getPadCoordinate(boardObject,referenceDesignator,pinNumber)
    
    # initialize shape detection alorithm
    x_min = x
    y_min = y
    x_max = x
    y_max = y
    c_x = 0
    c_y = 0
    
    # get box corner coordinates and determine
    # the shape of the footwprint
    for pad in footprint.Pads():
        pos = pad.GetPosition()
        xi = pcbnew.ToMM(pos.x)
        yi = pcbnew.ToMM(pos.y)
        if x_min > xi:
            x_min = xi
            c_x += 1
        elif y_min > yi:
            y_min = yi
            c_y += 1
        elif x_max < xi:
            x_max = xi
            c_x += 1
        elif y_max < yi:
            y_max = yi
            c_y += 1
        elif x_max == xi:
            c_x += 1
        elif x_min == xi:
            c_x += 1
        elif y_max == yi:
            c_y += 1
        elif y_min == yi:
            c_y += 1

    x,y = getPadCoordinate(boardObject,referenceDesignator,pinNumber)
    
    offsetAngle = 0 
    
    # TODO finish the c_x and c_y evaluation
    # for the corner conditions
    if x == x_max and y == y_max:
        print("first quadrant corner")
        if c_x > c_y:
            offsetAngle = 0
        else:
            offsetAngle = -90
    elif x == x_min and y == y_max:
        print("seccond quadrant corner")
        if c_x > c_y:
            print("a")
            offsetAngle = -180
        elif c_x == c_y:
            print("b")
            print(referenceDesignator)
            print(pinNumber)
            offsetAngle = -90
        else:
            print("c")
            offsetAngle = -90
    elif x == x_min and y == y_min:
        print("third quadrant corner")
        if c_x > c_y:
            print("debug1")
            #offsetAngle = -270
            offsetAngle = -180
        elif c_x == c_y:
            print("debug2")
            offsetAngle = -90
        else:
            offsetAngle = -90
    elif x == x_max and y == y_min:
        print("fourth quadrant corner")
    elif x == x_max:
        print("first quadrant")
        offsetAngle = 0
    elif y == y_max:
        print("seccond quadrant")
        if c_x == c_y:
            offsetAngle = 0
        else:
            offsetAngle = -90
    elif x == x_min:
        print("third quadrant")
        offsetAngle = -180 
    elif y == y_min:
        print("fourth quadrant")
        offsetAngle = -270
    
    # rotate back to original orientation
    setOrientation(
        referenceDesignator,
        partOrientation)
    
    x,y = getPadCoordinate(referenceDesignator,pinNumber)
    
    xv, yv = mu.pol2cartDEG(partOrientation + offsetAngle, distanceToPinOrigin_mm)
    xv += x
    yv += y
    if isInFront(referenceDesignator):
        kp.track.add(x,y,xv,yv,trackWidth_mm,pcbnew.F_Cu)
    else:
        kp.track.add(x,y,xv,yv,trackWidth_mm,pcbnew.B_Cu)
    return xv, yv

def addTrackStubAndViaToPin(
        boardObject,
        referenceDesignator,
        pinNumber,
        distanceToPinOrigin_mm,
        viaDrillDiameter_mm,
        viaWidth_mm,
        trackWidth_mm):
    #TODO: to be tested
    xv,yv = addTrackStubToPin(
        boardObject,
        referenceDesignator,
        pinNumber,
        distanceToPinOrigin_mm,
        trackWidth_mm)
    
    print("refDes")
    print(referenceDesignator)
    print("pinNumber")
    print(pinNumber)
    kp.via.add(xv,yv,viaDrillDiameter_mm,viaWidth_mm)
    return xv, yv