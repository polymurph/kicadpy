import os
import pcbnew
import layout.via as via

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
