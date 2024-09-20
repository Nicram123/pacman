from pacman.constants import cell_size, num1, num2, POWER_UP_DURATION
import pygame
import random
from pacman.board import boards


class Ghosts():
    def __init__(self, current_rows=0, current_cols=0):

        self.current_rows = current_rows
        self.current_cols = current_cols
        self.listOfObject = []
        self.listOfGhosts = [
            pygame.transform.scale(pygame.image.load("blue.png"), (cell_size, cell_size)),
            pygame.transform.scale(pygame.image.load("pink.png"), (cell_size, cell_size)),
            pygame.transform.scale(pygame.image.load("orange.png"), (cell_size, cell_size)),
            pygame.transform.scale(pygame.image.load("red.png"), (cell_size, cell_size))
        ]
        self.collision_free = []
        self.CageWasLeft = False
        self.last_move_time = 0
        self.move_delay = 2
        self.current_time = 0
        self.powerup = False
        self.x = 0
        self.y = 0
        self.rand = 0
        self.start_time = 0
        self.text_ = ""
        
        
        

    def killingGhostByPacman(self, pacman, screen, font, obj, placeTarget):
        ghost = self.collisionWithPacman(pacman)[1]
        ix = self.collisionWithPacman(pacman)[2]
        if ghost != None and ghost.powerup == True:
            if ghost != None:
                self.listOfObject.pop(ix)
                obj = Ghosts(15, 13)
                self.listOfObject.insert(ix, obj)

    def returningToTheGateAfterCollision(self, pacman, screen, font):
        if self.collisionWithPacman(pacman)[0]:
            self.listOfObject.clear()
            pacman.lifePoints -= 1
            if pacman.lifePoints > -1:
                pacman.lifes.pop(-1)
            pacman.current_rows = 23
            pacman.current_cols = 12
            self.create_ghost_object(screen)
        if self.ifLifePointLessThenZero(pacman, screen, font):
            self.text_ = "Game over"
            text = font.render(self.text_, True, (255, 0, 0))
            screen.blit(text, (335, 350))
            
    def checkIfGameOver(self):
      if self.text_ == "Game over":
        return True

    def ifLifePointLessThenZero(self, pacman, screen, font):
        if pacman.lifePoints < 0:
            return True

    def collisionWithPacman(self, pacman):
        for ix, ghost in enumerate(self.listOfObject):
            if ghost.current_rows == pacman.current_rows and ghost.current_cols == pacman.current_cols:
                return (True, ghost, ix)
        return (False, None, None)

    def create_ghost_object(self, screen):
        for x in range(len(self.listOfGhosts) - 1):
            obj = Ghosts(15, 13 + x)
            self.listOfObject.append(obj)
            screen.blit(self.listOfGhosts[x], (obj.current_cols * num2 + (0.1 * num2), obj.current_rows * num1 + (0.1 * num1)))
        obj = Ghosts(11, 14)
        self.listOfObject.append(obj)
        self.CageWasLeft = True

    def displayGhosts(self, screen, ix):
        screen.blit(self.listOfGhosts[ix], (self.current_cols * num2 + (0.1 * num2), self.current_rows * num1 + (0.1 * num1)))

    def displayDeadForm(self, screen, ix):
        screen.blit(self.listOfDeadGhost[ix], (self.current_cols * num2 + (0.1 * num2), self.current_rows * num1 + (0.1 * num1)))

    def leafingTheCage(self, screen, ix):
        y = 0
        if ix == 2:
            y = 15 - self.current_cols  # yellow
        elif ix == 0 or ix == 1:
            print(self.current_cols)
            y = 14 - self.current_cols  # blue , pink
        x = 13 - 1 - self.current_rows
        self.current_cols -= y
        pygame.time.delay(20)
        self.displayGhosts(screen, ix)
        self.current_rows += x
        pygame.time.delay(20)
        self.displayGhosts(screen, ix)
        self.CageWasLeft = True

    def freeGhosts(self, screen, board, font, pacman, ghost):
        for ix, obj in enumerate(self.listOfObject):
            if obj.CageWasLeft == False:
                obj.leafingTheCage(screen, ix)
            obj.normalMove(screen, board, font, pacman, ghost)
            obj.displayGhosts(screen, ix)

    def create_collision_free_array(self, screen, obj, placeTarget):
        x = []
        s = [-1, 1]
        k = random.randint(0, len(s))
        self.collision_free.clear()
        if self.collision(self.current_rows, self.current_cols - 1):  # - 1
            x.append("left")
            if self.shortPath(obj, self.current_cols - 1, placeTarget):
                self.collision_free.append("left")
        k = random.randint(0, len(s))
        if self.collision(self.current_rows, self.current_cols + 1):  # + 1
            x.append("right")
            if self.shortPath(obj, self.current_cols + 1, placeTarget):
                self.collision_free.append("right")
        k = random.randint(0, len(s))
        if self.collision(self.current_rows - 1, self.current_cols):  # -1
            x.append("up")
            if self.shortPath(obj, self.current_rows - 1, placeTarget):
                self.collision_free.append("up")
        k = random.randint(0, len(s))
        if self.collision(self.current_rows + 1, self.current_cols):  # +1
            x.append("down")
            if self.shortPath(obj, self.current_rows + 1, placeTarget):
                self.collision_free.append("down")

        if len(self.collision_free) > 0:
            rand = random.randint(0, len(self.collision_free) - 1)
            self.Increment(rand)
        else:
            self.collision_free = x
            rand = random.randint(0, len(self.collision_free) - 1)
            self.Increment(rand)

    def shortPath(self, obj, par, placeTarget):
        if placeTarget[0] >= self.current_rows:
            if par == self.current_rows + 1:
                return True
        if placeTarget[0] <= self.current_rows:
            if par == self.current_rows - 1:
                return True
        if placeTarget[1] >= self.current_cols:
            if par == self.current_cols + 1:
                return True
        if placeTarget[1] <= self.current_cols:
            if par == self.current_cols - 1:
                return True
        return False

    def setPowerUpPictures(self):
        for obj in self.listOfObject:
            obj.listOfGhosts = [pygame.transform.scale(pygame.image.load("powerup.png"), (cell_size, cell_size))] * 4

    def returnToNormalSpirits(self):
        for obj in self.listOfObject:
            obj.listOfGhosts = [
                pygame.transform.scale(pygame.image.load("blue.png"), (cell_size, cell_size)),
                pygame.transform.scale(pygame.image.load("pink.png"), (cell_size, cell_size)),
                pygame.transform.scale(pygame.image.load("orange.png"), (cell_size, cell_size)),
                pygame.transform.scale(pygame.image.load("red.png"), (cell_size, cell_size))
            ]

    def powerUpFunc(self, pacman):
        if pacman.powerUp():
            self.start_time = pygame.time.get_ticks()  # Pobierz czas rozpoczęcia mocy power-up
            self.setPowerUpPictures()
            self.powerup = True
            self.powerUpForEach(True)

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time  # Oblicz upływający czas od rozpoczęcia mocy power-up
        if elapsed_time > POWER_UP_DURATION:
            self.returnToNormalSpirits()
            self.powerup = False
            self.powerUpForEach(False)

    def powerUpForEach(self, logic):
        for x in self.listOfObject:
            x.powerup = logic

    def normalMove(self, screen, board, font, pacman, ghost):
        ghost.powerUpFunc(pacman)

        pos = ["left", "right", "up", "down"]

        if pos[self.rand] == "left":
            self.x = -1
            self.y = 0
        if pos[self.rand] == "right":
            self.x = 1
            self.y = 0
        if pos[self.rand] == "up":
            self.y = -1
            self.x = 0
        if pos[self.rand] == "down":
            self.y = 1
            self.x = 0

        if self.collision(self.current_rows + self.y, self.current_cols + self.x):
            if pos[self.rand] == "left":
                self.current_cols += self.x
            if pos[self.rand] == "right":
                self.current_cols += self.x
            if pos[self.rand] == "up":
                self.current_rows += self.y
            if pos[self.rand] == "down":
                self.current_rows += self.y
        else:
            self.rand = random.randint(0, len(pos) - 1)

    def collision(self, curR, curC):  # 4 3 9
        if (boards[curR][curC] != 4 and boards[curR][curC] != 3 and boards[curR][curC] != 9 and boards[curR][curC] != 7 and boards[curR][curC] != 8 and boards[curR][curC] != 5 and boards[curR][curC] != 6):
            return True
        else:
            return False

    def Increment(self, rand):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < self.move_delay:
            return

        self.last_move_time = current_time
        if self.collision_free[rand] == "left":
            self.current_cols -= 1
        if self.collision_free[rand] == "right":
            self.current_cols += 1
        if self.collision_free[rand] == "up":
            self.current_rows -= 1
        if self.collision_free[rand] == "down":
            self.current_rows += 1
