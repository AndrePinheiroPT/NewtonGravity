import pygame
from pygame.locals import *
from Tools.math_gravity import *
# Screen configuration
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


class Planet:
    """
    -> Create planet object
    """
    def __init__(self, x, y, mass, radius):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.velocity = [0, 0]


def show_check_box(screen_param, position, text, color_text):
    """
    -> Function which can show check box
    passing just 4 parameters
    :screen_param: Screen where will draw.
    :position: Rect position of check box.
    :text: Label of check box.
    :color: Color of the rect.
    :return: Without return.
    """
    label = font_text.render(text, False, (255, 255, 255))
    pygame.draw.rect(screen_param, color_text, [position[0], position[1], 10, 10])
    screen.blit(label, (position[0] + 15, position[1] - 4))


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('NewtonGravity')

pygame.font.init()
font_text = pygame.font.SysFont('Times', 15)

corps = [
    Planet(301, 301, 50, 15),
    Planet(101, 301, 3, 8),
    Planet(501, 301, 3, 8)
]

corps[1].velocity = [0, -125]
corps[2].velocity = [0, 125]

check_box_color1 = (0, 255, 0)
check_box_color2 = (0, 255, 0)

clock = pygame.time.Clock()
while True:
    clock.tick(10)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == MOUSEBUTTONDOWN:
            if 10 <= mouse[0] <= 20 and 10 <= mouse[1] <= 20:
                check_box_color1 = [255, 0, 0] if check_box_color1[1] != 0 else [0, 255, 0]
            if 10 <= mouse[0] <= 20 and 30 <= mouse[1] <= 40:
                check_box_color2 = [255, 0, 0] if check_box_color2[1] != 0 else [0, 255, 0]

    mouse = pygame.mouse.get_pos()

    show_check_box(screen, (10, 10), 'Show vector field', check_box_color1)
    show_check_box(screen, (10, 30), 'Show velocity vector', check_box_color2)

    if check_box_color1[1] != 0:
        draw_vector_field(corps, screen)

    update_position(corps)
    update_gravity(corps)

    if check_box_color2[1] != 0:
        draw_velocity_vector(corps, screen)

    pygame.display.update()
