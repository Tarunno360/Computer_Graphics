from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

raindrops = [(random.uniform(-1, 1), random.uniform(0.5, 1)) for _ in range(100)]
rain_direction = 0.0
background_color = 0.0  # 0.0 (night) to 1.0 (day)

def draw_house():
    glBegin(GL_TRIANGLES) 
    glColor3f(1.0, 0.0, 1.0)  # Roof
    glVertex2f(-0.3, 0.1)
    glVertex2f(0.3, 0.1)
    glVertex2f(0.0, 0.4)
    glEnd()
    
    # Draw the body using two triangles
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 1.0)  # Body color
    glVertex2f(-0.3, -0.3)
    glVertex2f(0.3, -0.3)
    glVertex2f(0.3, 0.1)
    
    glVertex2f(-0.3, -0.3)
    glVertex2f(-0.3, 0.1)
    glVertex2f(0.3, 0.1)
    glEnd()

    # Draw the door
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.25, 0.0)  # Door color
    glVertex2f(-0.05, -0.3)
    glVertex2f(0.05, -0.3)
    glVertex2f(0.05, -0.1)
    glVertex2f(-0.05, -0.1)
    glEnd()

    # Draw the window
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)  # Window color
    glVertex2f(0.1, -0.1)
    glVertex2f(0.2, -0.1)
    glVertex2f(0.2, 0.0)
    glVertex2f(0.1, 0.0)
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
        glVertex2f(x + rain_direction, y - 0.05)
    glEnd()

def update_rain(value):
    global raindrops
    new_raindrops = []
    for x, y in raindrops:
        y -= 0.02
        x += rain_direction * 0.02
        if y < -1:
            y = 1
            x = random.uniform(-1, 1)
        new_raindrops.append((x, y))
    raindrops = new_raindrops
    generate_rain()
    glutPostRedisplay()
    glutTimerFunc(50, update_rain, 0)  # Adjust the interval here to control the frequency of raindrop updates

def generate_rain():
    global raindrops
    for _ in range(5):  # Adjust the number of raindrops generated each time
        x = random.uniform(-1, 1)
        y = 1  # Generate raindrops at the top of the screen
        raindrops.append((x, y))

def draw_horizon():
    # Draw the horizon line
    glColor3f(0.0, 0.5, 0.0)  # Green color for trees
    glBegin(GL_LINES)
    glVertex2f(-1.0, 0.0)
    glVertex2f(1.0, 0.0)
    glEnd()

    # Draw some trees below the horizon line
    for i in range(-10, 11, 2):
        glBegin(GL_TRIANGLES)
        glVertex2f(i * 0.1, 0.0)
        glVertex2f((i + 1) * 0.1, 0.0)
        glVertex2f((i + 0.5) * 0.1, 0.2)
        glEnd()

def draw_sky_and_ground():
    # Draw the sky
    glBegin(GL_QUADS)
    glColor3f(background_color, background_color, background_color)  # Sky color
    glVertex2f(-1.0, 1.0)
    glVertex2f(1.0, 1.0)
    glVertex2f(1.0, 0.0)
    glVertex2f(-1.0, 0.0)
    glEnd()

    # Draw the ground
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.5, 0.0)  # Ground color
    glVertex2f(-1.0, 0.0)
    glVertex2f(1.0, 0.0)
    glVertex2f(1.0, -1.0)
    glVertex2f(-1.0, -1.0)
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
    global rain_direction
    if key == GLUT_KEY_LEFT:
        rain_direction += -0.02
    elif key == GLUT_KEY_RIGHT:
        rain_direction += 0.02
    glutPostRedisplay()

def init():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    W_Width, W_Height = 500, 500  
    glutInitWindowSize(W_Width, W_Height)
    glutCreateWindow("House with Rain")
    glOrtho(-1, 1, -1, 1, -1, 1)
    glutDisplayFunc(display)  
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutTimerFunc(50, update_rain, 0)  # Adjust the interval here to control the frequency of raindrop updates
    glutIdleFunc(display)  # Ensure continuous animation
    glutMainLoop()

if __name__ == "__main__":
    init()