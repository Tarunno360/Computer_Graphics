from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

width = 800
height = 800
dot_points=[]
speed=1
blink=False
pause_button_implementation=False

def draw_box():
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(10, 10)
    glVertex2f(width-10, 10)
    glVertex2f(width-10, height-10)
    glVertex2f(10, height-10)
    glEnd()

def draw_points():
    global pause_button_implementation
    if pause_button_implementation==False:
        glPointSize(6)
        glBegin(GL_POINTS)
        for p in dot_points:
            if blink==True and (glutGet(GLUT_ELAPSED_TIME)//500)%2==0:
                glColor3f(0, 0, 0)
            else:
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

def update_points():
    if pause_button_implementation==False:
        for i in dot_points:
            i['x']+=i['dx']*speed
            i['y']+=i['dy']*speed
            if i['x']<=10 or i['x']>=width-10:
                i['dx']*= -1
            if i['y']<=10 or i['y']>=height-10:
                i['dy']*= -1
        glutPostRedisplay()
        
def keyboard_listener(key, x, y):
    global pause_button_implementation,speed
    key = key.decode('utf-8')
    if pause_button_implementation==True:
        if key == ' ':
            pause_button_implementation= False
    else:
        if key == ' ':
            pause_button_implementation= True
    glutPostWindowRedisplay()
    
def special_key_listener(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
        speed+=0.01
    elif key == GLUT_KEY_DOWN:
        speed-=0.01
    glutPostRedisplay()
    
def mouse_listener(button, state, x, y):
    global blink
    y=height-y
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        dot_points.append({
            'x': x, 'y': y,
            'dx': random.choice([-1, 1]), 'dy': random.choice([-1, 1]),
            'color': (random.random(), random.random(), random.random())
        })
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blink = False
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
glutIdleFunc(update_points)
glutMouseFunc(mouse_listener)
glutKeyboardFunc(keyboard_listener)
glutSpecialFunc(special_key_listener)
glutMainLoop()