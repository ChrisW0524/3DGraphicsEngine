import pygame
import sys
import numpy as np
import math

# Initialize variables -----------------------------------------------------------------------------------------#
pygame.init()
WINDOW_SIZE = [1080, 720]
FPS = 60
mainClock = pygame.time.Clock()
mainScreen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("3D Graphics Engine")

# Initialize matrix and camera variables
scale = 100
changeScale = 0

# Camera translation
locX = 0
locY = 0
locZ = 0

# Camera rotation
rotX, rotY, rotZ = 0, 0, 0
changeRotX, changeRotY, changeRotZ = 0, 0, 0



# Draw method ---------------------------------------------------------------------------------------------------------#
def draw(points):
    mainScreen.fill((255, 255, 255))
    for point in points:
        pygame.draw.circle(mainScreen, (0, 0, 0), (point[0, 0] + WINDOW_SIZE[0] / 2, point[1, 0] + WINDOW_SIZE[1] / 2),
                           10)
        for i in range(8):
            draw_lines(point, points[i])

    # Draw lines
    '''draw_lines(points[0], points[1])
    draw_lines(points[1], points[3])
    draw_lines(points[2], points[3])
    draw_lines(points[2], points[0])
    draw_lines(points[4], points[5])
    draw_lines(points[5], points[7])
    draw_lines(points[6], points[7])
    draw_lines(points[6], points[4])
    draw_lines(points[0], points[4])
    draw_lines(points[1], points[5])
    draw_lines(points[3], points[7])
    draw_lines(points[2], points[6])'''

    pygame.display.update()
    mainClock.tick(FPS)


# draw lines connecting points
def draw_lines(a, b):
    pygame.draw.line(mainScreen, (0, 0, 0), (a[0, 0] + WINDOW_SIZE[0] / 2, a[1, 0] + WINDOW_SIZE[1] / 2),
                     (b[0, 0] + WINDOW_SIZE[0] / 2, b[1, 0] + WINDOW_SIZE[1] / 2), 2)


# Matrix calculations -------------------------------------------------------------------------------------------------#
def update(points):
    updated_points = []

    displacement = np.array([[scale, 0, 0, -locX],
                             [0, scale, 0, -locY],
                             [0, 0, scale, -locZ],
                             [0, 0, 0, scale]])

    rotationX = np.array([[1, 0, 0, 0],
                          [0, np.cos(rotX), -np.sin(rotX), 0],
                          [0, np.sin(rotX), np.cos(rotX), 0, ],
                          [0, 0, 0, 1]])

    rotationY = np.array([[np.cos(rotY), 0, np.sin(rotY), 0],
                          [0, 1, 0, 0],
                          [-np.sin(rotY), 0, np.cos(rotY), 0],
                          [0, 0, 0, 1]])

    rotationZ = np.array([[np.cos(rotZ), -np.sin(rotZ), 0, 0],
                          [np.sin(rotZ), np.cos(rotZ), 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])

    for point in points:
        updated_point = np.matmul(displacement, point)
        updated_point = np.matmul(rotationX, updated_point)
        updated_point = np.matmul(rotationY, updated_point)
        updated_point = np.matmul(rotationZ, updated_point)
        updated_points.append(updated_point)

    return updated_points


def update_variables():
    global scale, changeScale
    global rotX, rotY, rotZ
    global changeRotX, changeRotY, changeRotZ
    rotX += changeRotX
    rotY += changeRotY
    rotZ += changeRotZ
    scale += changeScale


# Main game loop ------------------------------------------------------------------------------------------------------#
def main():
    # Initialize game loop variables
    global rotX, rotY, rotZ
    global changeRotX, changeRotY, changeRotZ
    global locX, locY, locZ
    global scale, changeScale
    run = True

    # Initialize points ([[x], [y], [z], [1]])
    points = [n for n in range(8)]
    points[0] = np.array([[1], [1], [1], [1]])
    points[1] = np.array([[-1], [1], [1], [1]])
    points[2] = np.array([[1], [-1], [1], [1]])
    points[3] = np.array([[-1], [-1], [1], [1]])
    points[4] = np.array([[1], [1], [-1], [1]])
    points[5] = np.array([[-1], [1], [-1], [1]])
    points[6] = np.array([[1], [-1], [-1], [1]])
    points[7] = np.array([[-1], [-1], [-1], [1]])

    while run:
        # Update
        '''rotX += math.pi / 360
        rotY += math.pi / 360
        rotZ += math.pi / 360'''
        update_variables()

        projected_points = update(points)

        # Draw
        draw(projected_points)

        # Event loop
        for event in pygame.event.get():

            #KEYDOWN
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    changeRotX = math.pi / 360
                if event.key == pygame.K_DOWN:
                    changeRotX = -math.pi / 360
                if event.key == pygame.K_LEFT:
                    changeRotY = math.pi / 360
                if event.key == pygame.K_RIGHT:
                    changeRotY = -math.pi / 360
                if event.key == pygame.K_z:
                    changeRotZ = math.pi / 360
                if event.key == pygame.K_x:
                    changeRotZ = -math.pi / 360
                if event.key == pygame.K_n:
                    changeScale = -1
                if event.key == pygame.K_m:
                    changeScale = 1
            #KEYUP
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeRotX = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    changeRotY = 0
                if event.key == pygame.K_z or event.key == pygame.K_x:
                    changeRotZ = 0
                if event.key == pygame.K_n or event.key == pygame.K_m:
                    changeScale = 0
            # Exit code
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()


main()
