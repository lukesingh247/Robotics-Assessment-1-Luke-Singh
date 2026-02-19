import math
import random
from vexcode_vr import *

brain=Brain()
drivetrain = Drivetrain("drivetrain", 0)
pen = Pen("pen", 8)
pen.set_pen_width(THIN)
left_bumper = Bumper("leftBumper", 2)
right_bumper = Bumper("rightBumper", 3)
front_eye = EyeSensor("frontEye", 4)
down_eye = EyeSensor("downEye", 5)
front_distance = Distance("frontdistance", 6)
distance = front_distance
magnet = Electromagnet("magnet", 7)
location = Location("location", 9)

#function for quickly recording move and location
def wayback(route, turn, positions):
    route.append(turn)
    positions.append([location.position(X, MM), location.position(Y, MM), location.position_angle(DEGREES)])

#if robot reaches a dead end and has to go back will remove unnecessary path moves from route
def fixroute(route, positions):
    Xvalue = 0
    Yvalue = 0
    #little calc to determine which way backward the position needs to be looked for
    if location.position_angle(DEGREES) == (0):
        Yvalue = -250
        brain.print("FACING FORWARD")
    if location.position_angle(DEGREES) == (360):
        Yvalue = -250
        brain.print("FACING FORWARD")
    if location.position_angle(DEGREES) == 90:
        Xvalue = -250
        brain.print("FACING RIGHT")
    if location.position_angle(DEGREES) == 180:
        Yvalue = 250
        brain.print("FACING BACKWARDS")
    if location.position_angle(DEGREES) == 270:
        Xvalue = 250
        brain.print("FACING LEFT")
        
    for i, pos in enumerate(positions):
        #account for 20mm of space
        if location.position(X, MM) + Xvalue + 20 > pos[0] > location.position(X, MM) + Xvalue - 20 and location.position(Y, MM) + Yvalue + 20 > pos[1] > location.position(Y, MM) + Yvalue - 20:  # With tolerance
            found_index = i
            brain.new_line()
            brain.print("THE INDEX, ", i , " IS THE FIRST INSTANCE")
            destroyroute(route, positions, i)
            break
    return route
        
def destroyroute(route, positions, i):
    #set variables for understanding and giving turning direction to the crossroad position
    addturn = ""
    angle = 720
    priordirection = positions[i][2]
    brain.new_line()
    brain.print(priordirection)
    brain.new_line()
    #if statements for determining the correct angle to give to the turn at the crossroads
    if priordirection == 0:
        if location.position_angle(DEGREES) == 90: 
            addturn = "RIGHT"
            angle = 90
        if location.position_angle(DEGREES) == 270:
            addturn = "LEFT"
            angle = 270
    if priordirection == 360:
        if location.position_angle(DEGREES) == 90:
            addturn = "RIGHT"
            angle = 90
        if location.position_angle(DEGREES) == 270:
            addturn = "LEFT"
            angle = 270
    if priordirection == 90:
        if location.position_angle(DEGREES) == 0:
            addturn = "LEFT"
            angle = 0
        if location.position_angle(DEGREES) == 360:
            addturn = "LEFT"
            angle = 0
        if location.position_angle(DEGREES) == 180:
            addturn = "RIGHT"
            angle = 180
    if priordirection == 180:
        if location.position_angle(DEGREES) == 90:
            addturn = "LEFT"
            angle = 90
        if location.position_angle(DEGREES) == 270:
            addturn = "RIGHT"
            angle = 270
    if priordirection == 270:
        if location.position_angle(DEGREES) == 0:
            addturn = "RIGHT"
            angle = 0
        if location.position_angle(DEGREES) == 360:
            addturn = "RIGHT"
            angle = 0
        if location.position_angle(DEGREES) == 180:
            addturn = "LEFT"
            angle = 180
    
    #sets angle to straight forward
    if angle == 720:
        angle = location.position_angle(DEGREES)
    route[:] = route[:i + 1]
    positions[:] = positions[:i + 1]
    if len(route) >= 1:
        #if the crossroad angle is not facing the correct way by default add it
        if angle != 720:
            route.append(addturn)
            brain.print("added ", addturn, " turn")
        route.append("FORWARD")
        #add copy for route as well
        if len(positions) >= 1:
            last_pos = positions[-1]
            if angle != 720:
                positions.append([last_pos[0], last_pos[1], angle])
            positions.append([location.position(X, MM), location.position(Y, MM), location.position_angle(DEGREES)])
    #print new version of route
    brain.new_line()
    brain.print("route successfully destroyed here is new route")
    brain.new_line()
    brain.print(route)
    brain.new_line()
    brain.print("route length ", len(route), " positions length ", len(positions))
    brain.new_line()

def clean_route(route):
    #new array that is faster
    cleaned = []
    i = 0
    while i < len(route):
        if i < len(route) - 1:
            #check for pointless patterns
            if (route[i] == "RIGHT" and route[i+1] == "LEFT") or \
               (route[i] == "LEFT" and route[i+1] == "RIGHT"):
                brain.print(f"Skipping unnecessary turns at positions {i} and {i+1}")
                i += 2
                continue
        cleaned.append(route[i])
        i += 1
    return cleaned

def retreat(route):
    #set pen to green to mark 
    pen.set_pen_color(GREEN)
    movenumber2 = 0
    drivetrain.turn_for(RIGHT, 180, DEGREES)
    #if not at the start reverse the route backwards
    while not (140 > location.position(X, MM) > 120 and -920 < location.position(Y, MM) < -880):
        movenumber2-=1
        current = route[movenumber2]
        if current == "FORWARD":
            drivetrain.drive_for(FORWARD, 250, MM)
        if current == "RIGHT":
            drivetrain.turn_for(LEFT, 90, DEGREES)
        if current == "LEFT":
            drivetrain.turn_for(RIGHT, 90, DEGREES)

def main():
    #variables
    movenumber = 0
    ongoing = True
    fix = False
    route = []
    positions= []
    #start stuff
    wait(0.5, SECONDS)
    pen.move(DOWN)
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.set_turn_velocity(100, PERCENT)
    #setting starting direction and first right turn properly
    wayback(route, "FORWARD", positions)
    brain.print(movenumber, route[-1], " ")
    movenumber += 1
    drivetrain.turn_for(RIGHT, 90, DEGREES)
    wayback(route, "RIGHT", positions)
    brain.print(movenumber, route[-1], " ")
    movenumber += 1
    while ongoing:
        #move forward if nothing infront
        if front_distance.get_distance(MM) > 230:
            drivetrain.drive_for(FORWARD, 250, MM)
            wayback(route, "FORWARD", positions)
            brain.print(movenumber, route[-1], " ")
            #if dead end has been hit erase it from the route
            if fix:
                current_pos = [location.position(X, MM), location.position(Y, MM)]
                is_new_position = True
                #check new position against previous positions with 30mm of tolerance
                for prev_pos in positions[:-1]:  # Exclude current position
                    if (abs(prev_pos[0] - current_pos[0]) < 30 and 
                        abs(prev_pos[1] - current_pos[1]) < 30):
                        is_new_position = False
                        brain.print(f"Still near old position: {prev_pos}")
                        break
                
                #this triggers if the new position is actually new
                if is_new_position:
                    brain.print("REACHED NEW POSITION - REMOVING DEAD END")
                    route = fixroute(route, positions)
                    fix = False
            movenumber+=1
            #if robot reaches end remove unecessary turns then go back to start
            if down_eye.detect(RED):
                brain.new_line()
                brain.print("Solved")
                brain.new_line()
                finalroute = clean_route(route)
                brain.print(finalroute)
                brain.new_line()
                brain.print("final route length is", len(finalroute))
                retreat(finalroute)
                ongoing = False
            else:
                drivetrain.turn_for(RIGHT, 90, DEGREES)
                turn = "RIGHT"
                wayback(route, turn, positions)
                brain.print(movenumber, route[-1], " ")
                movenumber+=1
        #turn left if right doesnt work
        else:
            drivetrain.turn_for(LEFT, 90, DEGREES)
            turn = "LEFT"
            wayback(route, turn, positions)
            brain.print(movenumber, route[-1], " ")
            movenumber+=1
        if len(route) >= 4:
            if route[-4] == "RIGHT" and route[-3] == "LEFT" and route[-2] == "LEFT" and route[-1] == "LEFT":
                brain.print ("DEAD END")
                fix = True

#DO NOT DELETE
vr_thread(main())
