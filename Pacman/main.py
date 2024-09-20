import pygame
from pacman.board import boards
from pacman.generateBoard import Board
from pacman.constants import HEIGHT, WIDTH
from pacman.pac import Pacman
from pacman.ghosts import Ghosts
import copy 

pygame.init()


screen = pygame.display.set_mode([WIDTH,HEIGHT])
timer = pygame.time.Clock()
fps = 9

pacmanBoard = copy.deepcopy(boards)

font = pygame.font.Font("freesansbold.ttf", 20)

obj = Board()
ghost = Ghosts()

pacman = Pacman(23,12,0)

#text2 = 0

run = True 
ghost.create_ghost_object(screen)
while run:
  timer.tick(fps)
  screen.fill('black')
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
      
  obj.draw_board(screen,pacmanBoard, pacman, font)
  ghost.freeGhosts(screen, obj, font ,pacman, ghost)
  
  pacman.increasePoints(screen, font, pacmanBoard)
  
  ghost.killingGhostByPacman(pacman, screen, font, obj, (13, 14))
  
  ghost.returningToTheGateAfterCollision(pacman, screen, font)
  pacman.move(screen)
  ghost.killingGhostByPacman(pacman, screen, font, obj, (13, 14))
  
  ghost.returningToTheGateAfterCollision(pacman, screen, font)
  
  if pacman.ifAllPointsCollected(pacmanBoard):
    pacmanBoard = copy.deepcopy(boards) # czy działa z samym copy ?? 
  
  pygame.display.flip()
  
  if ghost.checkIfGameOver():
    break

pygame.quit()