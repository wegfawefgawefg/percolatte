import random

from src.settings import (
    GRID_DIMS,
    AUTO_TUNE_LOWER_SUCCESS,
    AUTO_TUNE_UPPER_SUCCESS,
)
from src.state import State, init_grid
from src.step import step


MAX_STEPS = GRID_DIMS.x * GRID_DIMS.y


def _run_single_trial(fill_fraction: float, seed: int) -> bool:
    trial_state = State()
    init_grid(trial_state, seed=seed, fill_fraction=fill_fraction)

    for _ in range(int(MAX_STEPS)):
        if trial_state.right_wall_on_fire():
            return True

        changed = step(trial_state)
        if not changed:
            break

    return trial_state.right_wall_on_fire()


def auto_tune_density(state: State, trials: int = 100) -> tuple[int, int, float]:
    rng_state = random.getstate()
    goals = 0

    try:
        for _ in range(trials):
            seed = state.auto_seed_counter
            state.auto_seed_counter += 1
            if _run_single_trial(state.fill_fraction, seed):
                goals += 1
    finally:
        random.setstate(rng_state)

    success_rate = goals / trials
    direction = 0
    if success_rate < AUTO_TUNE_LOWER_SUCCESS:
        direction = 1
    elif success_rate > AUTO_TUNE_UPPER_SUCCESS:
        direction = -1

    prev_direction = state.auto_last_direction

    if direction == 0:
        state.auto_last_direction = 0
        state.auto_flip_count = 0
        return goals, direction, success_rate

    if prev_direction and direction != prev_direction:
        state.auto_flip_count += 1
        if state.auto_flip_count >= 10:
            state.auto_step = max(state.auto_step / 10.0, state.auto_min_step)
            state.auto_flip_count = 0
    else:
        state.auto_flip_count = 0

    state.auto_last_direction = direction
    state.set_fill_fraction(state.fill_fraction + direction * state.auto_step)
    state.reset()
    init_grid(state, seed=state.last_seed)

    return goals, direction, success_rate
