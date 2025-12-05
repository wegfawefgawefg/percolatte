import pygame
import random

from src.state import State, init_grid
from src.auto_tune import auto_tune_density
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

            if event.key == pygame.K_t:
                state.reset_auto_tune()
                state.set_fill_fraction(0.5)
                state.reset()
                init_grid(state, seed=state.last_seed)

                iterations = 0
                while (
                    state.auto_step >= state.auto_min_step
                    and iterations < state.auto_max_iterations
                ):
                    print(
                        f"[TUNE] start fill={state.fill_fraction:.8f} "
                        f"jump={state.auto_step:.8f}"
                    )
                    goals, direction, success_rate = auto_tune_density(state)
                    print(
                        f"[TUNE] goals: {goals}/100 ({success_rate:.3f}) "
                        f"fill={state.fill_fraction:.8f} jump={state.auto_step:.8f}"
                    )
                    if direction == 0:
                        if state.auto_step <= state.auto_min_step:
                            print("[TUNE] within hysteresis band; stopping.")
                            break
                        state.auto_step = max(state.auto_step / 10.0, state.auto_min_step)
                        print(
                            f"[TUNE] within band; reducing jump to "
                            f"{state.auto_step:.8f} and continuing."
                        )
                        continue
                    iterations += 1

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
