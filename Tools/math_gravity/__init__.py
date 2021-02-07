import math
import pygame
# Newton's constant
G = 10 ** 4


def grid(x, y):
    """
    -> Function which helps to change cartesian coordinates
    for standard coordinates and vice versa.
    :x: X of old grid.
    :y: Y of old grid.
    """
    return [x, 600 - y]


def draw_vector_field(planets, screen):
    """
    -> Function creates a gravitational vector field
    :planets: List of corps that will be control.
    :screen: Screen where will draw.
    """
    for x in range(20, 600, 20):
        for y in range(20, 600, 20):
            inputs = [x, y]
            vector = [0, 0]
            base_vector = [0, 0]

            for pla in planets:
                # Vector that goes from the input to the coordinates of the planet
                base_vector[0] = pla.x - inputs[0]
                base_vector[1] = pla.y - inputs[1]

                vector_length = math.sqrt((base_vector[0] ** 2) + (base_vector[1] ** 2))

                # Newton's formula
                for i in range(0, 2):
                    gama = 1
                    if G * pla.mass / vector_length ** 3 <= 1:
                        gama = (G * pla.mass) / vector_length ** 3
                    base_vector[i] *= gama
                    vector[i] += base_vector[i] / 2

            # Show vector
            pygame.draw.line(
                screen,
                (0, 250, 0),
                grid(x, y),
                grid(x + vector[0], y + vector[1])
            )


def draw_velocity_vector(planets, screen):
    for corp in planets:
        pygame.draw.line(
            screen,
            (255, 255, 0),
            grid(corp.x, corp.y),
            grid(corp.x + corp.velocity[0] / 5, corp.y + corp.velocity[1] / 5)
            # divide by 5 for not a mini vector
        )


def update_position(planets, screen):
    """
    -> Function updates the position of the planets
    :planets: List of corps that will be control.
    :screen: Screen where will draw.
    """
    for corp in planets:
        corp.x += corp.velocity[0] / 10
        corp.y += corp.velocity[1] / 10

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            grid(int(corp.x), int(corp.y)),
            corp.radius
        )


def update_gravity(planets):
    """
    -> That function adds a velocity vector for all planets
    :planets: List of corps that will be control.
    """
    for corp in planets:
        vector_sum = [0, 0]

        for key in range(0, len(planets)):
            if planets.index(corp) != key:
                base_vector = [0, 0]
                # Vector that goes from the planet(i) to the coordinates of other planet(i+1)
                base_vector[0] = planets[key].x - corp.x
                base_vector[1] = planets[key].y - corp.y

                vector_length = math.sqrt((base_vector[0] ** 2) + (base_vector[1] ** 2))

                # Newton's formula
                for i in range(0, 2):
                    base_vector[i] *= (G * planets[key].mass) / vector_length ** 3
                    vector_sum[i] += base_vector[i]

        # Update velocity vector
        for i in range(0, 2):
            corp.velocity[i] += vector_sum[i]
