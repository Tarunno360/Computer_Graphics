from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import random
import os

window_width = 800
window_height = 600
catcher_x = 380
catcher_width = 120
diamond_x = random.randint(100, 700)
diamond_y = 470
diamond_speed = 1
score = 0
game_over = False
paused = False
catcher_color = (1.0, 1.0, 1.0)
diamond_color = (random.uniform(0.7, 1.0), random.uniform(0.3, 1.0), random.uniform(0.9, 1.0))

def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()

def convert_to_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def convert_from_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    abs_dx = abs(dx)
    abs_dy = abs(dy)
    if abs_dx >= abs_dy:
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6

def draw_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    x1_zone0, y1_zone0 = convert_to_zone0(x1, y1, zone)
    x2_zone0, y2_zone0 = convert_to_zone0(x2, y2, zone)

    dx = x2_zone0 - x1_zone0
    dy = y2_zone0 - y1_zone0
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x1_zone0
    y = y1_zone0
    while x <= x2_zone0:
        real_x, real_y = convert_from_zone0(x, y, zone)
        draw_pixel(real_x, real_y)
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1

def draw_catcher():
    global catcher_color
    glColor3f(*catcher_color)
    
    catcher_height = 20 

    draw_line(catcher_x, 20, catcher_x + catcher_width, 20)

    draw_line(catcher_x, 20, catcher_x + 15, 20 + catcher_height)

    draw_line(catcher_x + catcher_width, 20, catcher_x + catcher_width - 15, 20 + catcher_height)


    draw_line(catcher_x + 15, 20 + catcher_height, catcher_x + catcher_width - 15, 20 + catcher_height)

def draw_diamond():
    glColor3f(*diamond_color)
    draw_line(diamond_x, diamond_y, diamond_x + 10, diamond_y + 10)
    draw_line(diamond_x + 10, diamond_y + 10, diamond_x, diamond_y + 20)
    draw_line(diamond_x, diamond_y + 20, diamond_x - 10, diamond_y + 10)
    draw_line(diamond_x - 10, diamond_y + 10, diamond_x, diamond_y)

def draw_rect_button(x, y, w, h, color):
    glColor3f(*color)
    draw_line(x, y, x + w, y)
    draw_line(x + w, y, x + w, y + h)
    draw_line(x + w, y + h, x, y + h)
    draw_line(x, y + h, x, y)


def draw_line_raw(x1, y1, x2, y2, color):
    glColor3f(*color)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def exit(x, y, color):
    draw_line_raw(x, y, x + 50, y - 50, color)
    draw_line_raw(x, y - 50, x + 50, y, color)

def restart(x, y, color):
    draw_line_raw(x, y, x + 50, y, color)
    draw_line_raw(x, y, x + 20, y + 25, color)
    draw_line_raw(x, y, x + 20, y - 25, color)
def pause_play(x, y, color):
    global paused
    if paused:
        # Play symbol
        draw_line_raw(x - 25, y + 25, x - 25, y - 25, color)
        draw_line_raw(x - 25, y + 25, x + 25, y, color)
        draw_line_raw(x - 25, y - 25, x + 25, y, color)
    else:
        # Pause symbol
        draw_line_raw(x - 20, y + 25, x - 20, y - 25, color)
        draw_line_raw(x + 20, y + 25, x + 20, y - 25, color)

buttons = {
    'R': {'x': 20, 'y': 570, 'w': 60, 'h': 60, 'func': restart, 'color': (0.2, 0.8, 1.0)},
    'P': {'x': window_width // 2 - 30, 'y': 570, 'w': 60, 'h': 60, 'func': pause_play, 'color': (1.0, 1.0, 0.2)},
    'Q': {'x': window_width - 80, 'y': 570, 'w': 60, 'h': 60, 'func': exit, 'color': (1.0, 0.2, 0.2)},
}

def draw_buttons():
    for key, btn in buttons.items():
        cx = btn['x'] + btn['w'] // 4
        cy = btn['y'] - btn['h'] // 2
        btn['func'](cx, cy, btn['color'])



def mouse_click(button, state, x, y):
    global game_over, paused, score, catcher_color

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        screen_y = window_height - y  # OpenGL Y flip
        for key, btn in buttons.items():
            if (btn['x'] <= x <= btn['x'] + btn['w']) and (btn['y'] - btn['h'] <= screen_y <= btn['y']):
                if key == 'R':
                    print("Starting Over!")
                    game_over = False
                    score = 0
                    catcher_color = (1.0, 1.0, 1.0)
                    reset_diamond()
                elif key == 'P':
                    paused = not paused
                    print("Game Paused:")
                elif key == 'Q':
                    print("Quiting Game... Final Score:", score)
                    os._exit(0)

def random_bright_color():
    r = random.uniform(0.5, 1.0)
    g = random.uniform(0.5, 1.0)
    b = random.uniform(0.5, 1.0)
    return r, g, b

def update(value):
    global diamond_y, diamond_x, diamond_speed, score, game_over, catcher_color
    if not game_over and not paused:
        diamond_y -= diamond_speed
        if diamond_y <= 40:
            if catcher_x <= diamond_x <= catcher_x + catcher_width:
                score += 1
                print("Score:", score)
                reset_diamond()
                diamond_speed += 0.2
            else:
                print("Game Over!Score:", score)
                catcher_color = (1.0, 0.0, 0.0)
                game_over = True
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def reset_diamond():
    global diamond_y, diamond_x, diamond_color
    diamond_y = 470
    diamond_x = random.randint(100, 700)
    diamond_color = random_bright_color() 
    
    
def special_keys(key, x, y):
    global catcher_x
    if not paused and not game_over:
        if key == GLUT_KEY_LEFT:
            catcher_x = max(catcher_x - 20, 0)
        elif key == GLUT_KEY_RIGHT:
            catcher_x = min(catcher_x + 20, window_width - catcher_width)

def keyboard(key, x, y):
    global game_over, score, catcher_color, paused
    key = key.decode("utf-8")
    if key == 'r': 
        print("Starting Over")
        game_over = False
        score = 0
        catcher_color = (1.0, 1.0, 1.0)
        reset_diamond()
    elif key == 'p':  
        paused = not paused
    elif key == 'q':
        print("Quiting Game..! Final Score:", score)
        sys.exit()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_buttons()
    draw_catcher()
    if not game_over:
        draw_diamond()
    glutSwapBuffers()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, window_width, 0, window_height)
    glPointSize(2)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow("Catch the Diamonds!")
    init()
    glutDisplayFunc(display)
    glutSpecialFunc(special_keys)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse_click)
    glutTimerFunc(0, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
