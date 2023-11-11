import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy as np

angle_x = 0.0
angle_y = 0.0
camera_distance = -10.0


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, camera_distance)


def midpoint_equations(t):
    x = 1.5 * t
    y = 0.5 * t + 2
    z = 1 - t
    return x, y, z


def line1_equations(t):
    x = 1 + t
    y = 3 + t
    z = 2 + t
    return x, y, z


def line2_equations(t):
    x = 1 + 2 * t
    y = 1
    z = t
    return x, y, z


def draw_line(point1, point2, color):
    glBegin(GL_LINES)
    glColor3f(*color)
    glVertex3f(*point1)
    glVertex3f(*point2)
    glEnd()


def draw():
    global angle_x, angle_y, camera_distance

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, camera_distance)
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)

    # Отрисовка трех прямых
    t_values = np.linspace(-10, 10, 100)

    glBegin(GL_POINTS)
    glColor3f(0, 0, 1) 
    for t in t_values:
        x, y, z = midpoint_equations(t)
        glVertex3f(x, y, z)
    glEnd()

    glBegin(GL_LINES)
    glColor3f(1, 0, 0)  
    for i in range(len(t_values) - 1):
        x1, y1, z1 = line1_equations(t_values[i])
        x2, y2, z2 = line1_equations(t_values[i + 1])
        glVertex3f(x1, y1, z1)
        glVertex3f(x2, y2, z2)
    glEnd()

    glBegin(GL_LINES)
    glColor3f(0, 1, 0) 
    for i in range(len(t_values) - 1):
        x1, y1, z1 = line2_equations(t_values[i])
        x2, y2, z2 = line2_equations(t_values[i + 1])
        glVertex3f(x1, y1, z1)
        glVertex3f(x2, y2, z2)
    glEnd()

    for t in t_values:
        x1, y1, z1 = line1_equations(t)
        x2, y2, z2 = line2_equations(t)
        x_mid, y_mid, z_mid = midpoint_equations(t)

        draw_line((x1, y1, z1), (x_mid, y_mid, z_mid), (1, 0, 0))  
        draw_line((x2, y2, z2), (x_mid, y_mid, z_mid), (0, 1, 0)) 

    pygame.display.flip()



def main():
    global angle_x, angle_y, camera_distance

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            angle_x -= 0.015
        if keys[pygame.K_s]:
            angle_x += 0.015
        if keys[pygame.K_a]:
            angle_y -= 0.015
        if keys[pygame.K_d]:
            angle_y += 0.015

        if keys[pygame.K_UP]:
            camera_distance += 0.1
        if keys[pygame.K_DOWN]:
            camera_distance -= 0.1

        draw()


if __name__ == "__main__":
    main()
