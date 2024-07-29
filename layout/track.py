import pcbnew
import kicadpy as kp
import math

def add(
    startX_mm,
    srartY_mm,
    endX_mm,
    endY_mm,
    width_mm,
    layer,
    formatCartesian = True):

    if formatCartesian:
        endY_mm *= -1
    track = pcbnew.PCB_TRACK(kp._board)
    track.SetStart(pcbnew.VECTOR2I(int((startX_mm) * 1E6), int((srartY_mm) * 1E6)))
    track.SetEnd(pcbnew.VECTOR2I(int((endX_mm) * 1E6), int((endY_mm) * 1E6)))
    track.SetWidth(int(width_mm * 1e6))
    track.SetLayer(layer)
    kp._board.Add(track)


# TODO add function like "addArc" with thre points as input

def addArc(
        startAngle_DEG,
        endAngle_DEG,
        radius_mm,
        center_mm,
        width_mm,
        layer,
        formatCartesian = True):
    # TODO: solve 180° offset and ccw fault
    start_angle = math.radians(-startAngle_DEG)
    end_angle = math.radians(-endAngle_DEG)

    if start_angle > end_angle and True:
        endAngle_DEG += math.radians(180)

    start = (radius_mm * math.cos(start_angle) + center_mm[0], radius_mm * math.sin(start_angle)+ center_mm[1])
    end = (radius_mm * math.cos(end_angle)+ center_mm[0], radius_mm * math.sin(end_angle)+ center_mm[1])

    #mid_angle = startAngle_DEG + (endAngle_DEG - startAngle_DEG) / 2
    mid_angle = start_angle + (end_angle - start_angle) / 2

    mid = (radius_mm * math.cos(mid_angle) + center_mm[0], radius_mm * math.sin(mid_angle)+ center_mm[1])

    arc = pcbnew.PCB_ARC(kp._board)
    arc.SetStart(pcbnew.VECTOR2I(int((start[0]) * 1E6), int((start[1]) * 1E6)))
    arc.SetMid(pcbnew.VECTOR2I(int((mid[0]) * 1E6), int((mid[1]) * 1E6)))
    arc.SetEnd(pcbnew.VECTOR2I(int((end[0]) * 1E6), int((end[1]) * 1E6)))
    arc.SetLayer(layer)
    arc.SetWidth(int(width_mm * 1e6))
    
    #a = pcbnew.NETINFO_ITEM_ClassOf(arc)
    #a.SetNetname(netName)
    #arc.SetNetname(netName)
    #print(arc.GetNetname())
    #arc.SetNet(netName)
    
    kp._board.Add(arc)
    #pcbnew.Refresh()
    #input("wainting")