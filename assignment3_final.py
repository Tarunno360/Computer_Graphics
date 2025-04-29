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
player_health_bar=5

#game logic
score_card=0

#camera all variables
current_camera_position = [0, -500, 300]
current_camera_mode=0
camera_up_vector = [0, 0, 1]
camera_initial_angle = 0
camera_initial_height=300

#boundary variables
number_of_tiles=80
number_of_grids=13
central_position_grid=(number_of_tiles*number_of_grids)/2

total_enemy_at_a_time=5
enemies_char=[]

#bullet variables
bullet_char=[]
total_missed_bullets=0

#cheat 
cheat_mode_rotate_angle=0
cheat_mode_activated=False
Following_active=False

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

def draw_enemy_shape():
    if game_stopped==True:
        return
    for each_enemy in enemies_char:
        glPushMatrix()
        glTranslatef(each_enemy[0], each_enemy[1], each_enemy[2]+15)
        beep=each_enemy[3]
        glScalef(beep, beep, beep)
        glColor3f(1, 0, 0)
        glutSolidSphere(15,20,20)
        
        glPushMatrix()
        glTranslatef(0, 0, 20)
        glColor3f(0, 0, 0)
        glutSolidSphere(10, 20, 20)
        glPopMatrix()
        
        glPopMatrix()
        
def draw_bullet_pallents():
    if game_stopped==True:
        return
    glColor3f(1, 0, 0)
    for each_bullet in bullet_char:
        glPushMatrix()
        glTranslatef(each_bullet["position"][0], each_bullet["position"][1], 65)
        glutSolidSphere(5, 15, 15)
        glPopMatrix()

def reset_game():
    global player_current_position, player_current_angle, current_camera_position, game_stopped,player_health_bar, score_card, total_missed_bullets
    global enemies_char, bullet_char
    
    player_current_position = [0, 0, 0]
    player_current_angle = 0
    current_camera_position = [0, -500, 300]
    game_stopped = False
    
    enemies_char.clear()
    bullet_char.clear()
    score_card=0
    total_missed_bullets=0
    player_health_bar=5
    for _ in range(total_enemy_at_a_time):
        temp = create_enemy_position()
        enemy_temp = temp + [1.0, 1] 
        enemies_char.append(enemy_temp)
        
def keyboardListener(key, x, y):
    global player_current_position, player_current_angle, current_camera_position, game_stopped,cheat_mode_activated,cheat_mode_rotate_angle, Following_active,central_position_grid

    if current_camera_mode == 1:
        temp_step=12
    else:
        temp_step=20
    
    temp_rotation = 5

    if key == b'w':
        new_x = player_current_position[0] + temp_step * math.cos(math.radians(player_current_angle))
        new_y = player_current_position[1] + temp_step * math.sin(math.radians(player_current_angle))
        if -central_position_grid <= new_x <= central_position_grid:
            player_current_position[0] = new_x
        if -central_position_grid <= new_y <= central_position_grid:
            player_current_position[1] = new_y

    elif key == b's':
        new_x = player_current_position[0] - temp_step * math.cos(math.radians(player_current_angle))
        new_y = player_current_position[1] - temp_step * math.sin(math.radians(player_current_angle))
        if -central_position_grid <= new_x <= central_position_grid:
            player_current_position[0] = new_x
        if -central_position_grid <= new_y <= central_position_grid:
            player_current_position[1] = new_y

    elif key == b'a':
        player_angle += temp_rotation

    elif key == b'd':
        player_angle -= temp_rotation

    elif key == b'r' and game_stopped:
        reset_game()

    elif key == b'c' or key == b'C':
        cheat_mode_activated = not cheat_mode_activated
        if not cheat_mode_activated:
            Following_active = False
        

    elif key == b'v' or key == b'V':
        if cheat_mode_activated and cheat_mode_activated == 1:
            Following_active = not Following_active
            

    glutPostRedisplay()   

    
def specialKeyListener(key, x, y):
    global current_camera_mode, camera_initial_angle, camera_initial_height

    if current_camera_mode == 0:
        if key == GLUT_KEY_LEFT:
            camera_initial_angle -= 5
        elif key == GLUT_KEY_RIGHT:
            camera_initial_angle += 5
        elif key == GLUT_KEY_UP:
            if camera_initial_height < 600:
                camera_initial_height += 10
        elif key == GLUT_KEY_DOWN:
            if camera_initial_height > 100:  
                camera_initial_height -= 10


def mouseListener(button, state, x, y):
    global game_stopped, player_health_bar, total_missed_bullets,Following_active,camera_initial_angle,current_camera_mode
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        temp_posx=player_current_position[0]
        temp_posy=player_current_position[1]
        temp_angle= math.radians(player_current_angle)
        
        temp_dx=math.cos(temp_angle)
        temp_dy=math.sin(temp_angle)
        
        bullet_char.append({"position": [temp_posx, temp_posy, 0], "direction": [temp_dx, temp_dy]})
        
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        current_camera_mode= 1- current_camera_mode
        Following_active=False



    
    
    