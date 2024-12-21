import numpy as np
from collections import deque as deque

with open("./15/test9.txt") as f:
    input = f.read().strip()

split = input.split("\n\n")
assert len(split) == 2
input_grid = split[0].split("\n")
input_moves = [m for m in split[1] if m != "\n"]


class Warehouse:
    def __init__(self, raw_grid: list[str], wide: bool = False) -> None:
        if wide:
            raw_grid = [
                "".join([self.go_wide(cell) for cell in line]) for line in raw_grid
            ]
        self.grid = {
            (x, y): val for y, line in enumerate(raw_grid) for x, val in enumerate(line)
        }

        self.cols, self.rows = (
            val + 1 for val in np.max(list(self.grid.keys()), axis=0)
        )

    @staticmethod
    def go_wide(cell: str) -> str:
        match cell:
            case "#":
                return "##"
            case "O":
                return "[]"
            case ".":
                return ".."
            case "@":
                return "@."

    @staticmethod
    def get_color(cell: str) -> str:
        match cell:
            case "@":
                return f"\033[31;1m{cell}\033[0m"
            case "#":
                return f"\033[36;47m{cell}\033[0m"
            case "O" | "[" | "]":
                return f"\033[32;1m{cell}\033[0m"
            case ".":
                return f"\033[90;m{cell}\033[0m"

    def print(self) -> None:
        split = np.array_split(list(self.grid.values()), self.rows)
        for row in split:
            print("".join([self.get_color(cell) for cell in row]))
        pass

    def gps(self):
        sums_list = [
            pos[1] * 100 + pos[0] for pos, val in self.grid.items() if val == "O" or val == "["
        ]
        return np.sum(np.array(sums_list))



class Robot:
    dirs = {
        "^": np.array([0, -1]),
        ">": np.array([1, 0]),
        "v": np.array([0, 1]),
        "<": np.array([-1, 0]),
    }
    box_sides = {"]": np.array([-1, 0]), "[": np.array([1, 0])}

    def __init__(self, warehouse: Warehouse, moves: list[str]) -> None:

        self.warehouse = warehouse
        self.grid = warehouse.grid
        # self.pos = self.find(self.grid)
        self.move_q = deque(moves)

    @property
    def pos(self):
        return tuple(list(self.grid.keys())[list(self.grid.values()).index("@")])

    def run(self) -> None:
        i = 0
        while len(self.move_q) > 0:
            i += 1
            m = self.move_q.popleft()
            x, y = self.dirs[m]
            if y != 0:
                self.move_wide(m)
            else:
                self.move(m)
            # print(f"move {i}: {m}")
            # self.warehouse.print()
            # print("continuing")

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
            # append the last with the previous pos
            q.append((prev_pos, last_val))

    def move_wide(self, move: str) -> None:
        move_dir = self.dirs[move]
        next_cell_pos = tuple((self.pos + move_dir).tolist())
        next_cell = self.grid[next_cell_pos]
        if next_cell in self.box_sides.keys():
            cells = [self.pos]
            robot_neighbor = tuple((self.pos + self.box_sides[next_cell]).tolist())
            # don't shift the robot neighbor if it is a box
            if self.grid[robot_neighbor] not in self.box_sides.keys():
                cells.append(robot_neighbor)
            chain = self.get_box_chain([cells], move_dir)
            # shift the chain in reverse
            for row in chain[::-1]:
                for pos in row:
                    new_pos = tuple((pos + move_dir).tolist())

                    self.grid[new_pos] = self.grid[pos]
                    self.grid[pos] = "."
                    # self.warehouse.print()
        else:
            self.move(move)

    def get_box_chain(self, cells: list[tuple[int, int]], move_dir) -> list:
        next_cells = {}
        last_cells = cells[-1]
        for c in last_cells:
            # print(c)
            next_cell_pos = tuple((np.array(c) + move_dir).tolist())
            next_cell_val = self.grid[next_cell_pos]
            # print(next_cell_pos, next_cell_val)
            next_cells[next_cell_pos] = next_cell_val
            # if the cell is a box, check it for box side neighbors and add to next_cells
            if next_cell_val in self.box_sides.keys():
                box_neighbor = tuple(
                    (np.array(next_cell_pos) + self.box_sides[next_cell_val]).tolist()
                )
                if self.grid[box_neighbor] in self.box_sides.keys():
                    next_cells[box_neighbor] = self.grid[box_neighbor]
        # print(next_cells)
        # if all next_cells have free space we can return the chain and move
        if all([val == "." for val in next_cells.values()]):
            # cells.extend([list(next_cells.keys())])
            return cells
        # there is a wall in the box chain. do nothing
        elif any([val == "#" for val in next_cells.values()]):
            return []
        # there are boxes, continue the chain
        elif any([val in self.box_sides.keys() for val in next_cells.values()]):
            only_box_cells = [pos for pos, val in next_cells.items() if val in self.box_sides.keys()]
            cells.extend([only_box_cells])
            return self.get_box_chain(cells, move_dir)

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


# part 1

grid = Warehouse(input_grid)
robot = Robot(grid, input_moves)
robot.run()
robot.warehouse.print()
print(robot.warehouse.gps())

# part 2
grid2 = Warehouse(input_grid, True)
robot2 = Robot(grid2, input_moves)
print("initial state")
robot2.warehouse.print()
robot2.run()
robot2.warehouse.print()
print(robot2.warehouse.gps())
