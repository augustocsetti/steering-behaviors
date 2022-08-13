import sys

import pygame

from objects.agent import *
from config import *


class SteeringBehaviorSimulation:
    def __init__(self) -> None:
        pygame.init()

        self.window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pygame.display.set_caption("Steering Behavior")
        self.window.fill(BLACK)

        self.clock = pygame.time.Clock()
        
        # generate agents
        print('Generating agents...')
        self.agents = []
        for _ in range(1):
            self.agents.append(Agent((int(random.random()*SCREENWIDTH),int(random.random()*SCREENHEIGHT))))

        # draw control
        self.draw_sensor = False
        # self.draw_grid = False
        # self.draw_mark = False

        print('All done!')

    def run(self):
        self.start = False
        self.run = True
        while(self.run):
            self.window.fill(BLACK)

            self.event_handler()
            if self.start:
                self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
        quit()   

    def event_handler(self):
        # Event handler
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.agents.append(Agent(mouse_pos))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.start = not self.start
                # if event.key == pygame.K_g:
                #     self.draw_grid = not self.draw_grid
                # if event.key == pygame.K_m:
                #     self.draw_mark = not self.draw_mark                   
                if event.key == pygame.K_r:
                    try: self.agents.pop()                    
                    except: pass
                if event.key == pygame.K_s:
                    self.draw_sensor = not self.draw_sensor                  
        return

    def update(self):
        # updating agents position
        for agent in self.agents:
            agent.update(self.agents)
            # check if agent hit his goal
            # if not agent.on:
            #     self.agents.remove(agent)

    def draw(self):
        # agents
        for agent in self.agents:
            # agent.draw(self.window, self.draw_sensor)
            agent.draw(self.window, self.draw_sensor)

    def print_instructions(self):
        print('\n- Instructions:')
        print('\tSPACE BAR    Start/Stop simulation.')
        print('\tON CLICK     Add a agent at mouse position.')
        # print('\tG            Turn on/off grids draw.')
        # print('\tM            Turn on/off markers draw.')
        print('\tR            Delete last agent created.')
        print('\tS            Turn on/off sensor draw.')
        
        print('\nYou also can change all parameters playing with config.py file and, on simulation.py file by changing the parameters from simulations functions')

if __name__ == '__main__':

    print('# Steering Behavior\n')

    simulation = SteeringBehaviorSimulation()
    simulation.print_instructions()
    simulation.run()
