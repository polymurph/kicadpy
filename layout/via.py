import pcbnew
import numpy as np
import kicadpy as kp
import tools.mathUtils as mu

def place(
    x_mm,
    y_mm,
    drillDiameter_mm,
    width_mm,
    formatCartesian = True):

    if(formatCartesian):
        y_mm *= -1

    via = pcbnew.PCB_VIA(kp._board)
    via.SetPosition(pcbnew.VECTOR2I(int((x_mm) * 1E6), int((y_mm) * 1E6)))
    via.SetDrill(int((drillDiameter_mm) * 1E6))
    via.SetWidth(int((width_mm) * 1E6))
    kp._board.Add(via)
    kp.utils.autoRefresh()


def placePolar(
    center_x_mm,
    center_y_mm,
    radius_mm,
    angle_DEG,
    drillDiameter_mm,
    width_mm,
    formatCartesian = True):

    via = pcbnew.PCB_VIA(kp._board)
    x, y = mu.pol2cartDEG(angle_DEG, radius_mm, formatCartesian)
    x += center_x_mm
    y += center_y_mm
    via.SetPosition(pcbnew.VECTOR2I(int((x) * 1E6), int((y) * 1E6)))
    via.SetDrill(int((drillDiameter_mm) * 1E6))
    via.SetWidth(int((width_mm) * 1E6))
    kp._board.Add(via)
    kp.utils.autoRefresh()

def placeArray(
    start_x_mm,
    start_y_mm,
    end_x_mm,
    end_y_mm,
    drillDiameter_mm,
    width_mm,
    n_vias,
    formatCartesian = True):

    tmpStatus = kp._autoRefresh
    kp._autoRefresh = False

    delta_x = (end_x_mm - start_x_mm) / (n_vias-1)
    delta_y = (end_y_mm - start_y_mm) / (n_vias-1)
    
    x = start_x_mm
    y = start_y_mm

    for i in range(n_vias):
        place(x,y,drillDiameter_mm, width_mm, formatCartesian)
        x += delta_x
        y += delta_y
    
    kp._autoRefresh = tmpStatus
    kp.utils.autoRefresh()

def placeCircularArray(
    centerX_mm,
    centerY_mm,
    radius_mm,
    drillDiameter_mm,
    width_mm,
    startAngle_DEG,
    endAngle_DEG,
    n_vias,
    placeEndToEnd = False,
    formatCartesian = True):

    delta = (endAngle_DEG - startAngle_DEG)/n_vias
   
    tmpStatus = kp._autoRefresh
    kp._autoRefresh = False


    if placeEndToEnd:
        endAngle = endAngle_DEG
    else:
        endAngle = endAngle_DEG - delta
    
    for angle in np.linspace(startAngle_DEG,endAngle,n_vias):
        placePolar(
            centerX_mm,
            centerY_mm,
            radius_mm,
            angle,
            drillDiameter_mm,
            width_mm,
            formatCartesian)

    kp._autoRefresh = tmpStatus
    
    kp.utils.autoRefresh()

