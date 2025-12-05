import pygame
import glm

from src.state import State
from src.utils import mouse_pos
from src.settings import (
    WINDOW_DIMS,
    DIMS,
    SIMULATION_FPS,
    RENDER_FPS,
    GRID_DIMS,
)


def draw(
    state,
    graphics,
    sim_rate,
    fps,
):
    graphics.render_surface.fill((0, 0, 0))

    mpos = mouse_pos()

    grid_pos = glm.vec2(0, 0)
    grid_size = glm.vec2(1.0, 1.0)
    draw_grid(state, graphics, grid_pos, grid_size)

    # just draw a circle on the mouse
    pygame.draw.circle(graphics.render_surface, (0, 255, 0), mpos, 2)

    draw_grid_coords_under_mouse(state, graphics, grid_pos, grid_size, mpos)

    draw_perf_stats(graphics, sim_rate, fps, state.fill_fraction)

    if is_right_wall_on_fire(state):
        goal_font = pygame.font.Font(None, 96)
        goal_surface = goal_font.render("GOAL", True, (255, 255, 255))
        goal_rect = goal_surface.get_rect()
        goal_rect.top = 40
        goal_rect.centerx = graphics.render_surface.get_width() // 2
        graphics.render_surface.blit(goal_surface, goal_rect)

    if state.paused:
        pause_surface = graphics.font.render("PAUSE", True, (255, 0, 0))
        pause_rect = pause_surface.get_rect()
        pause_rect.top = 2
        pause_rect.right = graphics.render_surface.get_width() - 2
        graphics.render_surface.blit(pause_surface, pause_rect)

    stretched_surface = pygame.transform.scale(graphics.render_surface, WINDOW_DIMS)
    graphics.window.blit(stretched_surface, (0, 0))
    pygame.display.update()


def draw_grid_coords_under_mouse(
    state,
    graphics,
    grid_pos: glm.vec2,
    grid_size: glm.vec2,
    pos: glm.vec2,
):
    mouse = mouse_pos()
    col = "-"
    row = "-"

    size_in_pixels = DIMS * grid_size
    cell = size_in_pixels / glm.vec2(GRID_DIMS)

    within_x = grid_pos.x <= mouse.x < grid_pos.x + size_in_pixels.x
    within_y = grid_pos.y <= mouse.y < grid_pos.y + size_in_pixels.y
    if within_x and within_y and cell.x and cell.y:
        col = int((mouse.x - grid_pos.x) / cell.x)
        row = int((mouse.y - grid_pos.y) / cell.y)

    # draw the text in the top right corner
    font = pygame.font.Font(None, 16)
    text = font.render(f"({col}, {row})", True, (255, 255, 255))
    # put it at pos
    graphics.render_surface.blit(text, (pos.x, pos.y))


def draw_perf_stats(graphics, sim_rate, fps, density):
    def fmt_line(label, current, target):
        percent = 0.0
        if target:
            percent = (current / target) * 100.0
        return f"{label}: {current:6.1f} / {target:6.1f} ({percent:5.1f}%)"

    lines = [
        fmt_line("SIM", sim_rate, SIMULATION_FPS),
        fmt_line("FPS", fps, RENDER_FPS),
    ]

    y = 2
    for line in lines:
        text_surface = graphics.font.render(line, True, (255, 255, 255))
        graphics.render_surface.blit(text_surface, (2, y))
        y += text_surface.get_height() + 2

    density_text = graphics.font.render(f"Density: {density:.8f}", True, (255, 255, 255))
    density_rect = density_text.get_rect()
    density_rect.left = 2
    density_rect.bottom = graphics.render_surface.get_height() - 2
    graphics.render_surface.blit(density_text, density_rect)


def draw_grid(state, graphics, pos: glm.vec2, size: glm.vec2):
    size = size * DIMS
    grid = state.current
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if rows == 0 or cols == 0:
        return

    cell_w = size.x / cols
    cell_h = size.y / rows

    surface = graphics.render_surface
    TREE_COLOR = (34, 139, 34)
    FIRE_COLOR = (220, 20, 60)
    EMPTY_COLOR = (10, 10, 10)

    for y in range(rows):
        for x in range(cols):
            value = grid[y][x]
            if value == 2:
                color = FIRE_COLOR
            elif value == 1:
                color = TREE_COLOR
            else:
                color = EMPTY_COLOR

            rect = pygame.Rect(
                int(pos.x + x * cell_w),
                int(pos.y + y * cell_h),
                int(cell_w + 1),
                int(cell_h + 1),
            )
            pygame.draw.rect(surface, color, rect)

    # GRID_COLOR = (60, 60, 60)
    # GRID_WIDTH = 1
    # for i in range(cols + 1):
    #     x = int(round(pos.x + i * cell_w))
    #     pygame.draw.line(
    #         surface,
    #         GRID_COLOR,
    #         (x, int(round(pos.y))),
    #         (x, int(round(pos.y + size.y))),
    #         GRID_WIDTH,
    #     )
    # for j in range(rows + 1):
    #     y = int(round(pos.y + j * cell_h))
    #     pygame.draw.line(
    #         surface,
    #         GRID_COLOR,
    #         (int(round(pos.x)), y),
    #         (int(round(pos.x + size.x)), y),
    #         GRID_WIDTH,
    #     )


def draw_demo(surface):
    angle = pygame.time.get_ticks() / 1000

    rect_size = glm.vec2(16, 16)
    center = DIMS / 2
    rect_pos = center - rect_size / 2 + glm.vec2(32, 32)

    for i in range(3):
        rot = glm.rotate(glm.vec2(0.0, 1.0), angle + i * 90)
        rect_pos_rotated = rot @ (rect_pos - center) + rect_pos
        pygame.draw.rect(
            surface, (255, 0, 0), (rect_pos_rotated.to_tuple(), rect_size.to_tuple())
        )

    pygame.draw.circle(surface, (0, 255, 0), mouse_pos(), 10)


def is_right_wall_on_fire(state: State) -> bool:
    grid = state.current
    if not grid or not grid[0]:
        return False
    last_col = len(grid[0]) - 1
    for row in grid:
        if row[last_col] == 2:
            return True
    return False
