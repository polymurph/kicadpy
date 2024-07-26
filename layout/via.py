import pcbnew
import numpy as np
import kicadpy as kp
import tools.mathUtils as mu

def autoRefresh():
    if kp._autoRefresh:
        kp.layoutRefresh()


def place(
    x_mm,
    y_mm,
    drillDiameter_mm,
    width_mm):
    via = pcbnew.PCB_VIA(kp._board)
    via.SetPosition(pcbnew.VECTOR2I(int((x_mm) * 1E6), int((y_mm) * 1E6)))
    via.SetDrill(int((drillDiameter_mm) * 1E6))
    via.SetWidth(int((width_mm) * 1E6))
    kp._board.Add(via)
    autoRefresh()


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
    autoRefresh()


def placeCircularArray(
    centerX_mm,
    centerY_mm,
    radius_mm,
    drillDiameter_mm,
    width_mm,
    startAngle_DEG,
    endAngle_DEG,
    n_vias,
    formatCartesian = True):

    delta = (endAngle_DEG - startAngle_DEG)/n_vias
   
    tmpStatus = kp._autoRefresh

    kp._autoRefresh = False
    for angle in np.linspace(startAngle_DEG,endAngle_DEG - delta,n_vias):
        placePolar(centerX_mm,
                   centerY_mm,
                   radius_mm,
                   angle,
                   drillDiameter_mm,
                   width_mm,
                   formatCartesian)
    kp._autoRefresh = tmpStatus
    
    autoRefresh()

