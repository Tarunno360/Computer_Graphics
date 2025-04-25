from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18

# Camera-related variables
camera_pos = (0,500,500)

fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines
rand_var = 423
finished_game = False
current_game_score = 0


player_initial_velocity = 5
player_position_3d= (0, 0, 100)  
player_health_bar=3

total_enemy=[] # List of enemies
initial_gun_angle = 0
camera_angle = 0
cheat_buttion = False
cheat_look=False
first_person_mode = False

total_enemy = []
total_enemy_number = 5
enemy_initial_speed=0.5

gun_angle = 0

bullets=[] # List of bullets
bullets_hitting_boundary=0
bullet_velocity=10
#-----------draw part----------------
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_grid():
    size_step=50
    for i in range(-GRID_LENGTH, GRID_LENGTH , size_step):
        for j in range(-GRID_LENGTH, GRID_LENGTH, size_step):
            if (i + j) % 100 == 0:
                glColor3f(0.7, 0.5, 0.95)
            else:
                glColor3f(1, 1, 1)
            glBegin(GL_QUADS)
            glVertex3f(i, j, 0)
            glVertex3f(i + size_step, j, 0)
            glVertex3f(i + size_step, j + size_step, 0)
            glVertex3f(i,j+ size_step, 0)
            glEnd()
    boundary_height = 50
    boundary_weight = 10
    #boundary colors
    glColor3f(1, 1, 1) 
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH - boundary_weight, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH - boundary_weight, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, boundary_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, boundary_height)
    glEnd()
    
    glColor3f(0,1,1)
    glBegin(GL_QUADS)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH + boundary_weight, GRID_LENGTH, boundary_height)
    glVertex3f(GRID_LENGTH + boundary_weight, -GRID_LENGTH, boundary_height)
    glEnd()
    
    glColor3f(0,0,1) 
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH + boundary_weight,boundary_height )
    glVertex3f(-GRID_LENGTH, GRID_LENGTH + boundary_weight,boundary_height)
    glEnd()
    
    glColor3f(0, 1, 0) 
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH - boundary_weight,boundary_height )
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH - boundary_weight,boundary_height )
    glEnd()

def draw_player():
    
    glPushMatrix() 
    glTranslatef(player_position_3d[0], player_position_3d[1], player_position_3d[2]+10)
    glPushMatrix()  # player body
    glScalef(1, 0.5, 1.5)  # Scale the player body
    glColor3f(0, 0.92, 0) 
    glutSolidCube(30)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 0, 35)
    glColor3f(0.0, 0.0, 0.0)
    gluSphere(gluNewQuadric(), 10, 10, 10)
    glPopMatrix()

    # Left hand (perpendicular)
    glPushMatrix()
    glTranslatef(-25, 0, 15)
    glRotatef(90, 0, 1, 0)
    glColor3f(1.0, 0.8, 0.6)  # Skin color
    gluCylinder(gluNewQuadric(), 3, 3, 20, 10, 10)
    glPopMatrix()

    # Right hand (perpendicular)
    glPushMatrix()
    glTranslatef(25, 0, 15)
    glRotatef(-90, 0, 1, 0)
    glColor3f(1.0, 0.8, 0.6)  # Skin color
    gluCylinder(gluNewQuadric(), 3, 3, 20, 10, 10)
    glPopMatrix()

    # Left leg
    glPushMatrix()
    glTranslatef(-8, 0, -15)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.0, 0.0, 1.0)  # Blue
    gluCylinder(gluNewQuadric(), 4, 4, 25, 10, 10)
    glPopMatrix()

    # Right leg
    glPushMatrix()
    glTranslatef(8, 0, -15)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.0, 0.0, 1.0)  # Blue
    gluCylinder(gluNewQuadric(), 4, 4, 25, 10, 10)
    glPopMatrix()

    # Gun in the middle, pointing outward from chest
    glPushMatrix()
    glTranslatef(0, 20, 20)  # Between the arms
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.75, 0.75, 0.75)  # Silver
    gluCylinder(gluNewQuadric(), 3, 3, 40, 10, 10)
    glPopMatrix()

    glPopMatrix()
    
def draw_emeny(e):
    glPushMatrix()
    glTranslatef(e[0], e[1], e[2])
    
    glColor3f(1, 0, 0)  # Red color for the enemy
    gluSphere(gluNewQuadric(), 10, 10, 10)  # Draw a sphere for the enemy
    
    glTranslatef(0,0,30)
    glColor3f(0, 0, 0) 
    gluSphere(gluNewQuadric(), 10, 20, 20)
    glPopMatrix()
    # Draw a sphere for the enemy's head
def draw_bullet_pallet(bullets):
    glPushMatrix()
    glTranslatef(*bullets['position'])
    glColor3f(1, 0, 0)  # Red color for the bullet 
    glutSolidCube(10)  # Draw a bullet as a cube
    glPopMatrix()
    
def update_bullet_pallets():
    global bullets, bullets_hitting_boundary
    new_bullets_arr = []
    for bullet in bullets:
        dx = bullet_velocity * math.cos(math.radians(bullet['angle']))
        dy = bullet_velocity * math.sin(math.radians(bullet['angle']))
        bullet['position'][0] += dx
        bullet['position'][1] += dy
        if abs(bullet['position'][0]) > GRID_LENGTH or abs(bullet['position'][1]) > GRID_LENGTH:
            bullets_hitting_boundary += 1
        else:
            new_bullets_arr.append(bullet)
    bullets = new_bullets_arr
    
def update_movement_enemy():
    global total_enemy, current_game_score, player_health_bar, finished_game
    for bullet in bullets[:]:
        for enemy in total_enemy:
            if math.hypot(bullet['position'][0]-enemy['position'][0], bullet['position'][1]-enemy['position'][1]) < 25:
                current_game_score += 1
                bullets.remove(bullet)
                enemy['position'] = [random.uniform(-GRID_LENGTH+50, GRID_LENGTH-50),
                                random.uniform(-GRID_LENGTH+50, GRID_LENGTH-50), 0]
                break
    for enemy in total_enemy:
        ex, ey, _ = enemy['position']
        dx, dy = player_position_3d[0] - ex, player_position_3d[1] - ey
        distance = math.hypot(dx, dy)
        if distance:
            enemy['position'][0] += enemy_initial_speed * (dx / distance)
            enemy['position'][1] += enemy_initial_speed * (dy / distance)
        if math.hypot(dx, dy) < 40:
            player_health_bar -= 1
            enemy['position'] = [random.uniform(-GRID_LENGTH+50, GRID_LENGTH-50),
                            random.uniform(-GRID_LENGTH+50, GRID_LENGTH-50), 0]
            if player_health_bar <= 0:
                finished_game = True

def cheat_code_fire_logic():
    global gun_angle
    gun_angle = (gun_angle + 5) % 360
    for enemy in total_enemy:
        dx = enemy['position'][0] - player_position_3d[0]
        dy = enemy['position'][1] - player_position_3d[1]
        angle_to_enemy = math.degrees(math.atan2(dy, dx))
        diff = abs((angle_to_enemy - gun_angle + 180) % 360 - 180)
        if diff < 10:
            bullet_fire_logic()
            break

def bullet_fire_logic():
    start_x = player_position_3d[0] + 25 + 40 * math.cos(math.radians(gun_angle))
    start_y = player_position_3d[1] + 40 * math.sin(math.radians(gun_angle))
    bullets.append({'position': [start_x, start_y, 0], 'angle': gun_angle})

def update_game_logic():
    if not finished_game:
        update_bullet_pallets()
        update_movement_enemy()
        if cheat_buttion:
            cheat_code_fire_logic()
    glutPostRedisplay()

def reset_game():
    
    global player_position_3d, player_health_bar, total_enemy, finished_game, current_game_score,bullets
    player_position_3d = (0, 0, 100)  # Reset player position
    player_health_bar = 3  # Reset health bar
    total_enemy = []  # Reset enemies
    finished_game = False  # Reset game state
    current_game_score = 0  # Reset score
    bullets = []  # Reset bullets
    for i in range(total_enemy_number):
        ex = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        ey = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        total_enemy.append({'position': [ex, ey, 0], 'direction': 0})

def keyboardListener(key, x, y):
    global initial_gun_angle, player_position_3d, cheat_buttion, cheat_look, finished_game, player_initial_velocity
    if key == b'r':
        reset_game()
        player_initial_velocity = 5  # Reset speed after restarting
        return
    if finished_game:
        return
    if key == b'w':
        # Move forward with increased speed
        player_position_3d[0] += player_initial_velocity * math.cos(math.radians(gun_angle))
        player_position_3d[1] += player_initial_velocity * math.sin(math.radians(gun_angle))
        player_initial_velocity += 0.1  # Gradually increase speed when moving forward
    elif key == b's':
        # Move backward with increased speed
        player_position_3d[0] -= player_initial_velocity * math.cos(math.radians(gun_angle))
        player_position_3d[1] -= player_initial_velocity * math.sin(math.radians(gun_angle))
        player_initial_velocity += 0.1  # Gradually increase speed when moving backward
    elif key == b'a':
        gun_angle = (gun_angle + 5) % 360
    elif key == b'd':
        gun_angle = (gun_angle - 5) % 360
    elif key == b'c':
        cheat_buttion = not cheat_buttion
    elif key == b'v':
        cheat_look = not cheat_look
    glutPostRedisplay()


def specialKeyListener(key, x, y):
    
    global camera_pos, camera_angle

    if key == GLUT_KEY_UP:
        camera_pos[2] += 10  # Move camera up
    elif key == GLUT_KEY_DOWN:
        camera_pos[2] -= 10  # Move camera down
    elif key == GLUT_KEY_LEFT:
        camera_angle = (camera_angle + 5) % 360  # Orbit left
    elif key == GLUT_KEY_RIGHT:
        camera_angle = (camera_angle - 5) % 360  # Orbit right

    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global first_person_mode
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        bullet_fire_logic()
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person_mode = not first_person_mode  # Toggle view mode
    glutPostRedisplay()


def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    if first_person_mode:
        # First-person camera (gun-following view)
        eyeX, eyeY = player_position_3d[0], player_position_3d[1]
        eyeZ = 50
        centerX = eyeX + math.cos(math.radians(gun_angle)) * 100
        centerY = eyeY + math.sin(math.radians(gun_angle)) * 100
        centerZ = eyeZ
        gluLookAt(eyeX, eyeY, eyeZ, centerX, centerY, centerZ, 0, 0, 1)
    else:
        # Third-person orbiting camera around center (0, 0)
        radius = 500
        eyeX = radius * math.cos(math.radians(camera_angle))
        eyeY = radius * math.sin(math.radians(camera_angle))
        eyeZ = camera_pos[2]  # Keep using current height
        gluLookAt(eyeX, eyeY, eyeZ, 0, 0, 0, 0, 0, 1)


def idle():
    update_game_logic()  # Update game logic
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective
    draw_grid() 
    draw_player()  # Draw the player
    for i in total_enemy:
        draw_emeny(i)
        
    # Draw a random points
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Draw the grid (game floor)
    

    # Display game info text at a fixed screen position
    draw_text(10, 770, f"A Random Fixed Position Text")
    draw_text(10, 740, f"See how the position and variable change?: {rand_var}")

    #draw_shapes()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    glutCreateWindow(b"3D OpenGL Intro")  # Create the window
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically
    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()