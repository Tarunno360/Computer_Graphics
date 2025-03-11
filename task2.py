from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

width = 800
height = 800
dot_points=[]
speed=1
blink_button=False
pause_button_implementation=False
blink_state=False

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
            glColor3f(p['color'][0], p['color'][1], p['color'][2])
            glVertex2f(p['x'], p['y'])
    glEnd()

def mouse_listener(button, state, x, y):
    global pause_button_implementation,blink_button,blink_state
    y=height-y
    if pause_button_implementation==False:
        
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            blink_button = not blink_button 
            if blink_button:
                blink_screen()
            else:
                blink_state=False
                glutDisplayFunc(display)
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            dot_points.append({
                'x': x, 'y': y,
                'dx': random.choice([-1, 1]), 'dy': random.choice([-1, 1]),
                'color': (random.random(), random.random(), random.random())
            })
        glutPostRedisplay()

def update_points():
    global speed,pause_button_implementation
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
    global pause_button_implementation, speed
    key = key.decode('utf-8')
    if key == ' ':
        pause_button_implementation = not pause_button_implementation
        if pause_button_implementation:
            glutIdleFunc(None)  
        else:
            glutIdleFunc(update_points)  
    glutPostRedisplay()
    
def special_key_listener(key, x, y):
    global speed,pause_button_implementation
    if pause_button_implementation==False:
        if key == GLUT_KEY_UP:
            speed+=1
        elif key == GLUT_KEY_DOWN:
            speed= max(1, speed-1)
        glutPostRedisplay()
 
def blink_screen():
    global blink_state, blink_button
    if blink_button:
        blink_state = not blink_state  
        glutPostRedisplay()
        glutTimerFunc(500, lambda _: blink_screen(), 0)     

def display():
    global pause_button_implementation, blink_state
    glClear(GL_COLOR_BUFFER_BIT)

    if blink_state:
        glColor3f(0.0, 0.0, 0.0)  
        glRectf(0, 0, width, height)
    else:
        draw_box()
        draw_points()

    glutSwapBuffers()
    

def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
#------------------Driver Code-------------------
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