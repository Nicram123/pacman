import numpy as np
import random
from collections import deque
import time
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import Huber
from train.neural_network import build_q_network, PacmanEnv
from pacman.board import boards
import copy
from tensorflow.keras.models import load_model


# --- inicjalizacja ---
screen, font = None, None
env = PacmanEnv(difficulty="no_ghosts")  # start bez duchów
pacmanBoard = copy.deepcopy(boards)
state, pacman, ghost, obj, pacmanBoard = env.reset(screen, pacmanBoard)

# --- Hyperparametry ---
ALPHA = 0.0015
GAMMA = 0.98
EPSILON = 1.0

EPSILON_DECAY = 0.997
EPSILON_MIN = 0.05
BATCH_SIZE = 64
MEMORY_SIZE = 80000
MAX_STEPS = 2000 # 2000 # 300
NUM_EPISODES = 5000

EPSILON = max(EPSILON_MIN, EPSILON * (EPSILON_DECAY ** 2600))
print(f"Kontynuacja nauki od epizodu 2600, epsilon startowy: {EPSILON:.4f}")
# --- Sieci ---
state_size = 19
num_actions = 4

#q_network = build_q_network(state_size, num_actions)
#target_q_network = build_q_network(state_size, num_actions)
#optimizer = Adam(learning_rate=ALPHA)
#q_network.compile(optimizer=optimizer, loss=Huber())
#target_q_network.compile(optimizer=optimizer, loss=Huber())
#target_q_network.set_weights(q_network.get_weights())
#memory = deque(maxlen=MEMORY_SIZE)


checkpoint_path = "models_final/pacman_ai_ep2600.keras"
q_network = load_model(checkpoint_path, compile=False)
target_q_network = load_model(checkpoint_path, compile=False)
# Skonfiguruj optymalizator i loss (bo compile=False)
optimizer = Adam(learning_rate=ALPHA)
q_network.compile(optimizer=optimizer, loss=Huber())
target_q_network.compile(optimizer=optimizer, loss=Huber())
# Upewnij się, że target_q_network ma te same wagi
target_q_network.set_weights(q_network.get_weights())
memory = deque(maxlen=MEMORY_SIZE)


# --- epsilon-greedy ---
def get_action(state, epsilon):
    if np.random.rand() < epsilon:
        return np.random.randint(num_actions)
    q_values = q_network(np.expand_dims(state, axis=0))
    return np.argmax(q_values[0].numpy())

# --- Replay ---
def replay():
    if len(memory) < BATCH_SIZE:
        return None
    batch = random.sample(memory, BATCH_SIZE)
    states, targets = [], []
    for state, action, reward, next_state, done in batch:
        target = q_network(np.expand_dims(state, axis=0))[0].numpy()
        if done:
            target[action] = reward
        else:
            q_future = np.max(target_q_network(np.expand_dims(next_state, axis=0))[0].numpy())
            target[action] = reward + GAMMA * q_future
        states.append(state)
        targets.append(target)
    return q_network.train_on_batch(np.array(states), np.array(targets))

def same(pacmanBoard): 
    for i, x in enumerate(boards): 
        for j, y in enumerate(x): 
            if boards[i][j] == pacmanBoard[i][j]: 
                continue 
            else: 
                return False         
    return True

# --- Trening ---
start = time.time()
epsilon = EPSILON
rewards_history = []
losses_history = []

START_EPISODE = 2601
for episode in range(START_EPISODE, NUM_EPISODES + 1):
    # Curriculum learning
    if episode < 1500:
        env.difficulty = "no_ghosts"
    elif episode < 7500:
        env.difficulty = "one_ghost"
    else:
        env.difficulty = "full"

    state, pacman, ghost, obj, pacmanBoard = env.reset(screen, pacmanBoard)
    total_reward = 0
    episode_losses = []
    
    print(same(pacmanBoard))
    
    for step in range(MAX_STEPS):
        action = get_action(state, epsilon)
        next_state, reward, done, pacmanBoard = env.step(screen, font, action, pacmanBoard, pacman, ghost, obj)
        memory.append((state, action, reward, next_state, done))
        total_reward += reward
        state = next_state

        if step % 5 == 0:
            loss = replay()
            if loss is not None:
                episode_losses.append(loss)

        if step % 300 == 0:
            target_q_network.set_weights(q_network.get_weights())

        if done:
            break

    epsilon = max(EPSILON_MIN, epsilon * EPSILON_DECAY)
    avg_loss = np.mean(episode_losses) if episode_losses else 0
    rewards_history.append(total_reward)
    losses_history.append(avg_loss)

    if episode % 50 == 0:
        avg_reward = np.mean(rewards_history[-50:])
        avg_loss = np.mean(losses_history[-50:])
        print(f"Epizod {episode:5d} | Tryb: {env.difficulty:10s} | "
              f"Śr. nagroda: {avg_reward:8.2f} | Śr. strata: {avg_loss:.4f} | "
              f"Epsilon: {epsilon:.3f} | Ostatnia: {total_reward:.1f}")

    if episode % 100 == 0:
        q_network.save(f"models_final/pacman_ai_ep{episode}.keras")
        print(f"💾 Zapisano checkpoint po epizodzie {episode}")

q_network.save("models_final/pacman_ai_final.keras")
print(f"✅ Model końcowy zapisany! Czas całkowity: {time.time() - start:.2f}s")
