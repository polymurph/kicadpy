import pcbnew
import numpy as np
import kicadpy as kp

def setToFront(
    referenceDesignator_s,
    front = True):

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
    footprint = kp._board.FindFootprintByReference(referenceDesignator)
    return not(footprint.IsFlipped())