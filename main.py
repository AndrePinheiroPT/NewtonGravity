import pygame
from pygame.locals import *
from Tools.math_gravity import *
from Tools.menu_graph import *

# Screen configuration
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

corps = []

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('NewtonGravity')

pygame.font.init()
font = pygame.font.SysFont('Times', 15)

checkboxes = [
    Checkbox((10, 10), 'Show vector field', 1, font),
    Checkbox((10, 30), 'Show velocity vector', 1, font),
    Checkbox((10, 50), 'Freeze', 0, font)
]

created_planet = 0
mouse_down = 0
out_of_checkboxes = 0
clock = pygame.time.Clock()
while True:
    clock.tick(40)
    screen.fill((0, 0, 0))

    total_checked = 0
    mouse = pygame.mouse.get_pos()

    for checkbox in checkboxes:
        checkbox.show_checkbox(screen)
        checkbox.check_checkbox(mouse)
        total_checked += checkbox.out_of_checkboxes

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == MOUSEBUTTONDOWN:
            mouse_down = 1

            for checkbox in checkboxes:
                checkbox.check_checkbox(mouse)
                if not checkbox.out_of_checkboxes:
                    checkbox.change_state()

            if total_checked == 3:
                created_planet = Planet(mouse[0], 600 - mouse[1], 10, 10)

        if event.type == MOUSEBUTTONUP:
            mouse_down = 0

            if total_checked == 3:
                created_planet.velocity = [(mouse[0] - created_planet.x) * 3, (600 - mouse[1] - created_planet.y) * 3]
                corps.append(created_planet)

    if mouse_down and total_checked == 3:
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            grid(created_planet.x, created_planet.y),
            created_planet.radius
        )
        pygame.draw.line(
            screen,
            (0, 0, 255),
            grid(created_planet.x, created_planet.y),
            (mouse[0], mouse[1])
        )

    if not checkboxes[2].activate:
        check_collision_edges(corps, SCREEN_WIDTH, SCREEN_HEIGHT)
        check_collision_planets(corps)
        update_gravity(corps)
        update_position(corps)
    if checkboxes[0].activate:
        draw_vector_field(corps, screen)
    if checkboxes[1].activate:
        draw_velocity_vector(corps, screen)

    draw_planets(corps, screen)
    pygame.display.update()
