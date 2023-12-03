# UE Progress Record


## MassAI Demo following the video
https://www.youtube.com/watch?v=2LvUB3_PAhI</br>
### Problem1: Groom
enable Groom Plugin</br>

### Problem2: Fragment
//////some change about fragments////////</br>

### Problem2: Loop Animation
ABPCrowd -> select MTN_N_Walk_F -> Settings -> enable Loop Animation</br>


## Predefined path + timer demo
https://youtu.be/-V6D5WtemMI?si=NFlohOWUl0ob4YYo</br>

## Python Scripting (11/5/23)
Official document:  https://docs.unrealengine.com/5.1/en-US/scripting-the-unreal-editor-using-python/

### Python setup and install modules with pip
enable Python Editor Script Plugin</br>
https://dev.epicgames.com/community/learning/tutorials/lJly/python-install-modules-with-pip-unreal-engine-5-tutorial</br>

### Run the specified Python script when opening the project
Edit -> Project Settings -> Plugins -> Python</br>
Startup Scripts -> Add Array Element -> add file name (main.py)</br>
Additional Paths -> Add Array Element -> add path for the file (C:\Users\Administrator\Desktop\airport code\)</br>

### Import csv as Data Table
create blueprint for movementTrack info ran by main.py: https://youtu.be/Mb2iWvDxXNk?si=3vgWuXV2PQYGRa0g</br>
in main.py, export csv to the ue project Content Drawer location</br>
add a "Row" column as the first column in csv</br>
movementTrack in the form of "(0,0,0,1,1,1)" to be read as Data Table array</br>
in main.py, export person.movementTrack as str(person.movementTrack).replace('[','(').replace(']',')').replace(' ','') ot match the above format</br>
click allow import 

## predefined path 11/11/23
DA_CrowdAgent
index[0] -> fragments -> agent raduis fragment -> path radius

## avoidance/detour 12/3/23
BP_character
character movement: avoidance - use RVOAvoidance
DA_CrowdAgent
avoidance parameter change - time, radius


