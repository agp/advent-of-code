from collections import deque, defaultdict, Counter
import numpy as np
import time

with open("./20/input.txt") as f:
    input = [line for line in f.read().strip().splitlines()]


class Track:

    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, input: list) -> None:
        self.grid = defaultdict(lambda: False)
        for y, line in enumerate(input):
            for x, val in enumerate(line):
                self.grid[(x, y)] = val

        self.start = next(node for node in self.grid if self.grid[node] == "S")
        self.end = next(node for node in self.grid if self.grid[node] == "E")
        self.cols, self.rows = (
            val + 1 for val in np.max(list(self.grid.keys()), axis=0)
        )
        all_cheats = self.bfs(self.grid)
        best_cheats = [time for time in all_cheats if time >= 100]
        print(len(best_cheats))

    def print(self, grid: dict[tuple[int, int] : str]) -> None:
        gc = grid.copy()

        split = np.array_split([v for v in gc.values() if v], self.rows)
        for row in split:
            print("".join([self.get_color(cell) for cell in row]))

    @staticmethod
    def get_color(cell: str) -> str:
        match cell:
            case "O":
                return f"\033[31;1m{cell}\033[0m"
            case "#":
                return f"\033[36;47m{cell}\033[0m"
            case ".":
                return f"\033[90;m{cell}\033[0m"
            case "S" | "E":
                return f"\033[32;1m{cell}\033[0m"
            case _:
                print(cell)

    def bfs(self, grid: dict[tuple[int, int] : str]) -> None:
        cheats = defaultdict(list)
        saved = []
        visited = defaultdict(lambda: False)
        q = deque([(self.start, [])])  # node, path, cheated
        while q:
            node, path = q.pop()
            visited[node] = True
            if node == self.end:
                # print(f"picoseconds: {len(path)}")
                # print(sorted(Counter(saved).items()))
                return saved

            for d in self.dirs:
                x, y = node
                dx, dy = d
                neighbor = (x + dx, y + dy)
                # if there is a wall with a valid path beyond it cheat
                if grid[neighbor] == "#":
                    nx, ny = neighbor
                    cheat_to = (nx + dx, ny + dy)
                    if grid[cheat_to] in [".", "E"] and not visited[cheat_to]:
                        # store the cheat path length to compare to actual path
                        cheats[cheat_to].append(
                            len(path) + 2
                        )  # 1 for wall, one for step

                if grid[neighbor] != "#" and not visited[neighbor]:
                    new_path = path + [neighbor]
                    if cheats.get(neighbor):
                        for c in cheats[neighbor]:
                            saved.append(len(new_path) - c)
                    q.append((neighbor, new_path))


t1 = time.time()
mem = Track(input)
t2 = time.time()
print(f"time elapsed: {t2 - t1}")
