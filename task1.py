from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Window dimensions
W_Width, W_Height = 500, 500
raindrops = []
for i in range(100):  # Adjust the number of raindrops generated each time
        x = random.uniform(0, W_Width)
        y = random.randint(W_Height//2, W_Height)
        raindrops.append((x, y))
# raindrops = [(random.uniform(0, W_Width), random.uniform(0, W_Height)) for _ in range(100)]
rain_angle = 90  # Angle in degrees, default to 90 (vertical)
background_color = 0.0  # 0.0 (night) to 1.0 (day)

def draw_house():
    # Center coordinates
    center_x = W_Width / 2
    center_y = W_Height / 2

    # Draw the roof
    glBegin(GL_TRIANGLES) 
    glColor3f(1.0, 0.0, 1.0)  # Roof color
    glVertex2f(center_x - 100, center_y)
    glVertex2f(center_x + 100, center_y)
    glVertex2f(center_x, center_y + 100)
    glEnd()
    
    # Draw the body using two triangles
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 1.0)  # Body color
    glVertex2f(center_x - 100, center_y - 100)
    glVertex2f(center_x + 100, center_y - 100)
    glVertex2f(center_x + 100, center_y)
    
    glVertex2f(center_x - 100, center_y - 100)
    glVertex2f(center_x - 100, center_y)
    glVertex2f(center_x + 100, center_y)
    glEnd()

    # Draw the door
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.25, 0.0)  # Door color
    glVertex2f(center_x - 25, center_y - 100)
    glVertex2f(center_x + 25, center_y - 100)
    glVertex2f(center_x + 25, center_y - 50)
    glVertex2f(center_x - 25, center_y - 50)
    glEnd()

    # Draw the window
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)  # Window color
    glVertex2f(center_x + 50, center_y - 50)
    glVertex2f(center_x + 100, center_y - 50)
    glVertex2f(center_x + 100, center_y)
    glVertex2f(center_x + 50, center_y)
    glEnd()

def draw_rain():
    global raindrops
    glBegin(GL_LINES)
    for i, (x, y) in enumerate(raindrops):
        if i % 2 == 0:
            glColor3f(0.0, 0.0, 1.0)  # Blue color
        else:
            glColor3f(1.0, 1.0, 1.0)  # White color
        glVertex2f(x, y)
        glVertex2f(x + math.cos(math.radians(rain_angle)) * 30, y - math.sin(math.radians(rain_angle)) * 30)
    glEnd()

def update_rain():
    global raindrops
    new_raindrops = []
    for x, y in raindrops:
        y -= math.sin(math.radians(rain_angle)) * 10
        x += math.cos(math.radians(rain_angle)) * 10
        if y < 0 or x < 0 or x > W_Width:
            y = W_Height
            x = random.randint(0, W_Width)
        new_raindrops.append((x, y))
    raindrops = new_raindrops
    glutPostRedisplay()
    # glutTimerFunc(50, update_rain, 0)  # Adjust the interval here to control the frequency of raindrop updates
def animate():
    update_rain()
    glutPostRedisplay()
def draw_horizon():
    # Draw the horizon line
    glColor3f(0.0, 0.5, 0.0)  # Green color for trees
    glBegin(GL_LINES)
    glVertex2f(0, 250)
    glVertex2f(W_Width, 250)
    glEnd()

    # Draw some trees below the horizon line
    for i in range(0, W_Width, 50):
        glBegin(GL_TRIANGLES)
        glVertex2f(i, 250)
        glVertex2f(i + 25, 250)
        glVertex2f(i + 12.5, 300)
        glEnd()

def draw_sky_and_ground():
    # Draw the sky
    glBegin(GL_QUADS)
    glColor3f(background_color, background_color, background_color)  # Sky color
    glVertex2f(0, W_Height)
    glVertex2f(W_Width, W_Height)
    glVertex2f(W_Width, 250)
    glVertex2f(0, 250)
    glEnd()

    # Draw the ground
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.5, 0.0)  # Ground color
    glVertex2f(0, 250)
    glVertex2f(W_Width, 250)
    glVertex2f(W_Width, 0)
    glVertex2f(0, 0)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_sky_and_ground()
    draw_horizon()
    draw_house()
    draw_rain()
    glutSwapBuffers()

def keyboard(key, x, y):
    global background_color
    key = key.decode("utf-8")
    if key == 'd':
        background_color = min(1.0, background_color + 0.1)
    elif key == 'n':
        background_color = max(0.0, background_color - 0.1)
    glutPostRedisplay()

def special_keys(key, x, y):
    global rain_angle
    if key == GLUT_KEY_LEFT:
        rain_angle = min(135, rain_angle + 15)
    elif key == GLUT_KEY_RIGHT:
        rain_angle = max(45, rain_angle - 15)
    glutPostRedisplay()

def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, W_Width, 0, W_Height)
    # glutTimerFunc(50, update_rain, 0)
glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(W_Width, W_Height)
glutCreateWindow("House with Rain")
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_keys)
glutIdleFunc(animate)
glutMainLoop()