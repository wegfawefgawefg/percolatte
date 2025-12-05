import glm
import pygame

from src.state import State


# each cell has three states, empty: 0, tree: 1, fire: 2
def step(state: State) -> bool:
    grid = state.current
    next = state.next
    changed = False

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            cell = grid[y][x]

            # copy current to next
            next[y][x] = cell

            if cell == 1:  # tree
                # check von Neumann neighbors for fire
                neighbors = [
                    (x, y - 1),
                    (x + 1, y),
                    (x, y + 1),
                    (x - 1, y),
                    # add diagonals for Moore neighborhood
                    # (x - 1, y - 1),
                    # (x + 1, y - 1),
                    # (x + 1, y + 1),
                    # (x - 1, y + 1),
                ]
                for nx, ny in neighbors:
                    if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):  # in bounds
                        if grid[ny][nx] == 2:  # neighbor is burning
                            next[y][x] = 2  # tree catches fire
                            break
            if next[y][x] != cell:
                changed = True

    state.flip()
    return changed
