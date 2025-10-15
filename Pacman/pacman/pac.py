import pygame
from pacman.board import boards
from pacman.constants import cell_size, color, num1, num2
from pygame.locals import *
import copy

class Pacman:
    def __init__(self, current_rows, current_cols, ix):
        self.current_rows = current_rows
        self.current_cols = current_cols
        self.ix = ix
        self.keys = {K_LEFT: True, K_RIGHT: False, K_UP: False, K_DOWN: False}
        self.lifePoints = 2
        self.temp = self.keys
        self.r = self.keys
        self.pos = None
        self.pos_rl = None 
        self.rotate = False
        self.lifes = [
            pygame.transform.scale(pygame.image.load("1.png"), (cell_size, cell_size)),
            pygame.transform.scale(pygame.image.load("1.png"), (cell_size, cell_size))
        ]
        self.lifes_pos = [(5, 750), (40, 750)]
        self.points = 0
        self.pacman_images = [
            pygame.transform.scale(pygame.image.load("1.png"), (cell_size, cell_size)),
            pygame.transform.scale(pygame.image.load("2.png"), (cell_size, cell_size)),
            pygame.transform.scale(pygame.image.load("3.png"), (cell_size, cell_size)),
            pygame.transform.scale(pygame.image.load("4.png"), (cell_size, cell_size))
        ]
        self.pacman_images_copy = self.pacman_images.copy()
        
        self.countFoods = boards.count(1) +  boards.count(2) 
        
        self.tempCount = self.countFoods
        
        
    def ifAllPointsCollected(self, pacmanBoard):
      for i in range(len(pacmanBoard)):
        for j in range(len(pacmanBoard[i])):
          if pacmanBoard[i][j] == 1 or pacmanBoard[i][j] == 2:
            return False
      
      return True
    
    

    def powerUp(self, board):
        if board[self.current_rows][self.current_cols] == 2:
            return True
        else:
            return False

    def teleporter(self):
        if self.current_rows == 15 and self.current_cols < 1:
            self.current_cols = 29
        elif self.current_rows == 15 and self.current_cols > 28:
            self.current_cols = 0

    def changePos(self, flag):
        self.checkIfNotCollisionDuringMoving()
        self.rememberTheLastKeyPressed()
        self.incrementicTrafficParameters(flag)

    def rotatePacman(self):
        for i in range(len(self.pacman_images)):
            if self.collision(self.current_rows - 1, self.current_cols) and self.pos_rl == 2: # self.pos == pygame.K_UP
                self.pacman_images_copy[i] = pygame.transform.rotate(self.pacman_images[i], 90)
            elif self.collision(self.current_rows, self.current_cols - 1) and self.pos_rl == 0:
                self.pacman_images_copy[i] = pygame.transform.rotate(self.pacman_images[i], 180)
            elif self.collision(self.current_rows, self.current_cols + 1) and self.pos_rl == 1:
                self.pacman_images_copy[i] = pygame.transform.rotate(self.pacman_images[i], 0)
            elif self.collision(self.current_rows + 1, self.current_cols) and self.pos_rl == 3:
                self.pacman_images_copy[i] = pygame.transform.rotate(self.pacman_images[i], 270)

    def checkRotateRate(self):
        if self.rotate == False:
            self.rotatePacman()
            self.rotate = True

    def incrementicTrafficParameters(self, flag):
        if self.temp[K_LEFT]:
            if self.collision(self.current_rows, self.current_cols - 1):
                self.current_cols -= 1
                if flag:
                    self.checkRotateRate()
        if self.temp[K_RIGHT]:
            if self.collision(self.current_rows, self.current_cols + 1):
                self.current_cols += 1 
                if flag:
                    self.checkRotateRate()
        if self.temp[K_UP]:
            if self.collision(self.current_rows - 1, self.current_cols):
                self.current_rows -= 1
                if flag:
                    self.checkRotateRate()
        if self.temp[K_DOWN]:
            if self.collision(self.current_rows + 1, self.current_cols):
                self.current_rows += 1 
                if flag:
                    self.checkRotateRate()
    
    # {'left': 0, 'right': 1, 'up': 2, 'down': 3} 
    

        
    def incrementicTrafficParametersRL(self, action, flag=True):
        old_pos = self.pos_rl
        if action == 0:
            self.pos_rl = 0
        elif action == 1:
            self.pos_rl = 1
        elif action == 2:
            self.pos_rl = 2
        elif action == 3:
            self.pos_rl = 3
        if old_pos != self.pos_rl:
            self.rotate = False  
        if action == 0:  # left
            if self.collision(self.current_rows, self.current_cols - 1):
                self.current_cols -= 1
                if flag:
                    self.checkRotateRate()
        elif action == 1:  # right
            if self.collision(self.current_rows, self.current_cols + 1):
                self.current_cols += 1
                if flag:
                    self.checkRotateRate()
        elif action == 2:  # up
            if self.collision(self.current_rows - 1, self.current_cols):
                self.current_rows -= 1
                if flag:
                    self.checkRotateRate()
        elif action == 3:  # down
            if self.collision(self.current_rows + 1, self.current_cols):
                self.current_rows += 1
                if flag:
                    self.checkRotateRate()
   
        
    def increasePoints(self, screen, font, pacmanBoard, flag=True, is_reward=False): 
        # mała kropka 
        reward = 0 
        if pacmanBoard[self.current_rows][self.current_cols] == 1:
            self.points += 10
            if flag:
                pygame.draw.circle(screen, 'black', (self.current_cols * num2 + (0.5 * num2), self.current_rows * num1 + (0.5 * num1)), 4)
            pacmanBoard[self.current_rows][self.current_cols] = 0
            if is_reward: 
                reward += 1
                print('reward +1')
                return reward
        # duża kropka 
        elif pacmanBoard[self.current_rows][self.current_cols] == 2:
            self.points += 50 # 50
            
            if flag: 
                pygame.draw.circle(screen, 'black', (self.current_cols * num2 + (0.5 * num2), self.current_rows * num1 + (0.5 * num1)), 10)
            pacmanBoard[self.current_rows][self.current_cols] = 0 
  
        if is_reward:
            return reward
        
        if flag: 
            text = font.render(str(self.points), True, (255, 255, 255))
            screen.blit(text, (750, 770))

    def rememberTheLastKeyPressed(self):
        if self.pos == pygame.K_LEFT:
            if self.collision(self.current_rows, self.current_cols - 1):
                self.temp = self.r
        if self.pos == pygame.K_RIGHT:
            if self.collision(self.current_rows, self.current_cols + 1):
                self.temp = self.r
        if self.pos == pygame.K_UP:
            if self.collision(self.current_rows - 1, self.current_cols):
                self.temp = self.r
        if self.pos == pygame.K_DOWN:
            if self.collision(self.current_rows + 1, self.current_cols):
                self.temp = self.r
        self.rotate = False

    def checkIfNotCollisionDuringMoving(self):

        arrow_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        
        self.keys = pygame.key.get_pressed()

        for i in range(len(arrow_keys)):

            if self.keys[arrow_keys[i]] == True:
                self.r = self.keys
                self.pos = arrow_keys[i]
                self.rotate = False
                if arrow_keys[i] == pygame.K_LEFT:
                    if not self.collision(self.current_rows, self.current_cols - 1):
                        break
                if arrow_keys[i] == pygame.K_RIGHT:
                    if not self.collision(self.current_rows, self.current_cols + 1):
                        break
                if arrow_keys[i] == pygame.K_UP:
                    if not self.collision(self.current_rows - 1, self.current_cols):
                        break
                if arrow_keys[i] == pygame.K_DOWN:
                    if not self.collision(self.current_rows + 1, self.current_cols):
                        break

                self.temp = self.keys

    def move(self, screen, flag=True):

        #self.changePos(flag)
        self.teleporter()
        if flag:
            screen.blit(self.pacman_images_copy[self.ix], (self.current_cols * num2 + (0.2 * num2), self.current_rows * num1 + (0.2 * num1)))
        self.ix += 1
        if self.ix > len(self.pacman_images_copy) - 1:
            self.ix = 0


            
    def collision(self, curR, curC):
        if not (0 <= curR < len(boards) and 0 <= curC < len(boards[0])):
            return False  
        walls = {3, 4, 5, 6, 7, 8, 9}
        
        x = boards[curR][curC] not in walls
        return x 
