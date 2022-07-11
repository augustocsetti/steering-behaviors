import sys

import pygame

from agent import *
from config import *


if __name__ == '__main__':

    pygame.init()

    window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Steering bahavior")
    window.fill(BLACK)

    clock = pygame.time.Clock()

    #initial agents
    agents = []
    for i in range(1):
        agents.append(Agent((int(random.random()*1600),int(random.random()*900))))

    run = True
    while(run):
        window.fill(BLACK)
        # Event handler
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                agents.append(Agent(mouse_pos))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    agents = agents[:-1]

        for agent in agents:
            agent.update(agents)
            agent.draw(window)    
                 
        pygame.display.update()
        clock.tick(90)

    pygame.quit()
    quit()                       
