from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

fovY = 120
GRID_LENGTH = 600
rand_var = 423

#button variables
game_stopped = False

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

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_12):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def create_enemy_position():
    x=random.uniform(-central_position_grid, central_position_grid)
    y=random.uniform(-central_position_grid, central_position_grid)
    z=15
    return [x, y, z]

for i in range(total_enemy_at_a_time):
    enemies_char.append([*create_enemy_position(),0.7,1])
    
    
    
def draw_player_shape():
    glPushMatrix()
    glTranslatef(player_current_position[0], player_current_position[1], 0)
    
    if game_stopped==True:
        glRotatef(player_current_angle, 0, 0, 1)
    else:
        glRotatef(90, 1, 0, 0)
    
    glPushMatrix()
    glColor3f(0.0, 0.0, 1.0)
    glTranslatef(0, -15, 30)
    glScalef(1,1,2.5)
    glutSolidCube(20)
    glPopMatrix()
    
    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(0, 15, 30)
    glScalef(1, 1, 2.5)
    glutSolidCube(20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.5, 0.7, 0.4)
    glTranslatef(0, 0, 60)
    glScalef(1, 1.5, 2)
    glutSolidCube(20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(0, 0, 95)
    glutSolidSphere(10, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.96, 0.8, 0.69)
    glTranslatef(0, -20, 65)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 5, 20, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.96, 0.8, 0.69)
    glTranslatef(0, 20, 65)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 5, 20, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.3, 0.3, 0.3)
    glTranslatef(0, 0, 65)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 3, 3, 30, 10, 10)
    glPopMatrix()

    glPopMatrix()


        
    

    
    
    