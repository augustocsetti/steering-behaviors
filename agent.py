import math
import random

import numpy as np
import pygame
from config import *


class Agent:
    def __init__(self, position) -> None:

        self.origin = np.array(position)
        self.size = 15
        self.color = (random.random() * 128, random.random() * 128, random.random() * 128)

        self.visionratio = 100
        self.position = np.array(position, dtype=float)       
        self.velocity = np.array((random.random()*2 -1,random.random()*2 -1))
        self.acceleration = np.zeros(2)
        self.maxforce = .5
        self.maxvelocity= 3
        self.mass = 10 # aqui
        # self.orientation = self.velocity/np.linalg.norm(self.velocity) # aqui

        # behavior
        self.behavior = random.choice([self.seek, self.flee, self.arrive, self.wander, self.wander_simple])
        print(self.behavior)
        
        # for wander
        self.target = np.array((random.randint(0, SCREENWIDTH), random.randint(0, SCREENHEIGHT)))
        self.last_target = 0

    def seek(self, target_pos=None):
        if not np.any(target_pos != None):
            target_pos = pygame.mouse.get_pos()
        steer = np.zeros(2)
        #difference to target
        desired = np.array(target_pos) - self.position
        #normalization
        if np.linalg.norm(desired) > 0:
            desired = desired/np.linalg.norm(desired)
            #magnitude is maxvelocity
            desired = desired * self.maxvelocity
            #calculate steering force
            steer = desired - self.velocity
            # limit force
            if np.linalg.norm(steer) > self.maxforce:
                steer = self.normalizeto(steer, self.maxforce)        
        return steer

    def flee(self, target_pos=None):
        if not np.any(target_pos != None):
            target_pos = pygame.mouse.get_pos()
        steer = np.zeros(2)
        # difference to target
        difference = np.array(target_pos) - self.position
        #distance
        distance = np.linalg.norm(difference)
        # normalization
        if distance < self.visionratio and distance > 0:
            desired = difference / np.linalg.norm(difference)
            # magnitude is maxvelocity
            desired_speed = self.maxvelocity
            desired = desired * desired_speed
            # calculate steering force
            steer = desired - self.velocity
        return steer*-1

    def arrive(self, target_pos=None):
        if not np.any(target_pos != None):
            target_pos = pygame.mouse.get_pos()
        steer = np.zeros(2)
        #difference to target
        difference = np.array(target_pos) - self.position
        #normalization
        distance = np.linalg.norm(difference)
        if distance < self.visionratio:
            # normalize
            desired = difference / np.linalg.norm(difference)
            #magnitude is dependant on distance to target
            desired_speed = np.interp(distance,[0,self.visionratio],[0,self.maxvelocity])
            # set magnitude
            desired = desired * desired_speed     
        else:
            desired = difference/np.linalg.norm(difference)
            #magnitude is maxvelocity
            desired = desired*self.maxvelocity
        
        #calculate steering force
        steer = desired - self.velocity
        return steer

    def wander_simple(self):
        now = pygame.time.get_ticks()
        if now - self.last_target > 1000:
            self.last_target = now
            self.target = self.target = np.array((random.randint(0, SCREENWIDTH), random.randint(0, SCREENHEIGHT)))
        return self.seek(self.target)

    def wander(self):
        orientation = self.velocity/np.linalg.norm(self.velocity)
        circle_position = self.position + self.normalizeto(orientation, WANDER_RING_DISTANCE)
        target = circle_position + np.array((random.randint(-WANDER_RING_RADIUS, WANDER_RING_RADIUS),
                                             random.randint(-WANDER_RING_RADIUS, WANDER_RING_RADIUS)))
        return self.seek(target)

    def update(self, agents):
        '''
        function that handles an agents behavior
        '''
        force = np.zeros(2)
        # self.forces = []

        #calculate forces
        force = self.behavior()
        
        # # combining steering forces
        # f1 = self.wander_simple()
        # f2 = self.flee()
        # force = f1 + f2

        #apply forces
        self.applyForce(force)

        #HANDLE THE EDGE AQUI
        if self.position[0] < 0 or self.position[1] < 0 or self.position[0] > SCREENWIDTH or self.position[1] > SCREENHEIGHT:
            correction_force = (self.seek((SCREENWIDTH/2, SCREENHEIGHT/2)) * (abs(self.position[0])%SCREENWIDTH) * (abs(self.position[1])%SCREENHEIGHT)) *0.5
            self.applyForce(correction_force)

    def normalizeto(self, vector, max):
        if np.linalg.norm(vector) > 0:
            return (vector/np.linalg.norm(vector)) * max
        else:
            return np.zeros(2)    

    def applyForce(self, force):
        '''
        function to apply a force to an agent
        '''
        self.acceleration = force / self.mass
        self.velocity += self.acceleration
        # limit velocity
        if np.linalg.norm(self.velocity) > self.maxvelocity:
            self.velocity = self.normalizeto(self.velocity,self.maxvelocity)
        # if np.linalg.norm(self.velocity) < 0.5 and np.linalg.norm(self.acceleration) == 0:
        #     self.velocity = (0, 0)
        self.position += self.velocity

    def draw(self, window):
        '''
        function that draws the agent
        '''
        tip = self.normalizeto(self.velocity, self.size)
        tiplineEnd = (self.position[0] + tip[0],
                self.position[1] + tip[1])

        angle = math.atan2(self.velocity[0], self.velocity[1]) + (math.pi*0.85)
        angle2 = math.atan2(self.velocity[0], self.velocity[1]) - (math.pi*0.85)
        angleLineR = (self.position[0] + math.sin(angle) * self.size,
                    self.position[1] + math.cos(angle) * self.size)
        angleLineL = (self.position[0] + math.sin(angle2) * self.size,
                    self.position[1] + math.cos(angle2) * self.size)

        pygame.draw.line(window, self.color, angleLineR, tiplineEnd,
                        max(1, int((self.size * self.size) / 100)))
        pygame.draw.line(window, self.color, angleLineL, tiplineEnd,
                        max(1, int((self.size * self.size) / 100)))
        pygame.draw.line(window, self.color, self.position, angleLineR,
                        max(1, int((self.size * self.size) / 100)))
        pygame.draw.line(window, self.color, self.position, angleLineL,
                        max(1, int((self.size * self.size) / 100)))        
