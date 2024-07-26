
# Import the necessary KiCad modules
import pcbnew
# https://github.com/atomic14/kicad-coil-plugins/blob/main/coil_plugin.py
# exec(open('track.py').read())

def addTrackLine(
        boardObject,
        startPoint_mm,
        endPoint_mm,
        width_mm,
        layer):
    track = pcbnew.PCB_TRACK(boardObject)
    track.SetStart(pcbnew.VECTOR2I(int(startPoint_mm[0] * 1E6), int(startPoint_mm[1] * 1E6)))
    track.SetEnd(pcbnew.VECTOR2I(int(endPoint_mm[0] * 1E6), int(endPoint_mm[1] * 1E6)))
    track.SetWidth(int(width_mm * 1e6))
    track.SetLayer(pcbnew.F_Cu)
    boardObject.Add(track)

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

# Create a new PCB layout or open an existing one
board = pcbnew.GetBoard()

track = pcbnew.PCB_TRACK(board)
track.SetStart(pcbnew.VECTOR2I(int(0), int(0)))
track.SetEnd(pcbnew.VECTOR2I(int(100E6), int(100E6)))
track.SetWidth(int(1 * 1e6))
track.SetLayer(pcbnew.F_Cu)
board.Add(track)

arc = pcbnew.PCB_ARC(board)
start = pcbnew.VECTOR2I(int(0), int(0))
mid = pcbnew.VECTOR2I(int(-50E6), int(50E6))
end = pcbnew.VECTOR2I(int(0), int(100E6))
arc.SetMid(mid)
arc.SetStart(start)
arc.SetEnd(end)
arc.SetLayer(pcbnew.F_Cu)
arc.SetWidth(int(1 * 1e6))
board.Add(arc)

addTrackLine(board,[10,10],[50,20],10,pcbnew.F_Cu)
addTrackArc(board,[20,20],[40,40],[60,20],1,pcbnew.F_Cu)

# Update the display to show the new arc
pcbnew.Refresh()
