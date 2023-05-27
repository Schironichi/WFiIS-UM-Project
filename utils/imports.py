import random
import gym
import numpy as np
import pygame
import os
from stable_baselines3 import PPO
from game_utils.colors import Colors
from game_utils.window import Window
from game_utils.actions import Actions
from game_utils.positions import Positions
from game_utils.player import Player
from game_utils.obstacle import Obstacle
# from tensorflow.keras.optimizers.legacy import Adam
# from keras.models import Sequential
# from keras.layers import Dense, Flatten
# from rl.agents import DQNAgent
# from rl.policy import BoltzmannQPolicy
# from rl.memory import SequentialMemory
