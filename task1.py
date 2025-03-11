from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

W_Width, W_Height = 500, 500
raindrops = []

def generate_raindrops():
    global raindrops
    raindrops = []
    for _ in range(100):
        x = random.uniform(-W_Width, 2 * W_Width)  
        y = random.uniform(W_Height, 1.5 * W_Height) 
        raindrops.append((x, y))

generate_raindrops()

rain_angle = 90 
background_color = 0.0  

def draw_house():
    center_x = W_Width / 2
    center_y = W_Height / 2

    # Roof here
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 1.0)
    glVertex2f(center_x - 100, center_y)
    glVertex2f(center_x + 100, center_y)
    glVertex2f(center_x, center_y + 100)
    glEnd()
    #body here
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 1.0)  

    glVertex2f(center_x - 100, center_y - 100) 
    glVertex2f(center_x + 100, center_y - 100)  
    glVertex2f(center_x + 100, center_y)        

    glVertex2f(center_x - 100, center_y - 100)  
    glVertex2f(center_x - 100, center_y)        
    glVertex2f(center_x + 100, center_y)        

    glEnd()

    # Door
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.25, 0.0)
    glVertex2f(center_x - 25, center_y - 100)
    glVertex2f(center_x + 25, center_y - 100)
    glVertex2f(center_x + 25, center_y - 50)
    glVertex2f(center_x - 25, center_y - 50)
    glEnd()

    # Window
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(center_x + 40, center_y - 50)
    glVertex2f(center_x + 90, center_y - 50)
    glVertex2f(center_x + 90, center_y-10)
    glVertex2f(center_x + 40, center_y-10)
    glEnd()

def draw_rain():
    global raindrops
    glBegin(GL_LINES)
    for i, (x, y) in enumerate(raindrops):
        glColor3f(0.0, 0.0, 1.0) if i % 2 == 0 else glColor3f(1.0, 1.0, 1.0)
        glVertex2f(x, y)
        glVertex2f(x + math.cos(math.radians(rain_angle)) * 10, y - math.sin(math.radians(rain_angle)) * 10)
    glEnd()

def update_rain():
    global raindrops
    new_raindrops = []
    for x, y in raindrops:
        y -= math.sin(math.radians(rain_angle)) * 10
        x += math.cos(math.radians(rain_angle)) * 10

        if y < 0 or x < -50 or x > W_Width + 50:
            x = random.uniform(-W_Width, 2 * W_Width)  
            y = random.uniform(W_Height, 1.5 * W_Height)  

        new_raindrops.append((x, y))
    raindrops = new_raindrops
    glutPostRedisplay()

def animate():
    update_rain()
    glutPostRedisplay()

def draw_horizon():
    glColor3f(0.0, 0.5, 0.0)
    glBegin(GL_LINES)
    glVertex2f(0, 250)
    glVertex2f(W_Width, 250)
    glEnd()

    # Draw trees
    for i in range(0, W_Width, 50):
        glBegin(GL_TRIANGLES)
        glVertex2f(i, 250)
        glVertex2f(i + 25, 250)
        glVertex2f(i + 12.5, 300)
        glEnd()

def draw_sky_and_ground():
    glBegin(GL_QUADS)
    glColor3f(background_color, background_color, background_color)
    glVertex2f(0, W_Height)
    glVertex2f(W_Width, W_Height)
    glVertex2f(W_Width, 250)
    glVertex2f(0, 250)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(0.0, 0.5, 0.0)
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
        rain_angle = min(105, rain_angle + 5)
    elif key == GLUT_KEY_RIGHT:
        rain_angle = max(75, rain_angle - 5)
    glutPostRedisplay()

def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, W_Width, 0, W_Height)

#------------------DRIVER CODE------------------
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
