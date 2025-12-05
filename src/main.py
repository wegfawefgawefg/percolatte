import pygame

from src.graphics import Graphics
from src.state import State
from src.draw import draw
from src.settings import SIMULATION_FPS, SIM_DT, RENDER_INTERVAL
from src.state import init_grid
from src.step import step
from src.inputs import do_inputs

pygame.init()


def main():
    state = State()
    graphics = Graphics()

    init_grid(state, seed=0)

    accumulator = 0.0
    last_time = pygame.time.get_ticks() / 1000.0
    last_render_time = 0.0
    displayed_fps = 0.0
    sim_rate = SIMULATION_FPS
    sim_measure_start = last_time
    sim_steps = 0

    while state.running:
        current_time = pygame.time.get_ticks() / 1000.0
        frame_time = current_time - last_time
        last_time = current_time

        if not state.paused:
            accumulator += frame_time

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                state.running = False

        do_inputs(state, events)

        if not state.paused:
            while accumulator >= SIM_DT:
                step(state)
                accumulator -= SIM_DT
                sim_steps += 1

        if current_time - sim_measure_start >= 0.5:
            elapsed = current_time - sim_measure_start
            if elapsed > 0:
                sim_rate = sim_steps / elapsed
            sim_steps = 0
            sim_measure_start = current_time

        if current_time - last_render_time >= RENDER_INTERVAL:
            graphics.clock.tick()
            displayed_fps = graphics.clock.get_fps()
            draw(
                state,
                graphics,
                fps=displayed_fps,
                sim_rate=sim_rate,
            )
            last_render_time = current_time

    pygame.quit()


if __name__ == "__main__":
    main()
