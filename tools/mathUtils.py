import pcbnew
import numpy as np

def pol2cartDEG(phi, radius, formatCartesian=True):
    if formatCartesian :
        x = radius*np.sin(np.radians(phi+90))
        y = radius*np.cos(np.radians(phi+90))
    else:
        x = radius*np.sin(np.radians(phi))
        y = radius*np.cos(np.radians(phi))
    return x, y

