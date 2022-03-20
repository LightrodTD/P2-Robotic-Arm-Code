## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.

import random
import sys
sys.path.append('../')

from Common_Libraries.p2_sim_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()
update_thread = repeating_timer(2, update_sim)

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
#Assign a location variable that can be used between multiple functions
global location

#Identify Autoclave location function. Input: container ID
def identifyLocation(containerID):
    #Changing location variable's definition
    global location
    #Location is a list that contains the coordinates for every drop-off position (for the containers)
    location = []

    #Everytime this function is called properly, the global variable location shall change accordingly
    
    #Id's and location for the containers
    #Small, Red container
    if containerID == 1:
        location = [-0.586, 0.234, 0.38]
    
    #Small, Green container
    elif containerID == 2:
        location = [0, -0.63, 0.38]
    
    #Small, Blue container
    elif containerID == 3:
        location = [0, 0.63, 0.38]
        
    #Large, Red container
    elif containerID == 4:
        location = [-0.374, 0.155, 0.296]
    
    #Large, Green container
    elif containerID == 5:
        location = [0, -0.405, 0.296]
    
    #Large, Blue container
    elif containerID == 6:
        location = [0, 0.405, 0.296]
        
    #Returns location with new definition
    #Format for location: [x-coordinate, y-coordinate, z-coordinate]
    return location


#Control Gripper function. Input: right emg sensor, left emg sensor, and container ID
def controlGripper(right_emg, left_emg, containerID):
    #If gripper position is at pick-up location
    if arm.effector_position() == (0.509, 0.0, 0.04):
        #If right & left emg sensor are above threshold
        if (right_emg > 0.5) and (left_emg > 0.5):
            #If the container is a large container
            if containerID >= 4:
                #The gripper closes by 25 degrees, given the larger size
                arm.control_gripper(25)
            #If the container is a small container    
            elif containerID <= 3:
                #Gripper closes by 30 degrees
                arm.control_gripper(30)

    #If the gripper is not at pick-up location (which means its at a certain drop-off location)        
    else:
        #If right & left emg sensor are above threshold
        if (right_emg > 0.5) and (left_emg > 0.5):
            #If the container is a large container
            if containerID >= 4:
                #Open the gripper by the negative of the grabbing angle (-25 degrees)
                arm.control_gripper(-25)
            #If the container is a small container    
            elif containerID <= 3:
                #Open the gripper by the negative of the grabbing angle (-30 degrees)
                arm.control_gripper(-30)


#Move end effector function. Input: right emg sensor, left emg sensor, and container ID if required
def move_end_effector(right_emg, left_emg, container_IDn=None):

    #If right emg sensor is 0, and left emg sensor is above threshold
    if  (right_emg == 0) and (left_emg > 0.5):
        #If the end effector is at home position, move to pick-up location.
        #Having no container ID as a parameter (and run default value) indicates that the arm is holding nothing
        if arm.effector_position() == (0.406, 0.0, 0.483):
            arm.move_arm(0.509, 0.0, 0.04)

        #If the container ID is 1
        elif container_IDn == 1:
            #Drop-off location for small red container
            #Moves end effector based on what the location is for the container ID(1)
            #Selects the appropriate elements of the location list (assigned in identifyLocation()), and uses it as parameters for arm.move_arm()
            arm.move_arm(location[0], location[1], location[2])

        #Conatiner ID is 2    
        elif container_IDn == 2:
            #Drop-off location for small green container
            arm.move_arm(location[0], location[1], location[2])

        #Conatiner ID is 3   
        elif container_IDn == 3:
            #Drop-off location for small blue container
            arm.move_arm(location[0], location[1], location[2])

        #Conatiner ID is 4   
        elif container_IDn == 4:
            #Drop-off location for large red container
            arm.move_arm(location[0], location[1], location[2])

        #Conatiner ID is 5   
        elif container_IDn == 5:
            #Drop-off location for large green container
            arm.move_arm(location[0], location[1], location[2])

        #Conatiner ID is 6   
        elif container_IDn == 6:
            #Drop-off location for large blue container
            arm.move_arm(location[0], location[1], location[2])


#Open Autoclave function. Input: right emg sensor, left emg sensor, container ID, and an input of True or False
def open_autoclave(right_emg, left_emg, containerID, openBin):
    #Id the right emg sensor is above threshold, and left emg sensor is 0
    if (right_emg > 0.5) and (left_emg == 0):
        #If you wish to open a bin
        if openBin == True:
            #Depeneding on container ID for large containers (4,5,6), it will open said autoclave
            if containerID == 4:
                arm.open_red_autoclave(True)
        
            elif containerID == 5:
                arm.open_green_autoclave(True)
    
            elif containerID == 6:
                arm.open_blue_autoclave(True)
        #If you wish to close the bin
        else:
            #Depeneding on container ID for large containers (4,5,6), it will close said autoclave
            if containerID == 4:
                arm.open_red_autoclave(False)
        
            elif containerID == 5:
                arm.open_green_autoclave(False)
    
            elif containerID == 6:
                arm.open_blue_autoclave(False)

#Main cycle function. No inputs
def mainCycle():
    #List of Container ID's
    ID = [1,2,3,4,5,6]

    #While loop so all containers may be moved to designated positions
    while True:
        #Determine random ID by choosing random list element (from list 'ID')
        ran = random.randint(0, (len(ID)-1))
        #Assign current Container ID as previously choosen(randomly) element from ID list
        container_ID = ID[ran]

        #Move Q-arm to home position
        arm.home()
        
        #Spawn Container
        time.sleep(1)
        arm.spawn_cage(container_ID)
    
        #Identify Container Location
        identifyLocation(container_ID)
        time.sleep(3)
    
        #Move arm to pick up position
        move_end_effector(arm.emg_right(), arm.emg_left())
        time.sleep(5)
    
        #Grab container
        controlGripper(arm.emg_right(), arm.emg_left(), container_ID)
        time.sleep(5)
    
        #Move Container to proper location
        move_end_effector(arm.emg_right(), arm.emg_left(), container_ID)
        time.sleep(5)
    
        #Open Autoclave if required
        if container_ID >= 4:
            open_autoclave(arm.emg_right(), arm.emg_left(), container_ID, True)
            time.sleep(5)
    
        #Drop container
        controlGripper(arm.emg_right(), arm.emg_left(), container_ID)
        time.sleep(5)
    
        #Close Autoclave if required
        if container_ID >= 4:
            open_autoclave(arm.emg_right(), arm.emg_left(), container_ID, False)
            time.sleep(5)
            
        #After current container has been placed in position, remove ID from list
        ID.remove(container_ID)
        #If the container ID list is empty, return the Q-arm to its home position, and exit loop
        if len(ID) == 0:
            arm.home()
            break

    
      
#Run the entire process
mainCycle()
        


        


#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
