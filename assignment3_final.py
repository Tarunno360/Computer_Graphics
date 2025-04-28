from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

#player all variables 
player_current_position = [0, 0, 0]
player_current_angle = 0

#camera all variables
current_camera_position = [0, -500, 300]
current_camera_mode=0

#boundary variables
number_of_tiles=80
number_of_grids=13
central_position_grid=(number_of_tiles*number_of_grids)/2

total_enemy_at_a_time=5
enemies_char=[]

def create_enemy_position():
    x=random.uniform(-central_position_grid, central_position_grid)
    y=random.uniform(-central_position_grid, central_position_grid)
    z=15
    return [x, y, z]

for i in range(total_enemy_at_a_time):
    enemies_char.append([*create_enemy_position(),0.7,1])


    
    
    