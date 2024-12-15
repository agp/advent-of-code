import numpy as np
from collections import deque as deque

with open("./15/input.txt") as f:
    input = f.read().strip()

split = input.split("\n\n")
assert len(split) == 2
input_grid = split[0].split("\n")
input_moves = [m for m in split[1] if m != "\n"]


class Warehouse:
    def __init__(self, raw_grid: list[str]):
        self.grid = {
            (x, y): val for y, line in enumerate(raw_grid) for x, val in enumerate(line)
        }
        self.rows, self.col = (
            val + 1 for val in np.max(list(self.grid.keys()), axis=0)
        )

    def gps(self):
        sums_list = [
            pos[1] * 100 + pos[0]
            for pos, val in robot.warehouse.grid.items()
            if val == "O"
        ]
        return np.sum(np.array(sums_list))

    def print(self):
        split = np.array_split(list(self.grid.values()), self.rows)
        for row in split:
            print("".join([self.get_color(cell) for cell in row]))
        pass

    def get_color(self, cell: str):
        match cell:
            case "@":
                return f"\033[31;1m{cell}\033[0m"
            case "#":
                return f"\033[36;47m{cell}\033[0m"
            case "O":
                return f"\033[32;1m{cell}\033[0m"
            case ".":
                return f"\033[90;m{cell}\033[0m"


class Robot:
    dirs = {
        "^": np.array([0, -1]),
        ">": np.array([1, 0]),
        "v": np.array([0, 1]),
        "<": np.array([-1, 0]),
    }

    def __init__(self, warehouse: Warehouse, moves: list[str]) -> None:

        self.warehouse = warehouse
        self.grid = warehouse.grid
        self.pos = self.find(self.grid)
        self.move_q = deque(moves)

    def find(self, grid) -> tuple[int, int]:
        return tuple(list(grid.keys())[list(grid.values()).index("@")])

    def run(self) -> None:
        # i = 0
        while len(self.move_q) > 0:
            # i += 1
            m = self.move_q.popleft()
            self.move(m)
            # print(f"move {i}: {m}")
            # self.warehouse.print()

    def move(self, move: str) -> None:
        q = self.get_next_cells(self.dirs[move])
        while len(q) > 1:
            # pop two to swap
            last_pos, last_val = q.pop()
            prev_pos, prev_val = q.pop()
            # if it is a wall just break
            if last_val == "#":
                break
            else:
                # there is free space. swap the last with the previous
                self.warehouse.grid[prev_pos] = last_val
                self.warehouse.grid[last_pos] = prev_val
                # set robot pos if we are at it
                if prev_val == "@":
                    self.pos = last_pos
            # append the last with the previous pos
            q.append((prev_pos, last_val))

    def get_next_cells(self, vector: tuple[int, int]) -> deque:
        q = deque()
        next_cell = None
        curr_pos = self.pos
        # first in queue will always be the robot
        q.append((curr_pos, "@"))
        # get all cells until empty space or wall
        while next_cell != "." and next_cell != "#":
            next_cell_pos = tuple((curr_pos + vector).tolist())
            next_cell = self.grid[next_cell_pos]
            q.append((next_cell_pos, next_cell))
            curr_pos = next_cell_pos
        return q


grid = Warehouse(input_grid)
robot = Robot(grid, input_moves)
robot.run()
robot.warehouse.print()
print(robot.warehouse.gps())
