import pygame
import glm
import random

from src.settings import GRID_DIMS


# each cell has three states, empty: 0, tree: 1, fire: 2
class State:
    def __init__(self):
        self.running: bool = True
        self.paused: bool = False

        self.grid_a: list[list[int]] = self.make_grid()
        self.grid_b: list[list[int]] = self.make_grid()

        self.current: list[list[int]] = self.grid_a
        self.next: list[list[int]] = self.grid_b

    def make_grid(self) -> list[list[int]]:
        return [[0 for _ in range(int(GRID_DIMS.x))] for _ in range(int(GRID_DIMS.y))]

    def flip(self):
        self.current, self.next = self.next, self.current

    def reset(self):
        self.current = self.make_grid()
        self.next = self.make_grid()


def init_grid(state: State, seed: int, fill_fraction: float = 0.5):
    random.seed(seed)

    for y in range(GRID_DIMS.y):
        for x in range(GRID_DIMS.x):
            state.current[y][x] = random.random() < fill_fraction

    # left wall is all fires
    for y in range(GRID_DIMS.y):
        state.current[y][0] = 2
