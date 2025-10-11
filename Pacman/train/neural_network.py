import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input
from pacman.constants import WIDTH, HEIGHT
from random import randint
import numpy as np  
from pacman.generateBoard import Board 
from pacman.ghosts import Ghosts 
from collections import deque
from pacman.pac import Pacman 
import math 
from pacman.board import boards
import copy 


class PacmanEnv:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        
        
    def dist_to_nearest_ghost_bfs(self, board, pacman, ghost):
        max_dist = len(board) + len(board[0]) 
        min_dist = max_dist
        for g in ghost.listOfObject:
            path = ghost.bfs(board, (pacman.current_rows, pacman.current_cols),
                              (g.current_rows, g.current_cols))
            if path:
                min_dist = min(min_dist, len(path))
        return min_dist
      
    def bfs_nearest_dot(self, board, start):
        rows, cols = len(board), len(board[0])
        visited = set([start])
        queue = deque([(start[0], start[1], 0)])
        sr, sc = start
        while queue:
            r, c, dist = queue.popleft()
            if board[r][c] in [1, 2]:
                dx = c - sc
                dy = r - sr
                dot_type = 1 if board[r][c] == 2 else 2
                return dist, dx, dy, dot_type
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if board[nr][nc] not in [3,4,5,6,7,8,9] and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append((nr, nc, dist + 1))
        max_dist = rows + cols
        return max_dist, 0, 0, 0
        
    def reset(self, screen, pacmanBoard):
        # Pozycje paletek i piłki
        obj = Board()
        ghost = Ghosts()
        pacman = Pacman(23,12,0)
        ghost.create_ghost_object(screen, flag=False)
        self.steps_without_progress = 0
        # blue - inky, pink - pinky , orange - clyde, red - blinky 
        self.dy_pacman_blinky = pacman.current_rows - ghost.listOfObject[3].current_rows
        self.dx_pacman_blinky = pacman.current_cols - ghost.listOfObject[3].current_cols
        self.dy_pacman_pinky = pacman.current_rows - ghost.listOfObject[1].current_rows
        self.dx_pacman_pinky = pacman.current_cols - ghost.listOfObject[1].current_cols
        self.dy_pacman_inky = pacman.current_rows - ghost.listOfObject[0].current_rows
        self.dx_pacman_inky = pacman.current_cols - ghost.listOfObject[0].current_cols
        self.dy_pacman_clyde = pacman.current_rows - ghost.listOfObject[2].current_rows
        self.dx_pacman_clyde = pacman.current_cols - ghost.listOfObject[2].current_cols
        self.is_dot_here = 1 if pacmanBoard[pacman.current_rows][pacman.current_cols] == 1 else 0
        self.is_power_pellet_here = 1 if pacmanBoard[pacman.current_rows][pacman.current_cols] == 2 else 0
        self.dist_to_nearest_dot, self.nearest_dot_dx, self.nearest_dot_dy, self.dot_type = self.bfs_nearest_dot(pacmanBoard, (pacman.current_rows, pacman.current_cols))
        self.dist_to_nearest_ghost = self.dist_to_nearest_ghost_bfs(pacmanBoard, pacman, ghost)    
        if ghost.powerup == True:
          self.is_scared_mode = 1
        else: 
          self.is_scared_mode = 0                
        rows, cols = len(pacmanBoard), len(pacmanBoard[0])
        max_dist = rows + cols  
        state = np.array([
            self.dx_pacman_blinky / cols,
            self.dy_pacman_blinky / rows,
            self.dx_pacman_pinky / cols,
            self.dy_pacman_pinky / rows,
            self.dx_pacman_inky / cols,
            self.dy_pacman_inky / rows,
            self.dx_pacman_clyde / cols,
            self.dy_pacman_clyde / rows,
            self.dist_to_nearest_dot / max_dist,
            self.nearest_dot_dx / cols,
            self.nearest_dot_dy / rows,
            self.dist_to_nearest_ghost / max_dist,
            self.is_dot_here,
            self.is_power_pellet_here,
            self.is_scared_mode
        ], dtype=np.float32)
        return state, pacman, ghost, obj

    def step(self, screen, font, action, pacmanBoard, pacman, ghost, obj):
        # {'left': 0, 'right': 1, 'up': 2, 'down': 3} 
        reward = 0 
        done = False
        self.steps_without_progress += 1
        
        old_row, old_col = pacman.current_rows, pacman.current_cols
        old_dist_to_dot = self.dist_to_nearest_dot
        # poruszył się pacman  
        pacman.incrementicTrafficParametersRL(action)
        
        if (pacman.current_rows, pacman.current_cols) == (old_row, old_col):
          reward = reward -  10

        # za poruszanie się  
        reward = reward - 1 
        # ruch duchów 
        ghost.freeGhosts(screen, obj, font ,pacman, pacmanBoard,  ghost, flag=False)
        temp = pacman.increasePoints(screen, font, pacmanBoard, flag=False, is_reward=True)
        
        reward = reward + temp 
        temp = ghost.killingGhostByPacman(pacman, screen, font, obj, (13, 14), is_reward=True) 
        reward = reward + temp 
        temp = ghost.returningToTheGateAfterCollision(pacman, screen, font, ghost, obj, pacmanBoard, flag=False, is_reward=True) # ghost, obj, pacmanBoard
        if temp == -500: 
          done = True 
        reward = reward + temp 
        # czy zebrał wszystkie owoce (do tego dążymy to jest nasz cel)
        if pacman.ifAllPointsCollected(pacmanBoard):
          reward = reward + 1000 
          pacmanBoard = copy.deepcopy(boards) 
          done = True
          
        
        # odświeżenie wartości dla stanów 
        self.dy_pacman_blinky = pacman.current_rows - ghost.listOfObject[3].current_rows
        self.dx_pacman_blinky = pacman.current_cols - ghost.listOfObject[3].current_cols
        self.dy_pacman_pinky = pacman.current_rows - ghost.listOfObject[1].current_rows
        self.dx_pacman_pinky = pacman.current_cols - ghost.listOfObject[1].current_cols
        self.dy_pacman_inky = pacman.current_rows - ghost.listOfObject[0].current_rows
        self.dx_pacman_inky = pacman.current_cols - ghost.listOfObject[0].current_cols
        self.dy_pacman_clyde = pacman.current_rows - ghost.listOfObject[2].current_rows
        self.dx_pacman_clyde = pacman.current_cols - ghost.listOfObject[2].current_cols
        self.is_dot_here = 1 if pacmanBoard[pacman.current_rows][pacman.current_cols] == 1 else 0
        self.is_power_pellet_here = 1 if pacmanBoard[pacman.current_rows][pacman.current_cols] == 2 else 0
        self.dist_to_nearest_dot, self.nearest_dot_dx, self.nearest_dot_dy, self.dot_type = self.bfs_nearest_dot(pacmanBoard, (pacman.current_rows, pacman.current_cols))
        self.dist_to_nearest_ghost = self.dist_to_nearest_ghost_bfs(pacmanBoard, pacman, ghost)   
        
        
        new_dist_to_dot = self.dist_to_nearest_dot
        if new_dist_to_dot > old_dist_to_dot:
            reward = reward -  2
         
        if ghost.powerup == True:
          self.is_scared_mode = 1
        else: 
          self.is_scared_mode = 0   
          
          
        if pacmanBoard[pacman.current_rows][pacman.current_cols] == 1 or pacmanBoard[pacman.current_rows][pacman.current_cols] == 2:
          self.steps_without_progress = 0
          
        if self.steps_without_progress > 200: 
          reward -= 100
          done = True
          
        
        
        rows, cols = len(pacmanBoard), len(pacmanBoard[0])
        max_dist = rows + cols 
        # --- nowy stan ---
        state = np.array([
              self.dx_pacman_blinky / cols,
              self.dy_pacman_blinky / rows,
              self.dx_pacman_pinky / cols,
              self.dy_pacman_pinky / rows,
              self.dx_pacman_inky / cols,
              self.dy_pacman_inky / rows,
              self.dx_pacman_clyde / cols,
              self.dy_pacman_clyde / rows,
              self.dist_to_nearest_dot / max_dist,
              self.nearest_dot_dx / cols,
              self.nearest_dot_dy / rows,
              self.dist_to_nearest_ghost / max_dist,
              self.is_dot_here,
              self.is_power_pellet_here,
              self.is_scared_mode
          ], dtype=np.float32)
        return state, reward, done 

# --- Sieć Q-learning ---
def build_q_network(state_size=15, num_actions=4):
    model = Sequential([
        Input((state_size,)),
        Dense(64, activation='relu'),
        Dense(64, activation='relu'),
        Dense(num_actions)
    ])
    return model