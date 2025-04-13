'''from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

Window_Width, Window_Height = 500, 700

diamond_pos_x, diamond_pos_y = random.uniform(50, 450), 650
basket_pos_x, basket_pos_y = 250,60
p_button_pos_x, p_button_pos_y = 250, 675
restart_button_pos_x, restart_button_pos_y = 0, 675
exit_button_pos_x, exit_button_pos_y = 450, 700
speed = 0.10
Total_score = 0
random_color = [random.uniform(0.7, 1.0), random.uniform(0.3, 1.0), random.uniform(0.9, 1.0)]
basket_colours_lst = [1, 1, 1]
play = True
Game_over = False
Total_score = 0


def OpenGL_cordinate(x, y):
    global Window_Width, Window_Height
    openGL_Cordinate_X = x
    openGL_Cordinate_Y = (Window_Height) - y
    return openGL_Cordinate_X, openGL_Cordinate_Y'''
