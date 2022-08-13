import random

import numpy as np
import pygame
from config import *
from tools.np import normalizeto


class Behavior:
    def __init__(self):
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
                steer = normalizeto(steer, self.maxforce)        
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
        if distance < self.sensor.radius and distance > 0:
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
        if distance < self.sensor.radius:
            # normalize
            desired = difference / np.linalg.norm(difference)
            #magnitude is dependant on distance to target
            desired_speed = np.interp(distance,[0,self.sensor.radius],[0,self.maxvelocity])
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
        circle_position = self.position + normalizeto(orientation, WANDER_RING_DISTANCE)
        target = circle_position + np.array((random.randint(-WANDER_RING_RADIUS, WANDER_RING_RADIUS),
                                             random.randint(-WANDER_RING_RADIUS, WANDER_RING_RADIUS)))
        return self.seek(target)
