import gym
import pygame
import numpy as np
import time
import random

#from tensorflow.keras.optimizers.legacy import Adam
# trzeba posprzątać, co się da wrzucić do klasy FallingBirds
pygame.init()
'''positions = [500, 172, 397, 319, 402, 76, 80, 504, 45, 88, 539, 246, 563, 60,
             409, 503, 358, 452, 261, 406, 63, 466, 334, 187, 432, 179, 332,
             59, 622, 536, 523, 154, 307, 540, 344, 528, 195, 123, 295, 162,
             586, 145, 207, 395, 364, 481, 443, 114, 670, 579, 395, 293, 375,
             579, 234, 144, 302, 178, 31, 292, 285, 596, 59, 168, 240, 24, 212,
             304, 303, 373, 99, 323, 114, 284, 374, 498, 624, 565, 456, 472, 357,
             638, 111, 65, 431, 574, 297, 231, 455, 269, 473, 267, 572, 98, 457,
             46, 495, 63, 187, 352, 302, 178, 31, 292, 285]'''

positions = [random.randint(0, 700) for _ in range(102)]
# Actions
NO_ACTION = 0
LEFT_ACTION = 1
RIGHT_ACTION = 2

# player.right < obstacle_right
# player.left > obstacle_left
# if obstacle_height = 0 do not move


# Set the window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
pygame.display.set_caption("Falling Bird - DR PR KK")

# Set the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
BLUE = (0, 0, 255)

# Set the font
FONT = pygame.font.Font(None, 36)

# Set the game clock
clock = pygame.time.Clock()

# Set the player dimensions and position
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_X = WINDOW_WIDTH // 2
PLAYER_Y = 0

# Set the obstacle dimensions and speed
OBSTACLE_WIDTH = 100
OBSTACLE_HEIGHT = 50
OBSTACLE_SPEED = 2

# Set the number of obstacles
NUM_OBSTACLES = 2

# chyba można z tego zrobić klase w klasie, ale głowy nie dam bo python
# Create the player sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Kratos.png')
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Create the player sprite
player = Player(PLAYER_X, PLAYER_Y)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

FPS = 500

# przerobić na funkcje wewnątrz klasowe.
def update_gamestate(obstacles, score, player):
    # Move the obstacles down
    game_over = False
    for obstacle_rect in obstacles:
        obstacle_rect[0].move_ip(0, -OBSTACLE_SPEED)
        obstacle_rect[1].move_ip(0, -OBSTACLE_SPEED)

        # Check for collisions
        if player.rect.colliderect(obstacle_rect[0]) or player.rect.colliderect(obstacle_rect[1]) or score == 100:
            '''obstacle_left = positions[score]
            obstacle_right = obstacle_left + OBSTACLE_WIDTH
            obstacle_height = obstacle_rect[0].y if obstacle_rect[0].y >= 0 else 0
            print(f"Player.left: {player.rect.x} Player.right: {player.rect.x + PLAYER_WIDTH} Obst wysokosc: {obstacle_height}  Obst left: {obstacle_left}  Obst right: {obstacle_right} Score: {score}")
            '''
            game_over = True

        # If the obstacle goes off the screen, move it back to the bottom delete obst and create a new one at the bottom
        if obstacle_rect[0].bottom <= 0 and not game_over:
            score += 1
            obstacles.pop(0)
            obstacles.append([
                # left part
                pygame.Rect(0, WINDOW_HEIGHT, positions[score + 1], OBSTACLE_HEIGHT),
                # right part
                pygame.Rect(positions[score + 1] + OBSTACLE_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH - OBSTACLE_WIDTH,
                            OBSTACLE_HEIGHT)
            ])

    return game_over, score, obstacles


def player_input_handler(keys):
    # Handle input
    if keys[pygame.K_a]:
        if player.rect.left > 7:
            player.rect.move_ip(-8, 0)
    if keys[pygame.K_d]:
        if player.rect.right < WINDOW_WIDTH - 7:
            player.rect.move_ip(8, 0)


def event_handler(events):
    # Handle events
    game_over = False
    for event in events:
        if event.type == pygame.QUIT:
            game_over = True
    return game_over


def get_positions(player, obstacle_rects, score):
    obstacle_left = positions[score]
    obstacle_right = obstacle_left + OBSTACLE_WIDTH
    obstacle_height = obstacle_rects[0][0].y if obstacle_rects[0][0].y >= 0 else 0

    # print(f"Player.left: {player.rect.x} Player.right: {player.rect.x + PLAYER_WIDTH} Obst wysokosc: {obstacle_height}  Obst left: {obstacle_left}  Obst right: {obstacle_right} Score: {score}")
    return [player.rect.x, player.rect.x + PLAYER_WIDTH, obstacle_height, obstacle_left, obstacle_right]


class FallingBird(gym.Env):
    # uprościć jak się da tego inita bo wygląda jak gówno xd
    def __init__(self):
        self.score_text = None
        self.action = None
        self.dist = None
        self.done = None
        self.observation = None
        self.obstacle_rects = None
        self.game_over = None
        self.prev_dist = None
        self.reward = 0
        self.score = 0
        self.prev_score = 0
        # te poniżej są ważne reszta trochę mniej
        self.render_mode = None
        self.action_space = gym.spaces.Discrete(3)
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(6,), dtype=np.float32)
    # więcej funkcji pomocniczych IMO
    def step(self, action):
        obstacle_left = positions[self.score]
        obstacle_right = obstacle_left + OBSTACLE_WIDTH
        self.prev_dist = abs(self.player.rect.x - obstacle_left) + abs(
            self.player.rect.x + PLAYER_WIDTH - obstacle_right)

        if action == LEFT_ACTION:
            if self.player.rect.left > 7:
                self.player.rect.move_ip(-8, 0)

        elif action == RIGHT_ACTION:
            if self.player.rect.right < WINDOW_WIDTH - 7:
                self.player.rect.move_ip(8, 0)

        elif action == NO_ACTION:
            pass
        # Najważniejszy part, tutaj liczymy wszystko w sumie
        self.game_over, self.score, self.obstacle_rects = update_gamestate(self.obstacle_rects, self.score, self.player)
        self.observation = get_positions(self.player, self.obstacle_rects, self.score)
        self.observation.append(action)
        self.observation = np.array(self.observation).astype(np.float32)

        if self.game_over:
            self.done = True
        # można się pobawić, nie jestem pewien czy nagrody i kary są optymalne
        # reward
        # A: death
        if self.done:
            reward_a = -1000
        else:
            reward_a = 0

        # B: passing obstacle
        if self.prev_score < self.score:
            reward_b = 1000
            self.prev_score = self.score
        else:
            reward_b = 0

        # C: being in good spot
        obstacle_left = positions[self.score]
        obstacle_right = obstacle_left + OBSTACLE_WIDTH
        self.dist = abs(self.player.rect.x - obstacle_left) + abs(self.player.rect.x + PLAYER_WIDTH - obstacle_right)

        if self.dist > 51:
            reward_c = -5
        else:
            reward_c = 10

        # D: distance punishment
        if self.prev_dist > self.dist:
            reward_d = 1
        else:
            reward_d = -20

        # E: moving while inside G spot (To test)
        if self.dist < 51 and action != NO_ACTION:
            reward_e = -1
        else:
            reward_e = 0

        self.reward = reward_a + reward_b + reward_c + reward_d + reward_e

        self.info = {}

        if self.render_mode == 'human':
            self.render()

        return self.observation, self.reward, self.done, self.info

    def reset(self):
        self.done = False
        self.score = 0
        self.game_over = False
        self.obstacle_rects = []
        self.player = Player(PLAYER_X, PLAYER_Y)
        # first obstacle
        self.obstacle_rects.append([
            # left part
            pygame.Rect(0, WINDOW_HEIGHT // 2, positions[0], OBSTACLE_HEIGHT),
            # right part
            pygame.Rect(positions[0] + OBSTACLE_WIDTH, WINDOW_HEIGHT // 2, WINDOW_WIDTH - OBSTACLE_WIDTH,
                        OBSTACLE_HEIGHT)
        ])

        # second obstacle
        self.obstacle_rects.append([
            pygame.Rect(0, WINDOW_HEIGHT, positions[1], OBSTACLE_HEIGHT),
            pygame.Rect(positions[1] + OBSTACLE_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH - OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        ])

        # observation
        self.action = 0
        self.observation = get_positions(self.player, self.obstacle_rects, self.score)
        self.observation.append(self.action)
        self.observation = np.array(self.observation).astype(np.float32)

        # reward
        self.reward = 0
        self.score = 0
        self.prev_score = 0

        obstacle_left = positions[self.score]
        obstacle_right = obstacle_left + OBSTACLE_WIDTH
        self.dist = abs(self.player.rect.x - obstacle_left) + abs(self.player.rect.x + PLAYER_WIDTH - obstacle_right)

        if self.render_mode == 'human':
            pygame.init()
            pygame.display.set_caption("Falling Bird - DR PR KK")
            self.FONT = pygame.font.Font(None, 36)
            self.clock = pygame.time.Clock()
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.player = Player(PLAYER_X, PLAYER_Y)
            self.render()

        return self.observation
    #to imo git jest
    def render(self, render_mode='human'):
        # Clear the screen
        self.screen.fill(BLACK)

        # Draw the player
        # all_sprites.draw(screen)
        pygame.draw.rect(self.screen, BLUE, self.player.rect)

        # Draw the obstacles
        for obstacle_rect in self.obstacle_rects:
            pygame.draw.rect(self.screen, GRAY, obstacle_rect[0])
            pygame.draw.rect(self.screen, GRAY, obstacle_rect[1])

        # Draw the score
        self.score_text = self.FONT.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(self.score_text, (10, WINDOW_HEIGHT - 30))

        # Update the screen
        pygame.display.update()
        self.clock.tick(FPS)

        # if self.done:
        #   time.sleep(0.1)

    def close(self):
        pygame.quit()


import os

PPO_path = os.path.join('Training', 'Saved_models')
PPO_path_v2 = os.path.join('Training', 'Saved_models_v2')
PPO_path_v3 = os.path.join('Training', 'Saved_models_v3')
PPO_path_v4 = os.path.join('Training', 'Saved_models_v4')
from stable_baselines3 import PPO

# mozna by to w jakąs funkcje spróbować
#Create and teach model
env = FallingBird()
model = PPO('MlpPolicy', env, verbose=1)
env.render_mode = 'human'  # If you want to see the game
#env.render_mode = None
#model = PPO.load(PPO_path_v2, env=env)

# env.render_mode = None #If just wanna train the model
model.learn(total_timesteps=FPS * 600)

model.save(PPO_path_v4)
env.render_mode = 'human' #If just wanna train the model



'''def load_and_test_model(path, env, lib):
    model = lib.load(path, env=env)
    obs = env.reset()  # Zresetuj środowisko
    done = False
    while not done:
        action, _ = model.predict(obs)  # Wygeneruj akcję na podstawie obserwacji
        obs, reward, done, info = env.step(action)  # Wykonaj akcję w środowisku
        env.render()  # Wyświetl środowisko

 
for i in range(5):
    load_and_test_model(PPO_path_v3, env, PPO)'''



# TO DO
# Try to create selfmade models and test them
# Try to change rewards system
# Print part exists in update_gamestate()

'''
#  MODEL PART  #
from keras.models import Sequential
from keras.layers import Dense, Flatten
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

states = env.observation_space.shape
actions = env.action_space.n

print(states, actions)
def buildModel(states, actions):
    model = Sequential()
    model.add(Flatten(input_shape=states))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(actions, activation='linear'))
    return model

model = buildModel(states, actions)



print(model.summary())


#  AGENT PART  #

def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy, nb_actions=actions, nb_steps_warmup=10,
                   target_model_update=1e-2)
    return dqn


DQN = build_agent(model, actions)
DQN.compile(Adam(lr=1e-3), metrics=['mae'])
DQN.fit(env, nb_steps=50000, visualize=False, verbose=1)

'''
