from collections import deque, defaultdict
import numpy as np
import heapq
import time

with open("./18/input.txt") as f:
    input = [line for line in f.read().strip().splitlines()]


class Memory:
    
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, bites_in: list, part2: bool = False) -> None:
        self.size = 71
        run_time = 1024
        # self.size = 7
        # run_time =  12
        self.grid = defaultdict(lambda: False) # no need for bounds check with default False
        for y in range(self.size):
            for x in range(self.size):
                self.grid[(x, y)] = "."
        self.bites = [tuple(int(bit) for bit in bite.split(",")) for bite in bites_in]
        if part2:
            self.run_bin_search()
        else:
            grid = self.run_bites(self.bites[0:run_time])
            steps = self.a_star(grid)    
            print(steps)

    def print(self, grid, path=None) -> None:
        gc = grid.copy()
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

    def run_bites(self, bites=[]):
        gc = self.grid.copy()
        bites = bites or self.bites
        bq = deque(bites)
        bite_count = 0
        while bq:
            bite = bq.popleft()
            gc[bite] = "#"
            bite_count += 1
        return gc
    
    def run_bin_search(self):
        high = len(self.bites) - 1
        low = 0
        while high - low > 1:
            mid = (low + high) // 2
            grid = self.run_bites(self.bites[:mid])
            steps = self.a_star(grid)
            if steps:
                low = mid
            else:
                high = mid
        print(f"byte: {self.bites[mid]}")
        
        
    def a_star(self, grid) -> None:
        min_steps = np.inf
        seen = defaultdict(lambda: (False, np.inf))  # seen? and cost
        pq = [(0, 0, (0, 0), [])]  # cost, steps, node, path
        while pq:
            _, steps, node, path = heapq.heappop(pq)
            # print("\n")
            # mem.print(path)
            if len(path) > min_steps:
                continue
            if node == (self.size - 1, self.size - 1) and len(path) < min_steps:
                min_steps = len(path)
                print("path")
                self.print(grid, path)
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
                    grid[neighbor]
                    and grid[neighbor] != "#"
                    # and not is_seen
                    and new_cost < seen_cost
                ):
                    seen[neighbor] = (True, new_cost)
                    heapq.heappush(
                        pq, (new_cost, steps + 1, neighbor, path + [neighbor])
                    )
        if min_steps != np.inf:
            return min_steps
        else:
            return 0

t1 = time.time()
mem = Memory(input)
t2 = time.time()
print(f"time elapsed: {t2 - t1}")

t1 = time.time()
mem2 = Memory(input, True)
t2 = time.time()
print(f"time elapsed: {t2 - t1}")