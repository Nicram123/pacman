from pacman.board import boards
import pygame
from pacman.constants import BLACK, width, height, SQUARE_SIZE, WHITE, HEIGHT, WIDTH, color, num1, num2
import math
import copy

class Board:
  
  def __init__(self):
    self.copyBoard = copy.copy(boards)
    
  def generateLives(self, pacman, screen):
      for ix, pic in enumerate(pacman.lifes):
          screen.blit(pic, pacman.lifes_pos[ix])
  
  def draw_board(self,screen, board, pacman, font):
    for y in range(len(board)):
        for x in range(len(board[y])):
          cell_type = board[y][x]
          self.draw_cell(screen, x, y, cell_type)
          
    self.generateLives(pacman, screen)
    
          
  def draw_cell(self, screen, j, i, cell_type):
    
    flicker = False
    PI = math.pi

    if cell_type == 1:
        pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
    if cell_type == 2 and not flicker:
        pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
    if cell_type == 3:
        pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                         (j * num2 + (0.5 * num2), i * num1 + num1), 3)
    if cell_type == 4:
        pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                         (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
    if cell_type == 5:
        pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                        0, PI / 2, 3)
    if cell_type == 6:
        pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1],
                        PI / 2, PI, 3)
    if cell_type == 7:
        pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1],
                        PI, 3 * PI / 2, 3)
    if cell_type == 8:
        pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1],
                        3 * PI / 2, 2 * PI, 3)
    if cell_type == 9:
        pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                         (j * num2 + num2, i * num1 + (0.5 * num1)), 3)