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
pygame.font.init()

# Initialize matrix and camera variables
xScale, xScaleChange = 1, 0
yScale, yScaleChange = 1, 0
zScale, zScaleChange = 1, 0
scale, scaleChange = 100, 0

# Camera translation
locX = 0
locY = 0
locZ = 0

# Camera rotation
rotX, rotY, rotZ = 0, 0, 0
changeRotX, changeRotY, changeRotZ = 0, 0, 0
rotationMatrix = ''

#Axis
axis = [n for n in range(3)]
axis[0] = np.array([[1], [0], [0], [1]])
axis[1] = np.array([[0], [1], [0], [1]])
axis[2] = np.array([[0], [0], [1], [1]])


# Draw method ---------------------------------------------------------------------------------------------------------#
def draw(points, axis):
    mainScreen.fill((255, 255, 255))

    #Draw axis:
    draw_lines(axis[0], np.array([[0], [0], [0], [1]]), (255, 0, 0))
    draw_lines(axis[1], np.array([[0], [0], [0], [1]]), (0, 255, 0))
    draw_lines(axis[2], np.array([[0], [0], [0], [1]]), (0, 0, 255))


    # Draw lines
    draw_lines(points[0], points[1], (0, 0, 0))
    draw_lines(points[1], points[3], (0, 0, 0))
    draw_lines(points[2], points[3], (0, 0, 0))
    draw_lines(points[2], points[0], (0, 0, 0))
    draw_lines(points[4], points[5], (0, 0, 0))
    draw_lines(points[5], points[7], (0, 0, 0))
    draw_lines(points[6], points[7], (0, 0, 0))
    draw_lines(points[6], points[4], (0, 0, 0))
    draw_lines(points[0], points[4], (0, 0, 0))
    draw_lines(points[1], points[5], (0, 0, 0))
    draw_lines(points[3], points[7], (0, 0, 0))
    draw_lines(points[2], points[6], (0, 0, 0))

    # Draw points
    for point in points:
        pygame.draw.circle(mainScreen, (0, 0, 0), (point[0, 0] + WINDOW_SIZE[0] / 2, point[1, 0] + WINDOW_SIZE[1] / 2),
                           10)

    # Draw text
    draw_text("Rotation X: " + str(rotX), 10, 10)
    draw_text("Rotation Y: " + str(rotY), 10, 30)
    draw_text("Rotation Z: " + str(rotZ), 10, 50)
    draw_text("Scale X: " + str(xScale), 10, 70)
    draw_text("Scale Y: " + str(yScale), 10, 90)
    draw_text("Scale Z: " + str(zScale), 10, 110)
    draw_text("Rotation Matrix:\n " + rotationMatrix, 10, 130)

    pygame.display.update()
    mainClock.tick(FPS)


# draw lines connecting points
def draw_lines(a, b, color):
    pygame.draw.line(mainScreen, color, (a[0, 0] + WINDOW_SIZE[0] / 2, a[1, 0] + WINDOW_SIZE[1] / 2),
                     (b[0, 0] + WINDOW_SIZE[0] / 2, b[1, 0] + WINDOW_SIZE[1] / 2), 2)

def draw_text(text, x, y):
    textFont = pygame.font.Font('Fonts//Ubuntu-M.ttf', 17)
    lines = text.splitlines()
    for i, l in enumerate(lines):
        mainScreen.blit(textFont.render(l, 0, (175, 175, 175)), (x, y + 17 * i))


# Matrix calculations -------------------------------------------------------------------------------------------------#
def update(points):
    global rotationMatrix
    updated_points = []
    updated_axis = []

    displacement = np.array([[xScale + scale, 0, 0, -locX],
                             [0, yScale + scale, 0, -locY],
                             [0, 0, zScale + scale, -locZ],
                             [0, 0, 0, scale]])

    standard_displacement = np.array([[100, 0, 0, -locX],
                                      [0, 100, 0, -locY],
                                      [0, 0, 100, -locZ],
                                      [0, 0, 0, 100]])

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
        rotationMatrix = str(np.matmul(rotationZ, np.matmul(rotationY, rotationX)))
        updated_points.append(updated_point)

    for point in axis:
        updated_point = np.matmul(standard_displacement, point)
        updated_point = np.matmul(rotationX, updated_point)
        updated_point = np.matmul(rotationY, updated_point)
        updated_point = np.matmul(rotationZ, updated_point)
        updated_axis.append(updated_point)

    return updated_points, updated_axis


def update_variables():
    global scale, xScale, yScale, zScale, scaleChange, xScaleChange, yScaleChange, zScaleChange
    global rotX, rotY, rotZ,  changeRotX, changeRotY, changeRotZ
    rotX += changeRotX
    rotY += changeRotY
    rotZ += changeRotZ
    xScale += xScaleChange
    yScale += yScaleChange
    zScale += zScaleChange
    scale += scaleChange



# Main game loop ------------------------------------------------------------------------------------------------------#
def main():
    # Initialize game loop variables
    global rotX, rotY, rotZ, changeRotX, changeRotY, changeRotZ
    global locX, locY, locZ
    global size, xScaleChange, yScaleChange, zScaleChange, scaleChange
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

        projected_points, projected_axis = update(points)

        # Draw
        draw(projected_points, projected_axis)

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
                    scaleChange = -1
                if event.key == pygame.K_m:
                    scaleChange = 1
                if event.key == pygame.K_q:
                    xScaleChange = 1
                if event.key == pygame.K_a:
                    xScaleChange = -1
                if event.key == pygame.K_w:
                    yScaleChange = 1
                if event.key == pygame.K_s:
                    yScaleChange = -1
                if event.key == pygame.K_e:
                    zScaleChange = 1
                if event.key == pygame.K_d:
                    zScaleChange = -1

            #KEYUP
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeRotX = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    changeRotY = 0
                if event.key == pygame.K_z or event.key == pygame.K_x:
                    changeRotZ = 0
                if event.key == pygame.K_n or event.key == pygame.K_m:
                    scaleChange = 0
                if event.key == pygame.K_q or event.key == pygame.K_a:
                    xScaleChange = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    yScaleChange = 0
                if event.key == pygame.K_e or event.key == pygame.K_d:
                    zScaleChange = 0
            # Exit code
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()


main()
