
import sys

# findout hoe to append system files for ezdxf when using this script for kicad
# find out what virtualenv is 
# https://www.youtube.com/watch?v=6Ya8McK-Z3Q
sys.path.append('C:/Users/Edwin/AppData/Roaming/Python/Python38/site-packages/ezdxf')

import ezdxf
import math
import pcbnew

#exec(open('dxfToRoute.py').read())

def get_all_entities_from_dxf(file_path):
    entities = []

    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()

    for entity in msp:
        entities.append(entity)

    return entities

def routeARC(
        startPosition,
        midPosition,
        endPosition,
        width,
        layer,
        net):
    entry = "(arc (start "
    entry += str(startPosition[0])
    entry += " "
    entry += str(startPosition[1])
    entry += ") (mid "
    entry += str(midPosition[0])
    entry += " "
    entry += str(midPosition[1])
    entry += ") (end "
    entry += str(endPosition[0])
    entry += " "
    entry += str(endPosition[1])
    entry += ") (width "
    entry += str(width)
    entry += ") (layer \""
    entry += layer
    #entry += "\") (net "
    #entry += net
    entry += "\") (net 0"
    entry += ") (tstamp ))"
    return entry

def calculate_arc_points(arc):
    center = arc.dxf.center
    radius = arc.dxf.radius
    start_angle = math.radians(arc.dxf.start_angle)
    end_angle = math.radians(arc.dxf.end_angle)

    start_point = (
        center.x + radius * math.cos(start_angle),
        center.y + radius * math.sin(start_angle)
    )

    end_point = (
        center.x + radius * math.cos(end_angle),
        center.y + radius * math.sin(end_angle)
    )

    mid_angle = (start_angle + end_angle) / 2
    mid_point = (
        center.x + radius * math.cos(mid_angle),
        center.y + radius * math.sin(mid_angle)
    )

    return start_point, mid_point, end_point

def addTrackArc(
        boardObject,
        startPoint_mm,
        midPoint_mm,
        endPoint_mm,
        width_mm,
        layer):
    arc = pcbnew.PCB_ARC(board)
    arc.SetStart(pcbnew.VECTOR2I(int(startPoint_mm[0] * 1E6), int(startPoint_mm[1] * 1E6)))
    arc.SetMid(pcbnew.VECTOR2I(int(midPoint_mm[0] * 1E6), int(midPoint_mm[1] * 1E6)))
    arc.SetEnd(pcbnew.VECTOR2I(int(endPoint_mm[0] * 1E6), int(endPoint_mm[1] * 1E6)))
    arc.SetLayer(layer)
    arc.SetWidth(int(width_mm * 1e6))
    boardObject.Add(arc)

if 0:
    if __name__ == "__main__":
        dxf_file_path = "StatorPCBCoil-Sketch006.dxf"
        #all_entities = get_all_entities_from_dxf(dxf_file_path)
        doc = ezdxf.readfile(dxf_file_path)
        msp = doc.modelspace()

        for entity in msp.query('ARC'):
            #print(f"Type: {entity.dxftype()}, Handle: {entity.dxf.handle}")
            data = calculate_arc_points(entity)
            #print(data)
            print(routeARC(data[0],data[1], data[2], 0, "F.Cu", "test"))



board = pcbnew.GetBoard()

if __name__ == "__main__":
    dxf_file_path = "StatorPCBCoil-Sketch006.dxf"
    #all_entities = get_all_entities_from_dxf(dxf_file_path)
    doc = ezdxf.readfile(dxf_file_path)
    msp = doc.modelspace()

    for entity in msp.query('ARC'):
        start, mid, end = calculate_arc_points(entity)
        addTrackArc(board,start,mid,end,1,pcbnew.F_Cu)
    
pcbnew.Refresh()
