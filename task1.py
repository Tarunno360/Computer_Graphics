from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

raindrops = [(random.uniform(-1, 1), random.uniform(0, 1)) for _ in range(100)]
rain_direction = 0.0
background_color = 0.0  # 0.0 (night) to 1.0 (day)

def draw_house():
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_TRIANGLES)  # Roof
    glVertex2f(-0.3, 0.1)
    glVertex2f(0.3, 0.1)
    glVertex2f(0.0, 0.4)
    glEnd()
    
    glBegin(GL_QUADS)  # Body
    glVertex2f(-0.3, -0.3)
    glVertex2f(0.3, -0.3)
    glVertex2f(0.3, 0.1)
    glVertex2f(-0.3, 0.1)
    glEnd()

def draw_rain():
    global raindrops
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    for i in range(len(raindrops)):
        x, y = raindrops[i]
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
    glutPostRedisplay()
    glutTimerFunc(50, update_rain, 0)

def display():
    glClearColor(background_color, background_color, background_color, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
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
        rain_direction -= 0.01
    elif key == GLUT_KEY_RIGHT:
        rain_direction += 0.01
    glutPostRedisplay()

def init():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    
    # Define window size before using it
    W_Width, W_Height = 500, 500  
    glutInitWindowSize(W_Width, W_Height)
    
    glutCreateWindow("House with Rain")  # Removed `b`
    glOrtho(-1, 1, -1, 1, -1, 1)
    
    # Register callback functions
    glutDisplayFunc(display)  
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutTimerFunc(50, update_rain, 0)

    # Ensure a redraw is requested at startup
    glutPostRedisplay()

    glutMainLoop()

# if __name__ == "__main__":
    # main()


glutInit()
init()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color

# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"")


glutDisplayFunc(display)	#display callback function
glutIdleFunc(animate)	#what you want to do in the idle time (when no drawing is o)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()
