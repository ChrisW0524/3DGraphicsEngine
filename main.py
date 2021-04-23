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

# Initialize matrix variables
scale = 100

locX = 0
locY = 0
locZ = 0

rotX = 0
rotY = 0
rotZ = 0

# Draw method ---------------------------------------------------------------------------------------------------------#
def draw(points):
    mainScreen.fill((255, 255, 255))
    for point in points:
        pygame.draw.circle(mainScreen,(0, 0, 0), (point[0, 0] + WINDOW_SIZE[0] / 2, point[1, 0]+ WINDOW_SIZE[1] / 2),10)

    # Draw lines
    draw_lines(points[0], points[1])
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
    draw_lines(points[2], points[6])

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
        updated_point = np.matmul(rotationX, point)
        updated_point = np.matmul(rotationY, updated_point)
        updated_point = np.matmul(rotationZ, updated_point)
        updated_point = np.matmul(displacement, updated_point)
        updated_points.append(updated_point)

    return updated_points


# Main game loop ------------------------------------------------------------------------------------------------------#
def main():
    # Initialize game loop variables
    global rotX
    global rotY
    global rotZ
    global scale
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
        rotX += math.pi / 360
        rotY += math.pi / 360
        rotZ += math.pi / 360
        scale += 1
        projected_points = update(points)

        # Draw
        draw(projected_points)

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                continue

            # Exit code
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()


main()
