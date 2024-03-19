import pygame
import numpy as np
from math import *

WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
WIDTH, HEIGHT = 800, 600
SCALE = 100

circle_pos = [WIDTH/2, HEIGHT/2]


angle = 0

pygame.display.set_caption("3D Projection")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

points = []

points.append(np.matrix([-1,-1,1]))
points.append(np.matrix([1,-1,1]))
points.append(np.matrix([1,1,1]))
points.append(np.matrix([-1,1,1]))
points.append(np.matrix([-1,-1,-1]))
points.append(np.matrix([1,-1,-1]))
points.append(np.matrix([1,1,-1]))
points.append(np.matrix([-1,1,-1]))

projection_matrix = np.matrix([
    [1,0,0],
    [0,1,0],
    [0,0,0]])

projected_points = [
    [n, n] for n in range(len(points))
    ]

def connect_points(i, j, projpoints):
    pygame.draw.line(
        screen, BLACK, (projpoints[i][0], projpoints[i][1]), (projpoints[j][0], projpoints[j][1]))

while True :
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_SPACE:
                angle += 0.1

    #Update
    rotation_z = np.matrix([
        [cos(angle), -sin(angle), 0],
        [sin(angle), cos(angle), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angle), 0, sin(angle)],
        [0, 1, 0],
        [-sin(angle), 0, cos(angle)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle), -sin(angle)],
        [0, sin(angle), cos(angle)],
    ])

    
    #angle += 0.01


    screen.fill(WHITE)


    #draw
    
    i = 0
    for point in points:
        rotated2d = np.dot(rotation_z, point.reshape((3,1)))
        rotated2d = np.dot(rotation_y, rotated2d)

        projected2d = np.dot(projection_matrix, rotated2d)
    
        x = int(projected2d[0][0] * SCALE + circle_pos[0])
        y = int(projected2d[1][0] * SCALE + circle_pos[1])

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, BLACK, (x, y), 5)
        i += 1

    for p in range(4):
        connect_points(p, (p+1) % 4, projected_points)
        connect_points(p+4, ((p+1) % 4) + 4, projected_points)
        connect_points(p, (p+4), projected_points)
    
    pygame.display.update()