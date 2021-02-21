import math
import pygame
# Newton's constant
G = 10 ** 4


class Planet:
    def __init__(self, x, y, mass, radius):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.velocity = [0, 0]


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
    """
    -> Function which draws a velocity vector
    for each planet.
    :planets: List of corps.
    :screen: List of corps that will be control.
    """
    for corp in planets:
        pygame.draw.line(
            screen,
            (255, 255, 0),
            grid(corp.x, corp.y),
            grid(corp.x + corp.velocity[0] / 5, corp.y + corp.velocity[1] / 5)
            # divide by 5 for make mini vector
        )


def update_position(planets):
    """
    -> Function updates the position of the planets.
    :planets: List of corps that will be control.
    """
    for corp in planets:
        corp.x += corp.velocity[0] / 30
        corp.y += corp.velocity[1] / 30
    # Divide of the numbers of fps


def draw_planets(planets, screen):
    """
    -> Function which drawn planets.
    :planets: List of corps.
    :screen: Screen where will draw.
    """
    for corp in planets:
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


def check_collision_planets(planets):
    """
    -> The function check if two planets collide.
    :planets: List of corps.
    """
    try:
        for i in range(1, len(planets)):
            corp1 = planets[0]
            corp2 = planets[i]

            distance = math.sqrt(math.pow(corp1.x - corp2.x, 2) + math.pow(corp1.y - corp2.y, 2))

            if corp1.radius + corp2.radius >= distance:
                # Conservation of momentum
                corp1.velocity[0] = (corp1.mass * corp1.velocity[0] + corp2.mass * corp2.velocity[0]) / \
                                    (corp1.mass + corp2.mass)
                corp1.velocity[1] = (corp1.mass * corp1.velocity[1] + corp2.mass * corp2.velocity[1]) / \
                                    (corp1.mass + corp2.mass)
                # Sum the masses and 70% of radius
                corp1.mass = corp1.mass + corp2.mass
                corp1.radius = int((corp1.radius + corp2.radius) * 0.70)
                del planets[planets.index(corp2)]
    except IndexError:
        print('Error to check collision')


def check_collision_edges(planets, sw, sh):
    """
    -> This function checks if the planet collides to the edges,
    if collides, there is reflections.
    :planets: List of corps.
    :sw: Screen width.
    :sh: Screen height.
    """
    for corp in planets:
        # Reflection
        if corp.radius + corp.x >= sw or corp.x - corp.radius <= 0:
            corp.velocity[0] = -corp.velocity[0]
        if corp.radius + corp.y >= sh or corp.y - corp.radius <= 0:
            corp.velocity[1] = -corp.velocity[1]
