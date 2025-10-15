import pygame
from pacman.board import boards
from pacman.generateBoard import Board
from pacman.constants import HEIGHT, WIDTH
from pacman.pac import Pacman
from pacman.ghosts import Ghosts
from tensorflow.keras.models import load_model
import numpy as np
import copy 
from train.neural_network import PacmanEnv


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

env = PacmanEnv()

# 2600 the best 
q_network = load_model(r"C:\Users\marci\pacman\Pacman\models4\pacman_ai_ep2600.keras", compile=False)
while run:
    timer.tick(fps)
    screen.fill('black')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # --- WYBÓR AKCJI ---
    # Stan z poprzedniej klatki
    rows, cols = len(pacmanBoard), len(pacmanBoard[0])
    max_dist = rows + cols
    
    #print(f'{np.sum(np.isin(pacmanBoard, [0]))},  {np.sum(np.isin(pacmanBoard, [1,2]))}')

    dy_pacman_blinky = pacman.current_rows - ghost.listOfObject[0].current_rows
    dx_pacman_blinky = pacman.current_cols - ghost.listOfObject[0].current_cols
    #dy_pacman_pinky = pacman.current_rows - ghost.listOfObject[1].current_rows
    #dx_pacman_pinky = pacman.current_cols - ghost.listOfObject[1].current_cols
    #dy_pacman_inky = pacman.current_rows - ghost.listOfObject[0].current_rows
    #dx_pacman_inky = pacman.current_cols - ghost.listOfObject[0].current_cols
    #dy_pacman_clyde = pacman.current_rows - ghost.listOfObject[2].current_rows
    #dx_pacman_clyde = pacman.current_cols - ghost.listOfObject[2].current_cols
    
    #dy_pacman_blinky = 0
    #dx_pacman_blinky = 0
    dy_pacman_pinky = 0
    dx_pacman_pinky = 0
    dy_pacman_inky = 0
    dx_pacman_inky = 0 
    dy_pacman_clyde = 0
    dx_pacman_clyde = 0

    dist_to_nearest_dot, nearest_dot_dx, nearest_dot_dy, dot_type = env.bfs_nearest_dot(pacmanBoard, (pacman.current_rows, pacman.current_cols))
    dist_to_nearest_ghost = env.dist_to_nearest_ghost_bfs(pacmanBoard, pacman, ghost)
    #dist_to_nearest_ghost = len(boards) + len(boards)

    can_left  = 1.0 if pacman.collision(pacman.current_rows, pacman.current_cols - 1) else 0.0
    can_right = 1.0 if pacman.collision(pacman.current_rows, pacman.current_cols + 1) else 0.0
    can_up    = 1.0 if pacman.collision(pacman.current_rows - 1, pacman.current_cols) else 0.0
    can_down  = 1.0 if pacman.collision(pacman.current_rows + 1, pacman.current_cols) else 0.0

    is_dot_here = 1 if pacmanBoard[pacman.current_rows][pacman.current_cols] == 1 else 0
    is_power_pellet_here = 1 if pacmanBoard[pacman.current_rows][pacman.current_cols] == 2 else 0
    is_scared_mode = 1 if ghost.powerup else 0
    #is_scared_mode = 0

    state = np.array([
        dx_pacman_blinky / cols,
        dy_pacman_blinky / rows,
        dx_pacman_pinky / cols,
        dy_pacman_pinky / rows,
        dx_pacman_inky / cols,
        dy_pacman_inky / rows,
        dx_pacman_clyde / cols,
        dy_pacman_clyde / rows,
        dist_to_nearest_dot / max_dist,
        nearest_dot_dx / cols,
        nearest_dot_dy / rows,
        dist_to_nearest_ghost / max_dist,
        is_dot_here,
        is_power_pellet_here,
        is_scared_mode,
        can_left,
        can_right,
        can_up,
        can_down
    ], dtype=np.float32)


    state = np.expand_dims(state, axis=0)
    q_values = q_network(state)
    action = np.argmax(q_values[0])
    
    
    #ghost.killingGhostByPacman(pacman, screen, font, obj, (13, 14))
    #ghost.returningToTheGateAfterCollision(pacman, screen, font, ghost, obj, pacmanBoard)

    # --- 1️⃣ najpierw Pacman się rusza ---
    #pacman.incrementicTrafficParametersRL(action)
    #ghost.killingGhostByPacman(pacman, screen, font, obj, (13, 14))
    #ghost.returningToTheGateAfterCollision(pacman, screen, font, ghost, obj, pacmanBoard)
    # --- 2️⃣ dopiero teraz duchy ---
    #ghost.freeGhosts(screen, obj, font, pacman, pacmanBoard, ghost)
    # --- 3️⃣ punkty / kolizje / śmierć ---
    #pacman.increasePoints(screen, font, pacmanBoard)
    #ghost.killingGhostByPacman(pacman, screen, font, obj, (13, 14))
    #ghost.returningToTheGateAfterCollision(pacman, screen, font, ghost, obj, pacmanBoard)
    
    
    
    
    # --- 1️⃣ Pacman się rusza ---
    pacman.incrementicTrafficParametersRL(action)
    # --- 2️⃣ Punkty / powerup / kolizje ---
    
    
    _ = ghost.powerUpFunc(pacman, pacmanBoard)
    pacman.increasePoints(screen, font, pacmanBoard)
    

    
    
    ghost.killingGhostByPacman(pacman, screen, font, obj, (13, 14))
    ghost.returningToTheGateAfterCollision(pacman, screen, font, ghost, obj, pacmanBoard)
    
    # --- 3️⃣ Ruch duchów ---
    ghost.freeGhosts(screen, obj, font, pacman, pacmanBoard, ghost)
    # --- 4️⃣ Kolizje po ruchu duchów ---
    ghost.killingGhostByPacman(pacman, screen, font, obj, (13, 14))
    ghost.returningToTheGateAfterCollision(pacman, screen, font, ghost, obj, pacmanBoard)
    #ghost.killingGhostByPacman(pacman, screen, font, obj, (13, 14))
    
    
    
    

    # --- 4️⃣ aktualizacja stanu po ruchu ---
    # jeśli Pacman zebrał wszystko – reset planszy
    if pacman.ifAllPointsCollected(pacmanBoard):
        pacmanBoard = copy.deepcopy(boards)
        ghost.listOfObject.clear()
        ghost.create_ghost_object(screen)
        ghost.leafingTheCage(obj, screen, pacmanBoard, pacman, font)
    # --- 5️⃣ rysowanie ---
    obj.draw_board(screen, pacmanBoard, pacman, font)
    pacman.move(screen)
    
    #ghost.killingGhostByPacman(pacman, screen, font, obj, (13, 14))
    #ghost.returningToTheGateAfterCollision(pacman, screen, font, ghost, obj, pacmanBoard)
    
    pygame.display.flip()

    if ghost.checkIfGameOver():
        break

pygame.quit()