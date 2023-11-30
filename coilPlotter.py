import numpy as np
import ezdxf
import math
import pcbnew

# command to be executed inside the Kicad scripting shell sothat this script will be executed
#exec(open('coilPlotter.py').read())

def getDirectionFactor(start_point, center, end_point):
    #https://math.stackexchange.com/questions/1525961/determine-direction-of-an-arc-cw-ccw
    return (start_point[0] - center[0])*(end_point[1] - center[1]) - (start_point[1]-center[1])*(end_point[0]-center[0])
    

def calculate_radius(center, point):
    cx, cy = center
    px, py = point
    return math.sqrt((px - cx)**2 + (py - cy)**2)

def add_arc(msp, center, start_point, end_point, layer):
    radius = calculate_radius(center, start_point)
    start_angle = math.degrees(math.atan2(start_point[1] - center[1], start_point[0] - center[0]))
    end_angle = math.degrees(math.atan2(end_point[1] - center[1], end_point[0] - center[0]))
    msp.add_arc(center=center, radius=radius, start_angle=start_angle, end_angle=end_angle, dxfattribs={'layer': layer})

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

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
    #input("press any key to continue")
    #pcbnew.Refresh()

def addTrackArcAngles(
        boardObject,
        startAngle_DEG,
        endAngle_DEG,
        radius_mm,
        center_mm,
        width_mm,
        layer):
    
    start_angle = math.radians(startAngle_DEG)
    end_angle = math.radians(endAngle_DEG)

    if start_angle > end_angle and True:
        endAngle_DEG += math.radians(180)

    start = (radius_mm * math.cos(start_angle) + center_mm[0], radius_mm * math.sin(start_angle)+ center_mm[1])
    end = (radius_mm * math.cos(end_angle)+ center_mm[0], radius_mm * math.sin(end_angle)+ center_mm[1])

    #mid_angle = startAngle_DEG + (endAngle_DEG - startAngle_DEG) / 2
    mid_angle = start_angle + (end_angle - start_angle) / 2

    mid = (radius_mm * math.cos(mid_angle) + center_mm[0], radius_mm * math.sin(mid_angle)+ center_mm[1])


    if 0:
        c = getDirectionFactor(start,mid,end)
        
        if c > 0: # arc is CW
            print("CW")


        if c < 0: # arc is CCW
            print("CCW")
    
    arc = pcbnew.PCB_ARC(boardObject)
    arc.SetStart(pcbnew.VECTOR2I(int((start[0]) * 1E6), int((start[1]) * 1E6)))
    arc.SetMid(pcbnew.VECTOR2I(int((mid[0]) * 1E6), int((mid[1]) * 1E6)))
    arc.SetEnd(pcbnew.VECTOR2I(int((end[0]) * 1E6), int((end[1]) * 1E6)))
    arc.SetLayer(layer)
    arc.SetWidth(int(width_mm * 1e6))
    boardObject.Add(arc)
    #pcbnew.Refresh()
    #input("wainting")

def dxfLineToTrack(
        boardObject,
        line,
        width_mm,
        layer):
    addTrackLine(
        boardObject,
        line.dxf.start,
        line.dxf.end,
        (0,0),
        width_mm,layer)

def dxfArcToTrack(
        boardObject,
        arc,
        width_mm,
        layer):

    addTrackArcAngles(
        boardObject,
        arc.dxf.start_angle,
        arc.dxf.end_angle,
        arc.dxf.radius,
        arc.dxf.center,
        width_mm,
        layer)


def drawTrackCoil(
    boardObject,
    startAngle,
    endAngle,
    deltaPhi,
    deltaR,
    edgeRadius,
    R1,
    R2,
    centerPoint,
    N):
    
    if R1 >= R2:
        raise ValueError('R1 must be smaller than R2.')
    if N * deltaR >= R1:
        raise ValueError('R1 must be greater than N * deltaR')
    if startAngle > endAngle:
        raise ValueError('endAngle must be greater than startAngle')
    
    ri = R1 - stepRadius
    ro = R2 + stepRadius
    r_e = edgeRadius
    phi_S = startAngle
    phi_E = endAngle
    
    phi_Mid = phi_E - (phi_E - phi_S) / 2
    
    for n in range(N):
        #----------------------------------------------------------------
        # arc from point 1 to 2
        phi_1 = phi_Mid
        r_1 = ri
        
        r_a = (R1 - ri) / 2
        phi_a = np.arctan(r_a / (r_a + ri))
        phi_b = np.pi/2 - 2 * phi_a
        r_c1 = R1 / np.cos(2 * phi_a)
        phi_c1 = phi_E - 2 * phi_a
        phi_c1s = phi_E - 2 * phi_a - phi_b + np.pi
        phi_c1e = phi_E - 2 * phi_a + np.pi
        phi_2 = phi_E - 2 * phi_a
        r_2 = ri
        r_e = R1 * np.tan(2 * phi_a)
        
        
        P1 = pol2cart(r_1, phi_1)
        P2 = pol2cart(r_2, phi_2)

        #msp.add_arc(centerPoint, ri, np.degrees(phi_1), np.degrees(phi_2),is_counter_clockwise=True)
        addTrackArcAngles(boardObject,np.degrees(phi_1), np.degrees(phi_2), ri, centerPoint, 0.04, pcbnew.F_Cu)
        #----------------------------------------------------------------
        # edge arc from 2 to 3
        
        r_3 = R1
        phi_3 = phi_E
        
        
        P3 = pol2cart(r_3, phi_3)
        PC1 = pol2cart(r_c1, phi_c1)
        
        #msp.add_arc(PC1, r_e, np.degrees(phi_c1s) , np.degrees(phi_c1e),is_counter_clockwise=True)
        addTrackArcAngles(boardObject,np.degrees(phi_c1s), np.degrees(phi_c1e), r_e, PC1, 0.04, pcbnew.F_Cu)
        #----------------------------------------------------------------
        # line from 3 to 4
        
        phi_4 = phi_E
        r_4 = R2
        
        
        P4 = pol2cart(r_4, phi_4) 
        
        #msp.add_line(P3,P4)
        addTrackLine(boardObject, P3, P4, (0,0), 0.04, pcbnew.F_Cu)
        #----------------------------------------------------------------
        # edge arc from 4 to 5
        
        r_5 = ro
        r_a = (ro - R2) / 2
        phi_a = np.arctan(r_a / (R2 + r_a))
        phi_b = np.pi/2 - 2 * phi_a
        r_c2 = R2 / np.cos(2 * phi_a)
        phi_c2 = phi_E - 2 * phi_a
        phi_c2s = phi_E - 2 * phi_a
        phi_c2e = phi_c2s + np.pi - phi_b
        phi_5 = phi_E - 2 * phi_a
        r_e = R2 * np.tan(2 * phi_a)
        
        PC2 = pol2cart(r_c2, phi_c2)

        #msp.add_arc(PC2, r_e, np.degrees(phi_c2s), np.degrees(phi_c2e),is_counter_clockwise=True)
        addTrackArcAngles(boardObject,np.degrees(phi_c2s), np.degrees(phi_c2e), r_e, PC2, 0.04, pcbnew.F_Cu)
        #----------------------------------------------------------------
        # step start angle
        #phiS -= deltaPhi
        
        #----------------------------------------------------------------
        # arc from 5 to 6
        
        r_6 = ro
        r_a = (ro - R2) / 2
        phi_a = np.arctan(r_a / (R2 + r_a))
        phi_b = np.pi / 2 - 2 * phi_a
        r_c3 = R2 / np.cos(2 * phi_a)
        phi_c3s = phi_S + 3/2 * np.pi
        phi_c3e = phi_c3s + np.pi - phi_b#########
        phi_6 = phi_S + 2 * phi_a
        phi_c3 = phi_S + 2 * phi_a
        r_e = R2 * np.tan(2 * phi_a)
        
        P6 = pol2cart(r_6, phi_6)
        PC3 = pol2cart(r_c3, phi_c3)
        

        #msp.add_arc(centerPoint, ro, np.degrees(phi_6), np.degrees(phi_5),is_counter_clockwise=True)
        addTrackArcAngles(boardObject,np.degrees(phi_5), np.degrees(phi_6), ro, centerPoint, 0.04, pcbnew.F_Cu)
        #----------------------------------------------------------------
        # edge arc from 6 to 7
        
        phi_7 = phi_S
        r_7 = R2
                
        
        P7 = pol2cart(r_7, phi_7)
        

        #print("delta c3:\t" + str(phi_c3e-phi_c3s))
        #msp.add_arc(PC3, r_e, np.degrees(phi_c3s), np.degrees(phi_c3e),is_counter_clockwise=True)
        addTrackArcAngles(boardObject,np.degrees(phi_c3s), np.degrees(phi_c3e), r_e, PC3, 0.04, pcbnew.F_Cu)
        #----------------------------------------------------------------
        # step inner radius
        
        ri -= deltaR
        
        #----------------------------------------------------------------
        # line from 7 to 8

        phi_8 = phi_S
        r_8 = R1
        
        P8 = pol2cart(r_8, phi_8)
        
        #msp.add_line(P7,P8)
        addTrackLine(boardObject, P7, P8, (0,0), 0.04, pcbnew.F_Cu)
        #----------------------------------------------------------------
        # step outer diameter adn end angle
        
        #ro += deltaR
        #phiE += deltaPhi
        #re += deltaR
        
        #----------------------------------------------------------------
        # edge arc from 8 to 9
        
        r_a = (R1 - ri) / 2
        phi_a = np.arctan(r_a / (r_a + ri))
        phi_b = np.pi / 2 - 2 * phi_a
        r_c4 = R1 / np.cos(2 * phi_a)
        phi_c4 = phi_S + 2 * phi_a
        phi_c4s = phi_S + 2 * phi_a + np.pi
        phi_c4e = phi_c4s + phi_b      
        phi_9 = phi_S + 2 * phi_a
        r_9 = ri
        r_e = R1 * np.tan(2 * phi_a)
        
        PC4 = pol2cart(r_c4, phi_c4)
        #print("delta c4:\t" + str(phi_c4e-phi_c4s))
        
        #msp.add_arc(PC4, r_e, np.degrees(phi_c4s), np.degrees(phi_c4e),is_counter_clockwise=True)
        addTrackArcAngles(boardObject,np.degrees(phi_c4s), np.degrees(phi_c4e), r_e, PC4, 0.04, pcbnew.F_Cu)
        #----------------------------------------------------------------
        # arc from 9 to 10
        
        phi_10 = phi_Mid
        r_10 = ri
        P10 = pol2cart(r_10, phi_10)
        
        #msp.add_arc(centerPoint, ri, np.degrees(phi_9), np.degrees(phi_10))
        addTrackArcAngles(boardObject,np.degrees(phi_9), np.degrees(phi_10), ri, centerPoint, 0.04, pcbnew.F_Cu)
        #----------------------------------------------------------------
        # step
        ro += deltaR
        phi_S -= deltaPhi
        phi_E += deltaPhi

    pcbnew.Refresh()



board = pcbnew.GetBoard()
doc = ezdxf.readfile("coilSection.dxf")
msp = doc.modelspace()

startAngle = np.radians(25.5)
endAngle = np.radians(34.5)
stepAngle = np.radians(0.5)
stepRadius = 0.07
trackWidth = 0.2
R1 = 10
R2 = 16
N = 50

doc = ezdxf.new()
msp = doc.modelspace()


adjustAngle = 30
startAngle += np.radians(adjustAngle)
endAngle += np.radians(adjustAngle)

if 0:
    drawTrackCoil(
                board,
                startAngle,
                endAngle,
                stepAngle,
                stepRadius,
                trackWidth,
                R1, 
                R2,
                (0,0),
                N)


if 1:
    incrementAngle = 60
    for i in range(6):
        startAngle += np.radians(incrementAngle)
        endAngle += np.radians(incrementAngle)

        print("###########################")
        print("start angle\t"+str(startAngle))
        print("end angle\t"+str(endAngle))
        drawTrackCoil(
            board,
            startAngle,
            endAngle,
            stepAngle,
            stepRadius,
            trackWidth,
            R1, 
            R2,
            (0,0),
            N)
        print("###########################")

doc.saveas('coilSection.dxf') 
print("done!")
