from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


window_width = 500 #width
window_height = 500 #height

raindrops = [] 
day=False
current_x_position = 0 #for raindrop rotation 
background_color = [0.0, 0.0, 0.0] 
target_color = [0.0, 0.0, 0.0]  # desired background color
color_change_speed = 0.1 

def draw_line(x1, y1, x2, y2):

    if day==False:
        glColor3f(1.0, 0.0, 0.0)  
    elif day==True:
        glColor3f(0,0,0)

    #creating formats
    glBegin(GL_LINES) #start line
    glVertex2f(x1, y1) #first point's format
    glVertex2f(x2, y2) #second point's format
    glEnd() #end



def draw_rain():
    glColor3f(0.0, 0.0, 1.0)  # rain's color
    glLineWidth(3.0)          #width of the rain

    glBegin(GL_LINES)
    for x, y in raindrops:
        glVertex2f(x - current_x_position, y) #rotation handling 2
        glVertex2f(x + current_x_position, y - 10) #rotation handling 3,length of raindrop
    glEnd()



def generate_rain():
    x = random.randint(50, 500)  #values defines the area of rainfall
    y = 500                      #from where the rain is generated
    raindrops.append((x, y))     #appended to global raindrop's array 



def animate_rain():
    for i in range(len(raindrops)):
        x, y = raindrops[i]
        #y -= random.uniform(0.1, 0.4) 
        y-= 10
        raindrops[i] = (x, y)

    raindrops[:] = [raindrop for raindrop in raindrops if raindrop[1] >=110] #height 110



def change_background_color():
    global background_color, target_color

    for i in range(3):
        if background_color[i] < target_color[i]:
            background_color[i] += color_change_speed
        elif background_color[i] > target_color[i]:
            background_color[i] -= color_change_speed


def iterate():
    glViewport(0, 0, window_width, window_height) 
    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity() 
    glOrtho(0.0, window_width, 0.0, window_height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(*background_color, 0.0) #turns all black


def house():
    #house's body
    draw_line(100, 100, 300, 100)
    draw_line(100, 100, 100, 250)
    draw_line(100, 250, 300, 250)
    draw_line(300, 100, 300, 250)
    glColor3f(1,0,0)   
    #house's roof
    draw_line(100, 250, 200, 300)
    draw_line(300, 250, 200, 300)

    #house's door
    draw_line(140, 100, 140, 175)   
    draw_line(190, 100, 190, 175)
    draw_line(140, 175, 190, 175)

    #house's window
    draw_line(230, 150, 230, 190)
    draw_line(230, 190, 270, 190)
    draw_line(270, 190, 270, 150)
    draw_line(270, 150, 230, 150)



def showScreen(): #calling all functions

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_rain()
    animate_rain()
    generate_rain()
    change_background_color()
    house()
    glutSwapBuffers()



def specialKeyListener(key, x, y):
    
    global current_x_position

    if key == GLUT_KEY_RIGHT:
        current_x_position += 1 #raindrop's rotation handling 4
    elif key == GLUT_KEY_LEFT:
        current_x_position -= 1 #raindrop's rotation handling 5

    glutPostRedisplay() 

def keyboardListener(key, x, y):
    global target_color,day

    if key == b'd':

        if day==False:
            target_color = [1, 1, 1]  # desired color white for day
            day= True

    elif key == b'n':
        if day==True:
            target_color = [0.0, 0.0, 0.0]  #desired color black for night
            day=False
    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(0, 1)  #output window position
wind = glutCreateWindow(b"Task 1: Building a House in Rainfall")
glutDisplayFunc(showScreen)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)
glutIdleFunc(showScreen) #function will be repeatedly called by GLUT during idle time, allowing you to continuously update the rendering of your scene. This is essential for animations and real-time graphics.
glutMainLoop()