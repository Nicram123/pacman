# ---------- Sieć Q-learning + środowisko Pacmana ----------
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input
import numpy as np
import copy
from collections import deque
from pacman.board import boards
from pacman.generateBoard import Board
from pacman.ghosts import Ghosts
from pacman.pac import Pacman
from pacman.constants import WIDTH, HEIGHT


class PacmanEnv:
    def __init__(self, width=WIDTH, height=HEIGHT, difficulty="no_ghosts"):
        self.width = width
        self.height = height
        self.steps_without_progress = 0
        self.difficulty = difficulty  # "no_ghosts", "one_ghost", "full"

    # ---------- BFS: najbliższy duch ----------
    def dist_to_nearest_ghost_bfs(self, board, pacman, ghost):
        max_dist = len(board) + len(board[0])
        min_dist = max_dist
        for g in ghost.listOfObject:
            if not getattr(g, "isActive", True):
                continue
            path = ghost.bfs(board, (pacman.current_rows, pacman.current_cols),
                              (g.current_rows, g.current_cols))
            if path:
                min_dist = min(min_dist, len(path))
        return min_dist

    # ---------- BFS: najbliższa kropka ----------
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
                dot_type = 2 if board[r][c] == 2 else 1
                return dist, dx, dy, dot_type
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if board[nr][nc] not in [3,4,5,6,7,8,9] and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append((nr, nc, dist + 1))
        max_dist = rows + cols
        return max_dist, 0, 0, 0

    # ---------- RESET ----------
    def reset(self, screen, pacmanBoard):
        for attr in ["bonus_25", "bonus_50", "bonus_75", "bonus_90"]:
            if hasattr(self, attr):
                delattr(self, attr)

        pacmanBoard = copy.deepcopy(boards)
        obj = Board()
        ghost = Ghosts()
        pacman = Pacman(23, 12, 0)
        ghost.create_ghost_object(screen, flag=False)

        # tryb uczenia stopniowego
        if self.difficulty == "no_ghosts":
            for g in ghost.listOfObject:
                g.isActive = False
        elif self.difficulty == "one_ghost":
            for i, g in enumerate(ghost.listOfObject):
              
                g.isActive = (i == 0)  # czerwony
        else:
            for g in ghost.listOfObject:
                g.isActive = True

        self.steps_without_progress = 0
        self.update_state_vars(pacman, ghost, pacmanBoard)
        self.start_number_point = np.sum(np.isin(pacmanBoard, [1, 2]))

        return self._make_state(pacmanBoard), pacman, ghost, obj, pacmanBoard

    # ---------- STEP ----------
    def step(self, screen, font, action, pacmanBoard, pacman, ghost, obj):
        reward = -0.01
        done = False
        self.steps_without_progress += 1

        old_row, old_col = pacman.current_rows, pacman.current_cols
        old_dist_to_dot = self.dist_to_nearest_dot
        old_dist_to_ghost = self.dist_to_nearest_ghost

        # sprawdź, czy ruch możliwy
        action_possible = False
        if action == 0 and pacman.collision(pacman.current_rows, pacman.current_cols - 1): action_possible = True
        if action == 1 and pacman.collision(pacman.current_rows, pacman.current_cols + 1): action_possible = True
        if action == 2 and pacman.collision(pacman.current_rows - 1, pacman.current_cols): action_possible = True
        if action == 3 and pacman.collision(pacman.current_rows + 1, pacman.current_cols): action_possible = True

        pacman.incrementicTrafficParametersRL(action, False)
        moved = (pacman.current_rows, pacman.current_cols) != (old_row, old_col)

        # kary za brak ruchu / ścianę
        if not moved:
            reward -= 0.3 if not action_possible else 0.1
            print('sciana/brak ruchu')
        else:
            self.steps_without_progress = 0
            
        
        # przniosłem na górę 
        temp2 = 0
        temp = 0
        if self.difficulty != "no_ghosts":
            temp2 = ghost.powerUpFunc(pacman, pacmanBoard)
            
        temp = pacman.increasePoints(screen, font, pacmanBoard, flag=False, is_reward=True)
        reward += temp2
        

        if temp2 == 5:
            print('POWERUP zjedzony!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        if temp > 0:
            reward += temp
            
        # dodałem 
        temp = 0
        temp2 = 0
        if self.difficulty != "no_ghosts":
            temp += ghost.killingGhostByPacman(pacman, screen, font, obj, (13, 14), is_reward=True) # zawsze 0 zwraca 
            temp += ghost.returningToTheGateAfterCollision(pacman, screen, font, ghost, obj, pacmanBoard,
                                                           flag=False, is_reward=True) 
            if temp == -100:
                reward -= 100
                print('-100 (po ruchu pacmana)')
                done = True
            
        # ruch duchów (tylko w trybie z duchami)
        if self.difficulty != "no_ghosts":
            ghost.freeGhosts(screen, obj, font, pacman, pacmanBoard, ghost, flag=False)
            print(f'+{temp} (dot)')
        
        
            
        # duchy – kara za śmierć
        temp = 0
        if not done and self.difficulty != "no_ghosts":
            temp += ghost.killingGhostByPacman(pacman, screen, font, obj, (13, 14), is_reward=True) # zawsze 0 
            temp += ghost.returningToTheGateAfterCollision(pacman, screen, font, ghost, obj, pacmanBoard,
                                                           flag=False, is_reward=True) 
            if temp == -100:
                reward -= 100
                print('-100 (po ruchu duchów)')
                done = True

        # zakończenie planszy
        if pacman.ifAllPointsCollected(pacmanBoard):
            reward += 500
            print('+500 ALL COLLECTED !!!!!!!!!!!')
            done = True

        # aktualizacja
        self.update_state_vars(pacman, ghost, pacmanBoard)

        # progres ku kropce
        new_dist_to_dot = self.dist_to_nearest_dot
        delta_dot = old_dist_to_dot - new_dist_to_dot
        reward += 0.1 * delta_dot

        # unikanie duchów
        if self.difficulty != "no_ghosts":
            new_dist_to_ghost = self.dist_to_nearest_ghost_bfs(pacmanBoard, pacman, ghost)
            delta_ghost = new_dist_to_ghost - old_dist_to_ghost
            if not ghost.powerup:
                reward += 0.2 * delta_ghost  # większy dystans = lepiej (unikaj duchów)
            else:
                # W trybie powerup Pac-Man ignoruje duchy, skupia się na kropkach
                reward += 0.05 * (old_dist_to_dot - new_dist_to_dot)
                if moved:
                    reward += 0.05  # mała nagroda za aktywność
                else:
                    reward -= 0.2   # kara za stanie w miejscu
            self.dist_to_nearest_ghost = new_dist_to_ghost

        # brak progresu
        if self.steps_without_progress > 200:
            reward -= 10
            print('brak progresu')
            done = True
        
       
        # bonusy za progres
        reward = self._reward_progress(pacmanBoard, reward)

        return self._make_state(pacmanBoard), reward, done, pacmanBoard

    # ---------- Pomocnicze ----------
    def _reward_progress(self, pacmanBoard, reward):
        remaining = np.sum(np.isin(pacmanBoard, [1, 2]))
        progress = 1 - (remaining / self.start_number_point)
        for threshold, bonus, name in [(0.25, 50, "bonus_25"),
                                       (0.5, 150, "bonus_50"),
                                       (0.75, 250, "bonus_75"),
                                       (0.9, 500, "bonus_90")]:
            if progress >= threshold and not hasattr(self, name):
                setattr(self, name, True) 
                print(f'🎯 BONUS {int(threshold*100)}%  -> +{bonus}')
                reward += bonus
        return reward

    def _make_state(self, pacmanBoard):
        rows, cols = len(pacmanBoard), len(pacmanBoard[0])
        max_dist = rows + cols
        return np.array([
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
            self.is_scared_mode,
            self.can_left,
            self.can_right,
            self.can_up,
            self.can_down
        ], dtype=np.float32)

    def update_state_vars(self, pacman, ghost, board):
        print(f"Powerup: {ghost.powerup}")
        if self.difficulty == "no_ghosts":
            # neutralizuj cechy duchów
            self.dist_to_nearest_ghost = len(board) + len(board[0])
            self.dx_pacman_blinky = self.dy_pacman_blinky = 0
            self.dx_pacman_pinky = self.dy_pacman_pinky = 0
            self.dx_pacman_inky = self.dy_pacman_inky = 0
            self.dx_pacman_clyde = self.dy_pacman_clyde = 0
            self.is_scared_mode = 0
        else:
            # relacje z duchami
            # relacje Pacmana z duchami (sprawdź, czy duch aktywny)
            for i, name in enumerate(["blinky"]): # "inky" 
                g = ghost.listOfObject[i]
                if getattr(g, "isActive", True):
                    setattr(self, f"dy_pacman_{name}", pacman.current_rows - g.current_rows)
                    setattr(self, f"dx_pacman_{name}", pacman.current_cols - g.current_cols)
                    self.dx_pacman_pinky = self.dy_pacman_pinky = 0
                    self.dx_pacman_clyde = self.dy_pacman_clyde = 0
                    self.dx_pacman_inky = self.dy_pacman_inky = 0
                else:
                    setattr(self, f"dy_pacman_{name}", 0)
                    setattr(self, f"dx_pacman_{name}", 0)

            self.dist_to_nearest_ghost = self.dist_to_nearest_ghost_bfs(board, pacman, ghost)
            self.is_scared_mode = 1 if ghost.powerup else 0

        # cechy lokalne
        self.is_dot_here = 1 if board[pacman.current_rows][pacman.current_cols] == 1 else 0
        self.is_power_pellet_here = 1 if board[pacman.current_rows][pacman.current_cols] == 2 else 0
        self.dist_to_nearest_dot, self.nearest_dot_dx, self.nearest_dot_dy, self.dot_type = \
            self.bfs_nearest_dot(board, (pacman.current_rows, pacman.current_cols))

        self.can_left = 1.0 if pacman.collision(pacman.current_rows, pacman.current_cols - 1) else 0.0
        self.can_right = 1.0 if pacman.collision(pacman.current_rows, pacman.current_cols + 1) else 0.0
        self.can_up = 1.0 if pacman.collision(pacman.current_rows - 1, pacman.current_cols) else 0.0
        self.can_down = 1.0 if pacman.collision(pacman.current_rows + 1, pacman.current_cols) else 0.0


def build_q_network(state_size=19, num_actions=4):
    model = Sequential([
        Input((state_size,)),
        Dense(128, activation='relu'),
        Dense(128, activation='relu'),
        Dense(num_actions)
    ])
    return model
