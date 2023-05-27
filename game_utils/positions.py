from utils.imports import random
from utils.imports import np
from utils.imports import os


class Positions:
    RANDOM = [random.randint(0, 700) for _ in range(102)]
    STATIC = np.loadtxt(os.path.join('data', 'positions.csv'), delimiter=",", dtype=int).flatten()
