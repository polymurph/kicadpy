import os
import imp

import pcbnew
import layout.via as via
import layout.footprint as footprint
import layout.track as track
import utils.utils as utils

imp.reload(via)
imp.reload(footprint)
imp.reload(track)

_autoRefresh = False
_board = pcbnew.GetBoard()

print("Info: Kicadpy is ready to be used")

def setAutoRefresh(status: bool):
    global _autoRefresh
    print(f"Auto Resfresh is set to: {status} ")
    _autoRefresh = status

def getProjectPath():
    path = _board.GetFileName()
    return path.rpartition('/')[0]


def layoutRefresh():
    pcbnew.Refresh()

def layoutSave():
    pcbnew.Save()
