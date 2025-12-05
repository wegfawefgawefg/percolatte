# for event in pygame.event.get():
#     if event.type == pygame.QUIT or (
#         event.type == pygame.KEYDOWN
#         and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)
#     ):
#         state.running = False

import pygame

from src.state import State, init_grid


def do_inputs(state: State):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                state.running = False

            # r for reset
            if event.key == pygame.K_r:
                state.reset()
                init_grid(state, seed=0, fill_fraction=0.5)

            if event.key == pygame.K_SPACE:
                state.paused = not state.paused
