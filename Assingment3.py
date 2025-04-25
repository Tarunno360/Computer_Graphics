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

player_position_3d= (0, 0, 100)  # Player position in 3D space
total_enemy=[] # List of enemies

total_enemy = []
enemy_initial_speed=0.5

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
        bullet['pos'][0] += dx
        bullet['pos'][1] += dy
        if abs(bullet['pos'][0]) > GRID_LENGTH or abs(bullet['pos'][1]) > GRID_LENGTH:
            bullets_hitting_boundary += 1
        else:
            new_bullets_arr.append(bullet)
    bullets = new_bullets_arr
def update_movement_enemy():
    global enemies, score, player_life, game_over
    for bullet in bullets[:]:
        for enemy in total_enemy:
            if math.hypot(bullet['pos'][0]-enemy['pos'][0], bullet['pos'][1]-enemy['pos'][1]) < 25:
                score += 1
                bullets.remove(bullet)
                enemy['pos'] = [random.uniform(-GRID_LENGTH+50, GRID_LENGTH-50),
                                random.uniform(-GRID_LENGTH+50, GRID_LENGTH-50), 0]
                break
    for enemy in enemies:
        ex, ey, _ = enemy['pos']
        dx, dy = player_position_3d[0] - ex, player_position_3d[1] - ey
        distance = math.hypot(dx, dy)
        if distance:
            enemy['pos'][0] += enemy_initial_speed * (dx / distance)
            enemy['pos'][1] += enemy_initial_speed * (dy / distance)
        if math.hypot(dx, dy) < 40:
            player_life -= 1
            enemy['pos'] = [random.uniform(-GRID_LENGTH+50, GRID_LENGTH-50),
                            random.uniform(-GRID_LENGTH+50, GRID_LENGTH-50), 0]
            if player_life <= 0:
                game_over = True
    
def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    # # Move forward (W key)
    # if key == b'w':  

    # # Move backward (S key)
    # if key == b's':

    # # Rotate gun left (A key)
    # if key == b'a':

    # # Rotate gun right (D key)
    # if key == b'd':

    # # Toggle cheat mode (C key)
    # if key == b'c':

    # # Toggle cheat vision (V key)
    # if key == b'v':

    # # Reset the game if R key is pressed
    # if key == b'r':


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos
    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    # if key == GLUT_KEY_UP:

    # # Move camera down (DOWN arrow key)
    # if key == GLUT_KEY_DOWN:

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x -= 1  # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x += 1  # Small angle increment for smooth movement

    camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a bullet
        # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        # # Right mouse button toggles camera tracking mode
        # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:


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

    # Extract camera position and look-at target
    x, y, z = camera_pos
    # Position the camera and set its orientation
    gluLookAt(x, y, z,  # Camera position
              0, 0, 0,  # Look-at target
              0, 0, 1)  # Up vector (z-axis)


def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
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
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()