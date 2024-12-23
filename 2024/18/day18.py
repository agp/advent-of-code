from collections import deque, defaultdict
import numpy as np
import heapq
import time

with open("./18/input.txt") as f:
    input = [line for line in f.read().strip().splitlines()]


class Memory:
    size = 71
    # size = 7
    run_time = 1024
    # run_time = 12
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, input):
        # no need for bounds check with default False
        self.grid = defaultdict(lambda: False)
        for y in range(self.size):
            for x in range(self.size):
                self.grid[(x, y)] = "."
        self.min_steps = np.inf
        self.bq = deque([tuple(int(bit) for bit in byte.split(",")) for byte in input])

    def print(self, path=None) -> None:
        gc = self.grid.copy()
        if path:
            for node in path:
                gc[node] = "O"

        split = np.array_split([v for v in gc.values() if v], self.size)
        for row in split:
            print("".join([self.get_color(cell) for cell in row]))

    @staticmethod
    def get_color(cell: str) -> str:
        match cell:
            case "O":
                return f"\033[31;1m{cell}\033[0m"
            case "#":
                return f"\033[35;47;5m{cell}\033[0m"
            case ".":
                return f"\033[90;m{cell}\033[0m"
            case _:
                print(cell)

    def run(self):
        byte_count = 0
        while self.bq and byte_count < self.run_time:
            byte = self.bq.popleft()
            self.grid[byte] = "#"
            byte_count += 1

    def a_star(self) -> None:
        seen = defaultdict(lambda: (False, np.inf))  # visited? and min cost
        pq = [(0, 0, (0, 0), [])]  # cost, steps, node, path
        while pq:
            _, steps, node, path = heapq.heappop(pq)
            # print("\n")
            # mem.print(path)
            # print("\n")
            if len(path) > self.min_steps:
                continue
            if node == (self.size - 1, self.size - 1) and len(path) < self.min_steps:
                self.min_steps = len(path)
                self.print(path)
            for d in self.dirs:
                x, y = node
                dx, dy = d
                neighbor = (x + dx, y + dy)
                nx, ny = neighbor
                # manhattan distance plus steps
                new_cost = (
                    (abs(nx - self.size - 1) + abs(ny - self.size - 1)) + steps + 1
                )
                is_seen, seen_cost = seen[neighbor]
                if (
                    self.grid[neighbor]
                    and self.grid[neighbor] != "#"
                    # and not is_seen
                    and new_cost < seen_cost
                ):
                    seen[neighbor] = (True, new_cost)
                    heapq.heappush(
                        pq, (new_cost, steps + 1, neighbor, path + [neighbor])
                    )


mem = Memory(input)
mem.run()
mem.print()
t1 = time.time()
mem.a_star()
print(mem.min_steps)
t2 = time.time()
print(f"time elapsed: {t2 - t1}")
