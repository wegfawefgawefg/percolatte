import pygame
import glm
import random
from typing import Optional

from src.settings import (
    GRID_DIMS,
    AUTO_TUNE_INITIAL_STEP,
    AUTO_TUNE_MIN_STEP,
    AUTO_TUNE_MAX_ITERATIONS,
)


# each cell has three states, empty: 0, tree: 1, fire: 2
class State:
    def __init__(self):
        self.running: bool = True
        self.paused: bool = False

        self.grid_a: list[list[int]] = self.make_grid()
        self.grid_b: list[list[int]] = self.make_grid()

        self.current: list[list[int]] = self.grid_a
        self.next: list[list[int]] = self.grid_b

        self.fill_fraction: float = 0.59274621
        self.last_seed: int = 0
        self.auto_min_step = AUTO_TUNE_MIN_STEP
        self.auto_max_iterations = AUTO_TUNE_MAX_ITERATIONS
        self.reset_auto_tune()

    def make_grid(self) -> list[list[int]]:
        return [[0 for _ in range(int(GRID_DIMS.x))] for _ in range(int(GRID_DIMS.y))]

    def flip(self):
        self.current, self.next = self.next, self.current

    def reset(self):
        self.current = self.make_grid()
        self.next = self.make_grid()

    def set_fill_fraction(self, value: float):
        value = max(0.0, min(1.0, value))
        self.fill_fraction = value

    def reset_auto_tune(self):
        self.auto_step: float = AUTO_TUNE_INITIAL_STEP
        self.auto_last_direction: int = 0
        self.auto_seed_counter: int = 1
        self.auto_flip_count: int = 0

    def right_wall_on_fire(self) -> bool:
        if not self.current or not self.current[0]:
            return False
        last_col = len(self.current[0]) - 1
        for row in self.current:
            if row[last_col] == 2:
                return True
        return False


def init_grid(state: State, seed: int, fill_fraction: Optional[float] = None):
    state.last_seed = seed
    if fill_fraction is not None:
        state.set_fill_fraction(fill_fraction)
    fill_fraction = state.fill_fraction
    random.seed(seed)

    for y in range(GRID_DIMS.y):
        for x in range(GRID_DIMS.x):
            state.current[y][x] = random.random() < fill_fraction

    # left wall is all fires
    for y in range(GRID_DIMS.y):
        state.current[y][0] = 2
