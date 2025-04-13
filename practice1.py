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
    """