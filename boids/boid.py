import pygame
import random
import numpy as np

from util import set_vector_magnitude
from params import *


def get_angle(vec_1, vec_2):
    unit_vec_1 = vec_1 / np.linalg.norm(vec_1)
    unit_vec_2 = vec_2 / np.linalg.norm(vec_2)
    dot_product = np.dot(unit_vec_1, unit_vec_2)
    angle = abs(np.rad2deg(np.arccos(dot_product)))
    return angle


class Boid(pygame.sprite.Sprite):
    image = None
    flock = pygame.sprite.Group()

    def __init__(self, position=None):
        pygame.sprite.Sprite.__init__(self, self.flock)
        self.id = len(self.flock)
        self.rect = self.image.get_rect(center=(4, 13))
        x = random.randint(0, WINDOW_WIDTH)
        y = random.randint(0, WINDOW_HEIGHT)
        self.position = position if position is not None else np.array([x, y])
        self.velocity = set_vector_magnitude(np.random.rand(2), 4)  # set vector mag to 4 (higher speed)
        self.acceleration = np.zeros(2)

    def update(self):
        self.move()
        # reset acceleration to prevent accumulation over time
        self.acceleration = np.zeros(2)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = (self.position[0], self.position[1])

    def move(self):
        separation = self.separation()
        cohesion = self.cohesion()
        alignment = self.alignment()
        # force accumulation - acceleration is the sum of all forces acting on an object
        force_sum = np.add.reduce([separation, cohesion, alignment])
        # applying force to object is equal to setting acceleration to that force
        self.acceleration = force_sum
        self.check_borders()
        self.position = np.add(self.position, self.velocity)
        self.velocity = np.add(self.velocity, self.acceleration)
        # limit speed
        self.velocity = set_vector_magnitude(self.velocity, BOID_MAX_SPEED)

    def get_neighbours(self, neighbours_number, steering, rule):
        for other_boid in self.flock:
            distance_between_boids = np.linalg.norm(np.subtract(self.position, other_boid.position))
            if other_boid is not self and distance_between_boids < BOID_PERCEPTION_DISTANCE:
                if get_angle(self.velocity, np.subtract(self.position, other_boid.position)) < MAX_ANGLE:
                    if rule == "separation":
                        difference = np.subtract(self.position, other_boid.position)
                        steering = np.add(steering, difference / distance_between_boids)
                    if rule == "cohesion":
                        steering = np.add(steering, other_boid.position)
                    if rule == "alignment":
                        steering = np.add(steering, other_boid.velocity)
                    neighbours_number += 1
        return neighbours_number, steering

    def set_steering(self, neighbours_number, steering, factor, rule):
        if neighbours_number > 0:
            steering = steering / neighbours_number
            if rule == "cohesion":
                steering = np.subtract(steering, self.position)
            steering = set_vector_magnitude(steering, BOID_MAX_SPEED)
            steering = np.subtract(steering, self.velocity)
            steering = set_vector_magnitude(steering, factor)
        return steering

    # Cohesion rule - align boid's position with **neighbouring** agents
    # Returns the force which needs to be applied to the agent to correct agent's 'course of movement'.
    def cohesion(self):
        steering = np.zeros(2)  # force which needs to be applied to boid to 'correct' it's current moving direction
        neighbours_number = 0
        neighbours_number, steering = self.get_neighbours(neighbours_number, steering, "cohesion")
        steering = self.set_steering(neighbours_number, steering, BOID_COHESION_FACTOR, "cohesion")
        return steering

    # Alignment rule - align boid's orientation/velocity with **neighbouring** agents
    # Returns the force which needs to be applied to the agent to correct it's 'course of movement'.
    def alignment(self):
        steering = np.zeros(2)  # force which needs to be applied to boid to 'correct' it's current moving direction
        neighbours_number = 0
        neighbours_number, steering = self.get_neighbours(neighbours_number, steering, "alignment")
        steering = self.set_steering(neighbours_number, steering, BOID_ALIGNMENT_FACTOR, "alignment")
        return steering

    # Separation rule - separate boid to avoid crowds
    # Returns the force which needs to be applied to the agent to correct agent's 'course of movement'.
    def separation(self):
        steering = np.zeros(2)
        neighbours_number = 0
        neighbours_number, steering = self.get_neighbours(neighbours_number, steering, "separation")
        steering = self.set_steering(neighbours_number, steering, BOID_SEPARATION_FACTOR, "separation")
        return steering

    def check_borders(self):
        # Repel boids when near border of screen
        if abs(WINDOW_WIDTH / 2 - self.position[0]) > WINDOW_WIDTH / 2 - BORDER_WIDTH:
            repel = BORDER_REPEL_FACTOR if self.position[0] < WINDOW_WIDTH / 2 else -BORDER_REPEL_FACTOR
            self.velocity = np.array([self.velocity[0] + repel, self.velocity[1]])
        if abs(WINDOW_HEIGHT / 2 - self.position[1]) > WINDOW_HEIGHT / 2 - BORDER_WIDTH:
            repel = BORDER_REPEL_FACTOR if self.position[1] < WINDOW_HEIGHT / 2 else -BORDER_REPEL_FACTOR
            self.velocity = np.array([self.velocity[0], self.velocity[1] + repel])
