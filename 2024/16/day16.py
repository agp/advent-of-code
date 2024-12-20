import heapq
import time
import numpy as np
from collections import defaultdict

with open("./16/input.txt") as f:
    input_rows = [row for row in f.read().splitlines()]


class Maze:
    moves = {(1, 0): ">", (0, 1): "v", (-1, 0): "<", (0, -1): "^"}
    move_deg = {">": 90, "v": 180, "<": 270, "^": 0}

    def __init__(self, raw_grid: list[str]) -> None:
        self.grid = {
            (x, y): val for y, line in enumerate(raw_grid) for x, val in enumerate(line)
        }
        self.cols, self.rows = (
            val + 1 for val in np.max(list(self.grid.keys()), axis=0)
        )
        self.start = next(node for node in self.grid if self.grid[node] == "S")
        self.end = next(node for node in self.grid if self.grid[node] == "E")
        self.visited = defaultdict(lambda: False)
        self.costs = defaultdict(lambda: np.inf)
        self.min_score = np.inf

    def print(self) -> None:
        split = np.array_split([v for v in self.grid.values()], self.rows)
        for row in split:
            print("".join([self.get_color(cell) for cell in row]))
        pass

    def get_color(self, cell: str) -> str:
        match cell:
            case "S" | "E":
                return f"\033[31;1m{cell}\033[0m"
            case "#":
                return f"\033[36;47m{cell}\033[0m"
            case "^" | ">" | "v" | "<":
                return f"\033[32;1m{cell}\033[0m"
            case ".":
                return f"\033[90;m{cell}\033[0m"

    def dijkstra(self) -> None:
        start_dir = (1, 0)
        self.visited[(self.start, start_dir)] = True
        pq = [
            (0, count := 0, self.start, np.array(start_dir))
        ]  # cost, count, node, current_dir - need a count to ensure no duplicate entries
        while pq:
            # pop lowest node from priority queue
            score, _, node, dir = heapq.heappop(pq)
            dir_tup = tuple(dir.tolist())
            # set node visited direction and cost. since cost check is done before adding to queue it will always be the lowest
            self.visited[(node, dir_tup)] = True
            self.costs[node] = score
            # self.grid[node] = self.moves[dir_tup]
            # self.print()
            if node == self.end:
                if score < self.min_score:
                    self.min_score = score
            # continue when score is already greater than a found min score
            if score > self.min_score:
                continue
            for move_tup in self.moves.keys():
                # don't reverse direction
                dx, dy = dir_tup
                if move_tup == (-dx, -dy):
                    continue
                move = np.array(move_tup)
                neighbor = tuple((np.array(node) + move).tolist())
                if self.grid[neighbor] != "#":
                    cost = score + 1 if np.array_equal(move, dir) else score + 1001
                    # if node is visited from same movement direction check that it will be a lower cost
                    if (
                        self.visited[(neighbor, move_tup)]
                        and cost > self.costs[neighbor]
                    ):
                        continue
                    heapq.heappush(pq, (cost, count := count + 1, neighbor, move))


maze = Maze(input_rows)
# maze.print()

start_time = time.time()
maze.dijkstra()
print(maze.min_score)
end_time = time.time()
print(f"time to run: {end_time-start_time}s")
