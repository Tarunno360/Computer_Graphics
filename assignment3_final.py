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
player_current_position = [0, 0]
player_current_angle = 0.0
player_health_bar=5

#game logic
score_card=0

#camera all variables
current_camera_position = [0, -500, 300]
current_camera_mode=0
camera_up_vector = [0, 0, 1]
camera_initial_angle = 0
camera_initial_height=300
cam_look_at = [0, 0, 0]

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
    
    if game_stopped:
        glRotatef(90, 1, 0, 0) 
    else:
        glRotatef(player_current_angle, 0, 0, 1)
    
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
    
    #enemies_char.clear()
    bullet_char.clear()
    score_card=0
    total_missed_bullets=0
    player_health_bar=5
    for i in range(total_enemy_at_a_time):
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
        player_current_angle += temp_rotation

    elif key == b'd':
        player_current_angle -= temp_rotation

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
        
        bullet_char.append({
        "position": [temp_posx, temp_posy],
        "direction": [temp_dx, temp_dy]
        })

        
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        current_camera_mode= 1- current_camera_mode
        Following_active=False

def animate():
    global player_current_position, player_current_angle, current_camera_position, game_stopped, player_health_bar
    global enemies_char, bullet_char, total_missed_bullets, score_card,cheat_mode_rotate_angle

    if game_stopped:
        glutPostRedisplay()
        return
    
    for each_enemy in enemies_char:
        temp_dx= player_current_position[0] - each_enemy[0]
        temp_dy= player_current_position[1] - each_enemy[1]
        distance_enemy_player=math.sqrt(temp_dx**2 + temp_dy**2)
        if distance_enemy_player <20:
            player_health_bar-=1
            print("Player hit by enemy!")
            print(f"Player Health: {player_health_bar}")
            if player_health_bar <= 0:
                game_stopped = True
                print("Game Over!")
            each_enemy[:]=[*create_enemy_position(),1,1]
                #reset_game()
        else:
            temp_velocity=0.1
            each_enemy[0] += temp_velocity * (temp_dx / distance_enemy_player)
            each_enemy[1] += temp_velocity * (temp_dy / distance_enemy_player)
        
        temp_scale,temp_direction=each_enemy[3],each_enemy[4]
        #temp_direction=each_enemy[4]
        del_scale=0.005
        temp_scale += del_scale * temp_direction
        temp_scale,temp_direction=each_enemy[3],each_enemy[4]
        del_scale=0.01
        
        if temp_direction==1:
            temp_scale+=del_scale
            if temp_scale>=1.5:
                temp_direction=-1
        else:
            temp_scale-=del_scale
            if del_scale<=0.7:
                temp_direction=1
    
        each_enemy[3]=temp_scale
        each_enemy[4]=temp_direction
        
    temp_bullets=[]
    for each_bullets in bullet_char:
        each_bullets["position"][0] += each_bullets["direction"][0] * 5
        each_bullets["position"][1] += each_bullets["direction"][1] * 5
        
        temp_b_dx,temp_b_dy= each_bullets["position"]
        
        if not (-central_position_grid <= temp_b_dx <= central_position_grid and -central_position_grid <= temp_b_dy <= central_position_grid):
            total_missed_bullets += 1
            #temp_bullets.append(each_bullets)
            print(f'Bullet missed! Now your total bullet miised it {total_missed_bullets}')
            if total_missed_bullets > 9:
                game_stopped = True
                print("Game Over! You have missed you 10 bullets")
            continue
    
        enemy_shot_dead=False
        for i,j in enumerate(enemies_char):
            temp_e_dx,temp_e_dy= j[0],j[1]
            if math.dist([temp_b_dx,temp_b_dy],[temp_e_dx,temp_e_dy])<20*j[3]:
                enemy_shot_dead=True
                score_card+=1
                print(f"Enemy shot! Score: {score_card}")
                enemies_char[i]=[*create_enemy_position(),1.0,1.0]
                break
        if not enemy_shot_dead:
            temp_bullets.append(each_bullets)
            
    bullet_char=temp_bullets
    if cheat_mode_activated and not game_stopped:
        if current_camera_mode==1:           
            cheat_mode_rotate_angle+=1.8
        else:
            cheat_mode_rotate_angle+=2
        cheat_mode_rotate_angle=cheat_mode_rotate_angle%360
        player_current_angle=cheat_mode_rotate_angle
    
        for each_enemy in enemies_char:
            temp1_dx=each_enemy[0]- player_current_position[0]
            temp1_dy=each_enemy[1]- player_current_position[1]
            temp_angle_etop= math.degrees(math.atan2(temp1_dy, temp1_dx))%360
            temp_angle_diff= abs((temp_angle_etop-cheat_mode_rotate_angle+180)%360-180)
            
            if temp_angle_diff<1:
                temp_in_radian= math.radians(cheat_mode_rotate_angle)
                #bullet_char.append({"position": [each_enemy[0], each_enemy[1], 0], "direction": [math.cos(temp_in_radian), math.sin(temp_in_radian)]})
                bullet_char.append({
                "position": [player_current_position[0], player_current_position[1]],
                "direction": [math.cos(temp_in_radian), math.sin(temp_in_radian)]
                })
                break
            
    glutPostRedisplay()

def camera_functionality():
    radius=500
    global current_camera_mode,camera_initial_height,current_camera_position,player_current_position,cam_look_at,cheat_mode_rotate_angle,camera_up_vector
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if current_camera_mode==0:
        temp_rad_angle= math.radians(camera_initial_height)
        current_camera_position[0]=radius*math.cos(temp_rad_angle)+player_current_position[0]
        current_camera_position[1]=radius*math.sin(temp_rad_angle)+player_current_position[1]
        current_camera_position[2]=camera_initial_height
        cam_look_at[0]=player_current_position[0]
        cam_look_at[1]=player_current_position[1]
        cam_look_at[2]=60
        
    else:
        if cheat_mode_activated and Following_active:
            
            temp_rad_angle= math.radians(cheat_mode_rotate_angle)
        else:
            if cheat_mode_activated:
                if Following_active:
                    temp_rad_angle= math.radians(cheat_mode_rotate_angle)
                else:
                    temp_rad_angle= math.radians(0)
            else:
                temp_rad_angle= math.radians(player_current_angle)
        
        current_camera_position[0]= player_current_position[0] + 50*math.cos(temp_rad_angle)
        current_camera_position[1]= player_current_position[1] + 50*math.sin(temp_rad_angle)
        current_camera_position[2]= 100
        cam_look_at[0]=player_current_position[0]+ 50*math.cos(temp_rad_angle)
        cam_look_at[1]=player_current_position[1]+ 50*math.sin(temp_rad_angle)
        cam_look_at[2]= 100
    gluLookAt(*current_camera_position, *cam_look_at, *camera_up_vector)
    
def draw_grid():
    for i in range(number_of_grids):
        for j in range(number_of_grids):
            if (i + j) % 2 == 0:
                glColor3f(0.7, 0.5, 0.95)
            else:
                glColor3f(1.0, 1.0, 1.0)

            temp_x = -central_position_grid + i * number_of_tiles
            temp_y = -central_position_grid + j * number_of_tiles

            glBegin(GL_QUADS)
            glVertex3f(temp_x, temp_y, 0)
            glVertex3f(temp_x + number_of_tiles, temp_y, 0)
            glVertex3f(temp_x + number_of_tiles, temp_y + number_of_tiles, 0)
            glVertex3f(temp_x, temp_y + number_of_tiles, 0)
            glEnd()

  
    height_quads = 50.0
    base_quads = -0.1

    
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(-central_position_grid, -central_position_grid, base_quads)
    glVertex3f(-central_position_grid, -central_position_grid, height_quads)
    glVertex3f(-central_position_grid, central_position_grid, height_quads)
    glVertex3f(-central_position_grid, central_position_grid, base_quads)
    glEnd()

    
    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(central_position_grid, -central_position_grid, base_quads)
    glVertex3f(central_position_grid, -central_position_grid, height_quads)
    glVertex3f(central_position_grid, central_position_grid, height_quads)
    glVertex3f(central_position_grid, central_position_grid, base_quads)
    glEnd()

   
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(-central_position_grid, -central_position_grid, base_quads)
    glVertex3f(-central_position_grid, -central_position_grid, height_quads)
    glVertex3f(central_position_grid, -central_position_grid, height_quads)
    glVertex3f(central_position_grid, -central_position_grid, base_quads)
    glEnd()

   
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(-central_position_grid, central_position_grid, base_quads)
    glVertex3f(-central_position_grid, central_position_grid, height_quads)
    glVertex3f(central_position_grid, central_position_grid, height_quads)
    glVertex3f(central_position_grid, central_position_grid, base_quads)
    glEnd()
        
        
def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    camera_functionality()
    draw_grid()
    draw_player_shape()
    draw_enemy_shape()
    draw_bullet_pallents()
    if not game_stopped:
        draw_text(10, 680, f"Score: {score_card}")
        draw_text(10, 660, f"Missed Bullets: {total_missed_bullets}")
        draw_text(10, 640, f"Player Health: {player_health_bar}")
        
    if game_stopped:
        draw_text(400, 400, "Game Over!")
        draw_text(400, 380, "Press 'R' to Restart")
        draw_text(400, 360, f"Your Final score is {score_card}")
    glutSwapBuffers()
    
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Bullet Frenzy")

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(animate)

    glEnable(GL_DEPTH_TEST)
    glutMainLoop()


if __name__ == "__main__":
    main()
        
        
    
    
    

    
    
    