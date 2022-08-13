import math
import random

import numpy as np
import pygame
from config import *
from tools.np import normalizeto
from objects.behavior import Behavior

class VisionSensor(pygame.sprite.Sprite):
    def __init__(self, position, orientation, ratio = 100, angle = 180) -> None:
        pygame.sprite.Sprite.__init__(self)
  

        self.radius = ratio
        self.image = pygame.Surface((ratio*2, ratio*2), pygame.SRCALPHA)
        self.rect = pygame.draw.circle(self.image, GREEN, self.image.get_rect().center, self.radius, 1)
        self.rect.center = position

    # def update(self, position, orientation):
    def update(self, position, orientation):
        self.rect.center = position

    def draw(self, window, color):
        pygame.draw.circle(window, color, self.rect.center, self.radius, 1)  
    # def get_collide(group: pygame.sprite.Group):
    #     pass


class Agent(pygame.sprite.Sprite, Behavior):
    def __init__(self, position, color=None) -> None:
        pygame.sprite.Sprite.__init__(self)
        Behavior.__init__(self)

        self.on = True

        if color:
            self.color = color
        else:
            self.color = (random.random() * 255*(2/3), random.random() * 255*(2/3), random.random() * 255*(2/3))

        self.size = SIZE
        self.mass = MASS
        self.maxforce = MAX_FORCE
        self.maxvelocity= MAX_VELOCITY

        self.position = np.array(position, dtype=float)       
        self.velocity = np.array((random.random()*2 -1,random.random()*2 -1))
        self.acceleration = np.zeros(2)
        self.orientation = math.atan2(self.velocity[0], self.velocity[1])

        # vision sensor
        self.sensor = VisionSensor(position, self.orientation)

        # behavior
        self.behavior = random.choice([self.seek, self.flee, self.arrive, self.wander, self.wander_simple])
        print(self.behavior)
        
    def check_edges(self): # aqui melhorar
        correction_force = np.zeros(2)
        # if self.position[0] < 0 or self.position[1] < 0 or self.position[0] > SCREENWIDTH or self.position[1] > SCREENHEIGHT:
            # correction_force += (self.seek((SCREENWIDTH/2, SCREENHEIGHT/2)) * (abs(self.position[0])%SCREENWIDTH) * (abs(self.position[1])%SCREENHEIGHT)) *0.5
            # self.applyForce(correction_force)   
        if self.position[0] < 0:
            correction_force += self.flee(self.position + (-1, 0))
        if self.position[1] < 0:
            correction_force += self.flee(self.position + (0, -1))
        if self.position[0] > SCREENWIDTH:
            correction_force += self.flee(self.position + (1, 0))
        if self.position[1] > SCREENHEIGHT:
            correction_force += self.flee(self.position + (0, 1))

        return correction_force

    def update(self, agents):
        '''
        function that handles an agents behavior
        '''
        force = np.zeros(2)
        # self.forces = []

        # calculate forces
        force = self.behavior()
        
        # # combining steering forces
        # f1 = self.wander_simple()
        # f2 = self.flee()
        # force = f1 + f2

        # handle the edges
        force = force + self.check_edges()

        #apply forces
        self.applyForce(force)

        self.sensor.update(self.position, self.orientation)

    def applyForce(self, force):
        '''
        function to apply a force to an agent
        '''
        self.acceleration = force / self.mass
        self.velocity += self.acceleration
        # limit velocity
        if np.linalg.norm(self.velocity) > self.maxvelocity:
            self.velocity = normalizeto(self.velocity,self.maxvelocity)
        self.position += self.velocity
        self.orientation = math.atan2(self.velocity[0], self.velocity[1])

    def draw(self, window, draw_sensor):
        '''
        function that draws the agent
        '''
        # tip = normalizeto(self.velocity, self.size)
        # tiplineEnd = (self.position[0] + tip[0],
        #         self.position[1] + tip[1])

        # angle = math.atan2(self.velocity[0], self.velocity[1]) + (math.pi*0.85)
        # angle2 = math.atan2(self.velocity[0], self.velocity[1]) - (math.pi*0.85)
        # angleLineR = (self.position[0] + math.sin(angle) * self.size,
        #             self.position[1] + math.cos(angle) * self.size)
        # angleLineL = (self.position[0] + math.sin(angle2) * self.size,
        #             self.position[1] + math.cos(angle2) * self.size) 

        # pygame.draw.line(window, self.color, angleLineR, tiplineEnd,
        #                 max(1, int((self.size * self.size) / 100)))
        # pygame.draw.line(window, self.color, angleLineL, tiplineEnd,
        #                 max(1, int((self.size * self.size) / 100)))
        # pygame.draw.line(window, self.color, self.position, angleLineR,
        #                 max(1, int((self.size * self.size) / 100)))
        # pygame.draw.line(window, self.color, self.position, angleLineL,
        #                 max(1, int((self.size * self.size) / 100)))          

        pygame.draw.circle(window, self.color, self.position, 3, 5)     
        
        if draw_sensor:
            self.sensor.draw(window, self.color)    
