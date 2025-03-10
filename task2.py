from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

width = 800
height = 800
dot_points=[]
speed=0.01
blink=False
Frozen_screen=False

def draw_box():
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(10, 10)
    glVertex2f(width-10, 10)
    glVertex2f(width-10, height-10)
    glVertex2f(10, height-10)
    glEnd()

def draw_points():
    glPointSize(6)
    glBegin(GL_POINTS)
    for p in dot_points:
        glColor3f(p['color'][0], p['color'][1], p['color'][2])
        glVertex2f(p['x'], p['y'])
    glEnd()

def moouse_listener(button, state, x, y):
    global blink
    y=height-y
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        dot_points.append({
            'x': x, 'y': y,
            'dx': random.choice([-1, 1]), 'dy': random.choice([-1, 1]),
            'color': (random.random(), random.random(), random.random())
        })
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blink = not blink
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_box()
    draw_points()
    glutSwapBuffers()
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
# glutIdleFunc(update_points)
# glutMouseFunc(mouse_listener)
# glutKeyboardFunc(keyboard_listener)
# glutSpecialFunc(special_key_listener)
glutMainLoop()