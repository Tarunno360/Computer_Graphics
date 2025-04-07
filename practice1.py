""" from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

width, height = 800, 600
points = []
speed = 1
blink = False
frozen = False

def draw_box():
    glColor3f(1, 1, 1)
    glBegin(GL_LINE_LOOP)
    glVertex2f(50, 50)
    glVertex2f(width - 50, 50)
    glVertex2f(width - 50, height - 50)
    glVertex2f(50, height - 50)
    glEnd()

def draw_points():
    if blink:
        if (glutGet(GLUT_ELAPSED_TIME) // 500) % 2 == 0:
            return
    
    glPointSize(5)
    glBegin(GL_POINTS)
    for p in points:
        glColor3f(p['color'][0], p['color'][1], p['color'][2])
        glVertex2f(p['x'], p['y'])
    glEnd()

def update_points():
    if frozen:
        return
    for p in points:
        p['x'] += p['dx'] * speed
        p['y'] += p['dy'] * speed
        
        if p['x'] <= 50 or p['x'] >= width - 50:
            p['dx'] *= -1
        if p['y'] <= 50 or p['y'] >= height - 50:
            p['dy'] *= -1
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_box()
    draw_points()
    glutSwapBuffers()

def mouse_listener(button, state, x, y):
    global blink
    y = height - y
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        points.append({
            'x': x, 'y': y,
            'dx': random.choice([-1, 1]), 'dy': random.choice([-1, 1]),
            'color': (random.random(), random.random(), random.random())
        })
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blink = not blink
    glutPostRedisplay()

def keyboard_listener(key, x, y):
    global frozen
    if key == b' ':
        frozen = not frozen

def special_key_listener(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
        speed += 1
    elif key == GLUT_KEY_DOWN:
        speed = max(1, speed - 1)
#using glutInit to initialize the window
def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)

glutInit()
glutInitWindowSize(width, height)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Amazing Box")
init()
glutDisplayFunc(display)
glutIdleFunc(update_points)
glutMouseFunc(mouse_listener)
glutKeyboardFunc(keyboard_listener)
glutSpecialFunc(special_key_listener)
glutMainLoop() """