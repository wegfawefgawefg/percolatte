import pygame
import random

from src.state import State, init_grid
from src.settings import DENSITY_DELTA_PER_PRESS


def do_inputs(state: State, events):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                state.running = False

            if event.key == pygame.K_r:
                state.reset()
                init_grid(state, seed=0)

            if event.key == pygame.K_s:
                state.reset()
                seed = random.randrange(1_000_000)
                init_grid(state, seed=seed)

            if event.key == pygame.K_SPACE:
                state.paused = not state.paused

    keys = pygame.key.get_pressed()
    adjustment = 0.0
    if keys[pygame.K_UP]:
        adjustment += DENSITY_DELTA_PER_PRESS
    if keys[pygame.K_DOWN]:
        adjustment -= DENSITY_DELTA_PER_PRESS

    if adjustment:
        before = state.fill_fraction
        state.set_fill_fraction(state.fill_fraction + adjustment)
        if state.fill_fraction != before:
            state.reset()
            init_grid(state, seed=state.last_seed)
