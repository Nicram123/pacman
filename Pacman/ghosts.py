from pacman.constants import cell_size, num1, num2, POWER_UP_DURATION
import pygame
import random
from pacman.board import boards
from collections import deque 





class Ghosts():
    def __init__(self, current_rows=0, current_cols=0):

        self.current_rows = current_rows
        self.current_cols = current_cols
        self.listOfObject = [] 
        
    
        
        
        self.listOfGhosts = [
            pygame.transform.scale(pygame.image.load("pictures/red.png"), (cell_size, cell_size)),
            #pygame.transform.scale(pygame.image.load("orange.png"), (cell_size, cell_size)), 
            #pygame.transform.scale(pygame.image.load("pink.png"), (cell_size, cell_size)),
            #pygame.transform.scale(pygame.image.load("blue.png"), (cell_size, cell_size)),
            #pygame.transform.scale(pygame.image.load("red.png"), (cell_size, cell_size))
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
        
        
        

    def killingGhostByPacman(self, pacman, screen, font, obj, placeTarget, is_reward=False):
        ghost = self.collisionWithPacman(pacman)[1]  # ghost z ktorym kolizja 
        ix = self.collisionWithPacman(pacman)[2] # indeks gdzie ten duch leży 
        if ghost != None and ghost.powerup == True:
            if ghost != None:
                self.listOfObject.pop(ix) 
                if hasattr(ghost, "color") and ghost.color == 'red':  
                    obj = Blinky(11, 13) 
                #elif hasattr(ghost, "color") and ghost.color == 'pink': 
                #    obj = Pinky(11, 13)
                #elif hasattr(ghost, "color") and ghost.color == 'blue':
                #    obj = Inky(11, 13) 
                #elif hasattr(ghost, "color") and ghost.color == 'orange':
                #    obj = Clyde(11, 13) 
                #else: 
                #    obj = Ghosts(11, 13)
                self.listOfObject.insert(ix, obj)
                reward = 0 # 200
                if is_reward: 
                    return reward
        if is_reward: 
            return 0 
                

    def returningToTheGateAfterCollision(self, pacman, screen, font, ghost, board, pacmanBoard, flag=True, is_reward=False): 
        reward = 0 
        if self.collisionWithPacman(pacman)[0]: # True, ghst, ix 
            self.listOfObject.clear()
            pacman.lifePoints -= 1
            reward = -100 # -500
            if pacman.lifePoints > -1:
                pacman.lifes.pop(-1)
            pacman.current_rows = 23
            pacman.current_cols = 12
            
            self.create_ghost_object(screen, flag)
            ghost.leafingTheCage(board, screen, pacmanBoard, pacman, font, flag)
            
        if self.ifLifePointLessThenZero(pacman, screen, font):
            if flag:
                self.text_ = "Game over"
                text = font.render(self.text_, True, (255, 0, 0))
                screen.blit(text, (335, 350))
         
        if is_reward: 
            return reward     
    def checkIfGameOver(self):
      if self.text_ == "Game over":
        return True

    def ifLifePointLessThenZero(self, pacman, screen, font):
        if pacman.lifePoints < 0:
            return True

    def collisionWithPacman(self, pacman):
        for ix, ghost in enumerate(self.listOfObject):
            if ghost.current_rows == pacman.current_rows and ghost.current_cols == pacman.current_cols:
                #print(f'pacman ({pacman.current_rows}, {pacman.current_cols}),  ghost ({ghost.current_rows}, {ghost.current_cols})')
                return (True, ghost, ix)
        return (False, None, None)

    def create_ghost_object(self, screen, flag=True): 
        for x in range(len(self.listOfGhosts)):
            if x == 0: # 0 
                obj = Blinky(15, 12)    
            #elif x == 1: 
            #    obj = Pinky(15, 15)
            #elif x == 1:
            #    obj = Inky(15, 14) 
            #elif x == 1:
            #    obj = Clyde(15, 13) 
            
            self.listOfObject.append(obj) 
            if flag:
                screen.blit(self.listOfGhosts[x], (obj.current_cols * num2 + (0.1 * num2), obj.current_rows * num1 + (0.1 * num1)))        
       
        
    def displayGhosts(self, screen, ix):
        screen.blit(self.listOfGhosts[ix], (self.current_cols * num2 + (0.1 * num2), self.current_rows * num1 + (0.1 * num1)))

            
    def displayGhostsAll(self, screen, flag): 
        for ix, obj in enumerate(self.listOfObject): 
            obj.current_rows -= 1
        if flag:
            for ix, obj in enumerate(self.listOfObject): 
                screen.blit(self.listOfGhosts[ix], (obj.current_cols * num2 + (0.1 * num2), obj.current_rows * num1 + (0.1 * num1)))
    
    def leafingTheCage(self, board, screen, pacmanBoard, pacman, font, flag=True):
        # Wychodzimy z klatki stopniowo (3 pola do góry)
        steps = 3
        for _ in range(steps):
            if flag:
                screen.fill("black")
                pygame.time.delay(100)  # małe opóźnienie dla animacji
                board.draw_board(screen, pacmanBoard, pacman, font)
            self.displayGhostsAll(screen, flag)
            if flag:
                pygame.display.update()
                pygame.time.delay(100)
        
        self.CageWasLeft = True

    def freeGhosts(self, screen, board, font, pacman, pacmanBoard, ghost, flag = True):
        # screen, obj, font ,pacman, pacmanBoard, ghost 
        colors = []
        if ghost.CageWasLeft == False:
            ghost.leafingTheCage(board, screen, pacmanBoard, pacman, font, flag)
        blinky = self.listOfObject[-1]
        for ix, obj in enumerate(self.listOfObject):
            if hasattr(obj, "color") and obj.color == 'red':
                obj.move(pacman, pacmanBoard, ghost)
            elif hasattr(obj, "color") and obj.color == 'orange': 
                obj.move(pacman, pacmanBoard, ghost)
            elif hasattr(obj, "color") and obj.color == 'blue':
                obj.move(pacman, blinky ,pacmanBoard, ghost)
            elif hasattr(obj, "color") and obj.color == 'pink':
                obj.move(pacman, pacmanBoard, ghost)
            if flag: 
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
            obj.listOfGhosts = [pygame.transform.scale(pygame.image.load("pictures/powerup.png"), (cell_size, cell_size))] * 4

    def returnToNormalSpirits(self):
        for obj in self.listOfObject:
            obj.listOfGhosts = [
                pygame.transform.scale(pygame.image.load("pictures/red.png"), (cell_size, cell_size)), 
                #pygame.transform.scale(pygame.image.load("orange.png"), (cell_size, cell_size)),
                #pygame.transform.scale(pygame.image.load("pink.png"), (cell_size, cell_size)),
                #pygame.transform.scale(pygame.image.load("blue.png"), (cell_size, cell_size)),
                #pygame.transform.scale(pygame.image.load("red.png"), (cell_size, cell_size))
                
            ] 
            
    def get_escape_direction_bfs(self, ghost, pacman, board):
        rows, cols = len(board), len(board[0])
        start = (ghost.current_rows, ghost.current_cols)
        visited = set([start])
        queue = deque([start])
        best_pos = start
        best_dist = abs(start[0] - pacman.current_rows) + abs(start[1] - pacman.current_cols)

        while queue:
            r, c = queue.popleft()

            # Oblicz dystans od Pac-Mana
            dist = abs(r - pacman.current_rows) + abs(c - pacman.current_cols)
            if dist > best_dist:
                best_dist = dist
                best_pos = (r, c)

            # Sprawdź sąsiednie pola
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if board[nr][nc] not in [3,4,5,6,7,8,9] and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append((nr, nc))

        return best_pos




    def powerUpFunc(self, pacman, board):
        reward = 0 
        if pacman.powerUp(board):
            reward = reward + 5 
            print('reward +5 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            board[pacman.current_rows][pacman.current_cols] = 0 
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
        return reward 

    def powerUpForEach(self, logic):
        for x in self.listOfObject:
            x.powerup = logic

    def normalMove(self, screen, board, font, pacman, ghost):
        # ghost.powerUpFunc(pacman)

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
    
    def bfs(self, board, start, goal):
        rows, cols = len(board), len(board[0])
        queue = deque([(start, [])])
        visited = set([start])
        while queue:
            (r, c), path = queue.popleft() # duch (r, c) , [] 
            if (r, c) == goal:
                return path
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if board[nr][nc] not in [3,4,5,6,7,8,9]:
                        if (nr, nc) not in visited:
                            queue.append(((nr, nc), path + [(nr, nc)]))
                            visited.add((nr, nc))
        return []
            

# 14:36 
class Inky(Ghosts):
    def __init__(self, x, y):
        super().__init__()
        self.color = 'blue'
        self.current_rows = x
        self.current_cols = y
        self.path = []
        self.step_index = 0
        self.move_timer = 0
        self.speed = 1  # średnia prędkość
        

    

    def update_target(self, pacman, blinky, board):
        keys = pacman.keys  # ScancodeWrapper
        
        if keys[pygame.K_UP]:
            look_ahead = (pacman.current_rows - 2, pacman.current_cols)
        elif keys[pygame.K_DOWN]:
            look_ahead = (pacman.current_rows + 2, pacman.current_cols)
        elif keys[pygame.K_LEFT]:
            look_ahead = (pacman.current_rows, pacman.current_cols - 2)
        elif keys[pygame.K_RIGHT]:
            look_ahead = (pacman.current_rows, pacman.current_cols + 2)
        else:
            look_ahead = (pacman.current_rows, pacman.current_cols)

        # Oblicz wektor od Blinky’ego do tego punktu
        dx = look_ahead[0] - blinky.current_rows
        dy = look_ahead[1] - blinky.current_cols

        # Target to punkt dwa razy dalej
        target = (look_ahead[0] + dx, look_ahead[1] + dy)

        # Ograniczenie, żeby nie wychodził poza planszę
        rows, cols = len(board), len(board[0])
        r, c = target
        self.target = (max(0, min(rows - 1, r)), max(0, min(cols - 1, c)))

    def move(self, pacman, blinky, board, ghost):
        self.move_timer += 1
        
        if True or ghost.powerup == False:
            if self.move_timer % 5 == 0 or not self.path:
                self.update_target(pacman, blinky, board)
                start = (self.current_rows, self.current_cols)
                self.path = self.bfs(board, start, self.target)
                self.step_index = 0

            if self.path and self.step_index < len(self.path):
                if self.move_timer % self.speed == 0:
                    next_tile = self.path[self.step_index]
                    self.current_rows, self.current_cols = next_tile
                    self.step_index += 1        
        #else:
        #    if self.move_timer % self.speed == 0:
        #        # Znajdź najlepsze pole do ucieczki
        #        escape_target = self.get_escape_direction_bfs(ghost=self, pacman=pacman, board=board)
        #        start = (self.current_rows, self.current_cols)
        #        # Użyj BFS do wygenerowania ścieżki do tego punktu
        #        self.path = self.bfs(board, start, escape_target)
        #        self.step_index = 0
        #        if self.path:
        #            next_tile = self.path[self.step_index]
        #            self.current_rows, self.current_cols = next_tile
        #            self.step_index += 1

            
class Clyde(Ghosts):
    def __init__(self, x, y):
        super().__init__()
        self.color = 'orange'
        self.current_rows = x
        self.current_cols = y
        self.path = []
        self.step_index = 0
        self.move_timer = 0
        self.corner = (27, 0)  # np. dolny lewy róg
        self.speed = 2  # najwolniejszy

    def distance(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])  # dystans Manhattan

    def update_target(self, pacman):
        dist = self.distance((self.current_rows, self.current_cols),
                             (pacman.current_rows, pacman.current_cols))
        if dist > 8:
            # Goni Pac-Mana
            self.target = (pacman.current_rows, pacman.current_cols)
        else:
            # Ucieka w róg
            self.target = self.corner



    def move(self, pacman, board, ghost):
        self.move_timer += 1
        
        if True or ghost.powerup == False:
            # Aktualizuj target co klatkę i BFS co 1-2 klatki
            if not self.path or self.move_timer % 2 == 0:
                self.update_target(pacman)
                start = (self.current_rows, self.current_cols)
                self.path = self.bfs(board, start, self.target)
                self.step_index = 0

            # Poruszaj się po ścieżce co 1-2 klatki
            if self.path and self.step_index < len(self.path):
                if self.move_timer % self.speed == 0:
                    next_tile = self.path[self.step_index]
                    self.current_rows, self.current_cols = next_tile
                    self.step_index += 1
                    
        
        #else:
        #    # W trybie ucieczki duch ucieka od Pac-Mana
        #    if self.move_timer % self.speed == 0:
        #        # Znajdź najlepsze pole do ucieczki
        #        escape_target = self.get_escape_direction_bfs(ghost=self, pacman=pacman, board=board)
        #        start = (self.current_rows, self.current_cols)
        #        # Użyj BFS do wygenerowania ścieżki do tego punktu
        #        self.path = self.bfs(board, start, escape_target)
        #        self.step_index = 0
        #
        #        # Jeśli ścieżka istnieje, wykonaj ruch
        #        if self.path:
        #            next_tile = self.path[self.step_index]
        #            self.current_rows, self.current_cols = next_tile
        #            self.step_index += 1
                    



   


            
class Pinky(Ghosts): 
 
  def __init__(self, x, y): 
        super().__init__() 
        self.current_rows = x 
        self.current_cols = y 
        self.color = 'pink' 
        self.target = (x, y)
        self.path = []
        self.step_index = 0
        self.move_timer = 0
        self.speed = 2  # trochę wolniejsza

        
  def update_target(self, pacman, board):
        rows, cols = len(board), len(board[0])
        if pacman.keys[pygame.K_UP]:
            target = (pacman.current_rows - 4, pacman.current_cols)
        elif pacman.keys[pygame.K_DOWN]:
            target = (pacman.current_rows + 4, pacman.current_cols)
        elif pacman.keys[pygame.K_LEFT]:
            target = (pacman.current_rows, pacman.current_cols - 4)
        elif pacman.keys[pygame.K_RIGHT]:
            target = (pacman.current_rows, pacman.current_cols + 4)
        else:
            target = (pacman.current_rows, pacman.current_cols)
        r, c = target
        self.target = (max(0, min(rows - 1, r)), max(0, min(cols - 1, c)))
        
  def move(self, pacman, board, ghost):
        self.update_target(pacman, board)
        start = (self.current_rows, self.current_cols)
        self.move_timer += 1
        
        if True or ghost.powerup == False: 
            # Co kilka klatek przelicz BFS
            if self.move_timer % 2 == 0 or not self.path:
                self.path = self.bfs(board, start, self.target)
                self.step_index = 0

            if self.path and self.step_index < len(self.path): 
                if self.move_timer % self.speed == 0:
                    next_tile = self.path[self.step_index]
                    self.current_rows, self.current_cols = next_tile
                    self.step_index += 1
        #else:
        #    if self.move_timer % self.speed == 0:
        #        # Znajdź najlepsze pole do ucieczki
        #        escape_target = self.get_escape_direction_bfs(ghost=self, pacman=pacman, board=board)
        #        start = (self.current_rows, self.current_cols)
        #        # Użyj BFS do wygenerowania ścieżki do tego punktu
        #        self.path = self.bfs(board, start, escape_target)
        #        self.step_index = 0
        #        if self.path:
        #            next_tile = self.path[self.step_index]
        #            self.current_rows, self.current_cols = next_tile
        #            self.step_index += 1


class Blinky(Ghosts): 
  def __init__(self, x, y): 
    super().__init__()
    self.current_rows = x 
    self.current_cols = y 
    self.color = 'red'
    self.path = []
    self.step_index = 0
    self.move_timer = 0
    self.speed = 1
  
  def update_target(self, pacman): 
    self.target = (pacman.current_rows, pacman.current_cols)  
    

 
  
      
  def move(self, pacman, board, ghost):
        temp = ghost.powerUpFunc(pacman, board)
        self.update_target(pacman) 
        self.move_timer += 1
        if True or ghost.powerup == False: 
            # Co 10 klatek planuj nową ścieżkę
            if self.move_timer % 10 == 0 or not self.path:
                start = (self.current_rows, self.current_cols)
                self.path = self.bfs(board, start, self.target)
                self.step_index = 0

            # Jeśli jest ścieżka - idź po niej krok po kroku
            if self.path and self.step_index < len(self.path):
                if self.move_timer % self.speed == 0:
                    next_tile = self.path[self.step_index]
                    self.current_rows, self.current_cols = next_tile = next_tile
                    self.step_index += 1
                    
        #else:
        #    if self.move_timer % self.speed == 0:
        #        # Znajdź najlepsze pole do ucieczki
        #        escape_target = self.get_escape_direction_bfs(ghost=self, pacman=pacman, board=board)
        #        start = (self.current_rows, self.current_cols)
        #        # Użyj BFS do wygenerowania ścieżki do tego punktu
        #        self.path = self.bfs(board, start, escape_target)
        #        self.step_index = 0
        #        if self.path:
        #            next_tile = self.path[self.step_index]
        #            self.current_rows, self.current_cols = next_tile
        #            self.step_index += 1