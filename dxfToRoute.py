# findout hoe to append system files for ezdxf when using this script for kicad
# find out what virtualenv is 
# https://www.youtube.com/watch?v=6Ya8McK-Z3Q

import ezdxf
import math
import pcbnew

# command to be executed inside the Kicad scripting shell sothat this script will be executed
#exec(open('dxfToRoute.py').read())

def scale_entities(entities, scale_factor):
    scaled_entities = []
    for entity in entities:
        if entity.dxftype() == 'LINE':
            entity.dxf.start = (entity.dxf.start[0] * scale_factor, entity.dxf.start[1] * scale_factor)
            entity.dxf.end = (entity.dxf.end[0] * scale_factor, entity.dxf.end[1] * scale_factor)
        elif entity.dxftype() == 'LWPOLYLINE':
            for vertex in entity.get_points('xy'):
                vertex *= scale_factor
        elif entity.dxftype() == 'ARC':
            entity.dxf.center = (entity.dxf.center[0] * scale_factor, entity.dxf.center[1] * scale_factor)
            entity.dxf.radius *= scale_factor
            entity.dxf.start_angle = entity.dxf.start_angle
            entity.dxf.end_angle = entity.dxf.end_angle
        scaled_entities.append(entity)
    return scaled_entities

def getAllEntitiesFromDXF(file_path):
    entities = []

    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()

    for entity in msp:
        entities.append(entity)

    return entities

def calculateLinePoints(line):
    startPoint = line.dxf.start
    endPoint = line.dxf.end
    return startPoint, endPoint

def calculateArcPoints(arc):
    center = arc.dxf.center
    radius = arc.dxf.radius
    start_angle = math.radians(arc.dxf.start_angle)
    end_angle = math.radians(arc.dxf.end_angle)

    start_point = (
        center.x + radius * math.cos(start_angle),
        center.y + radius * math.sin(start_angle))

    end_point = (
        center.x + radius * math.cos(end_angle),
        center.y + radius * math.sin(end_angle))

    mid_angle = (start_angle + end_angle) / 2

    if start_angle > end_angle:
        mid_point = (
            center.x + radius * math.cos(mid_angle),
            center.y - radius * math.sin(mid_angle))
    else:
        mid_point = (
            center.x + radius * math.cos(mid_angle),
            center.y + radius * math.sin(mid_angle))

    return start_point, mid_point, end_point

def addTrackLine(    
        boardObject,
        startPoint_mm,
        endPoint_mm,
        offset_mm,
        width_mm,
        layer):
    line = pcbnew.PCB_TRACK(board)
    line.SetStart(pcbnew.VECTOR2I(int((startPoint_mm[0] + offset_mm[0]) * 1E6), int((startPoint_mm[1] + offset_mm[1]) * 1E6)))
    line.SetEnd(pcbnew.VECTOR2I(int((endPoint_mm[0] + offset_mm[0]) * 1E6), int((endPoint_mm[1] + offset_mm[1]) * 1E6)))
    line.SetLayer(layer)
    line.SetWidth(int(width_mm * 1e6))
    boardObject.Add(line)

def addTrackArc(
        boardObject,
        startPoint_mm,
        midPoint_mm,
        endPoint_mm,
        offset_mm,
        width_mm,
        layer):
    arc = pcbnew.PCB_ARC(board)
    arc.SetEnd(pcbnew.VECTOR2I(int((startPoint_mm[0] + offset_mm[0]) * 1E6), int((startPoint_mm[1] + offset_mm[1]) * 1E6)))
    arc.SetMid(pcbnew.VECTOR2I(int((midPoint_mm[0] + offset_mm[0]) * 1E6), int((midPoint_mm[1] + offset_mm[1]) * 1E6)))
    arc.SetStart(pcbnew.VECTOR2I(int((endPoint_mm[0] + offset_mm[0]) * 1E6), int((endPoint_mm[1] + offset_mm[1]) * 1E6)))
    arc.SetLayer(layer)
    arc.SetWidth(int(width_mm * 1e6))
    boardObject.Add(arc)

def routeDXF(
        dxfFilePath,
        scaleFactor,
        positionPoint_mm,
        rotation_deg,
        trackWidth_mm,
        layer):
    doc = ezdxf.readfile(dxfFilePath)
    msp = doc.modelspace()

    for entity in msp.query('ARC'):
        entity.scale_uniform(scaleFactor)
        #entity.rotate_deg(rotation_deg)
        start, mid, end = calculateArcPoints(entity)

        addTrackArc(board,start,mid,end,positionPoint_mm,trackWidth_mm,layer)
    
    for entity in msp.query('LINE'):
        entity.scale_uniform(scaleFactor)
        #entity.rotate_deg(rotation_deg)
        start, end = calculateLinePoints(entity)

        #start += positionPoint_mm
        #end += positionPoint_mm

        addTrackLine(board,start,end,positionPoint_mm,trackWidth_mm,layer)
    
    pcbnew.Refresh()


board = pcbnew.GetBoard()
'''
if __name__ == "__main__":
    #dxf_file_path = "StatorPCBCoil-Sketch006.dxf"

    dxf_file_path = "test.dxf"
    #all_entities = get_all_entities_from_dxf(dxf_file_path)
    doc = ezdxf.readfile(dxf_file_path)
    msp = doc.modelspace()

    for entity in msp.query('ARC'):
        start, mid, end = calculateArcPoints(entity)
        addTrackArc(board,start,mid,end,0.04,pcbnew.F_Cu)
    
    for entity in msp.query('LINE'):
        start, end = calculateLinePoints(entity)
        addTrackLine(board,start,end,0.04,pcbnew.F_Cu)
    
'''
if __name__ == "__main__":
    #dxf_file_path = "StatorPCBCoil-Sketch006.dxf"

    dxf_file_path = "test.dxf"
    routeDXF("StatorPCBCoil-Sketch006.dxf",2,(-20,-10),0,0.04,pcbnew.F_Cu)
   
    

pcbnew.Refresh()
