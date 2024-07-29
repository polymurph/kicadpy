import pcbnew
import kicadpy as kp

def autoRefresh():
    if kp._autoRefresh:
        kp.layoutRefresh()