from collections import defaultdict
from collections import deque as queue

with open("./12/input.txt") as f:
    input = [[s for s in line] for line in f.read().splitlines()]

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]


def validity(
    row: int,
    col: int,
    matrix: list[list[str]],
    visited: list[list[bool]],
    plant: str,
):
    not_visited = False
    is_same_plant = False
    in_bounds = 0 <= row < len(matrix) and 0 <= col < len(matrix[0])
    if in_bounds:
        not_visited = not visited[row][col]
        is_same_plant = plant == matrix[row][col]
    return in_bounds, not_visited, is_same_plant


def bfs_plants(row: int, col: int, matrix: list[list[str]], visited, start):
    q = queue()

    q.append((row, col))
    visited[row][col] = True
    plots[start]["points"] = set()

    while len(q) > 0:
        cell = q.popleft()
        cell_row = cell[0]
        cell_col = cell[1]
        plant = matrix[cell_row][cell_col]
        plots[start]["count"] += 1
        plots[start]["points"].add((cell_col, cell_row))

        for i in range(4):
            next_row = cell_row + dr[i]
            next_col = cell_col + dc[i]
            in_bounds, not_visited, is_same_plant = validity(
                next_row, next_col, matrix, visited, plant
            )
            # cell is in bounds, not visited and same plant - add to queue
            if all((in_bounds, not_visited, is_same_plant)):
                q.append((next_row, next_col))
                visited[next_row][next_col] = True
            # cell is out of bounds or in bounds with different plant:
            elif not in_bounds or (in_bounds and not is_same_plant):
                plots[start]["fences"] += 1


visited = [[False for _ in row] for row in input]
plots = defaultdict(lambda: defaultdict(int))

for i, row in enumerate(input):
    for j, col in enumerate(row):
        in_bounds, not_visited, is_same_plant = validity(
            i, j, input, visited, input[i][j]
        )
        if not_visited:
            start = f"x{j},y{i}"
            bfs_plants(i, j, input, visited, start)

print(sum([p["count"] * p["fences"] for p in plots.values()]))

# part 2
# copied from solutions... was wrinkling my brain.
def count_corners(area):
    up = set()
    down = set()
    left = set()
    right = set()
    for (x, y) in area:
        if (x - 1, y) not in area:
            left.add((x, y))

        if (x + 1, y) not in area:
            right.add((x, y))

        if (x, y + 1) not in area:
            down.add((x, y))

        if (x, y - 1) not in area:
            up.add((x, y))

    corners = 0
    for (x, y) in left:
        if (x, y) in up:
            corners += 1
        if (x, y) in down:
            corners += 1
        if (x - 1, y - 1) in down and (x, y) not in up:
            corners += 1
        if (x - 1, y + 1) in up and (x, y) not in down:
            corners += 1

    for (x, y) in right:
        if (x, y) in up:
            corners += 1
        if (x, y) in down:
            corners += 1
        if (x + 1, y - 1) in down and (x, y) not in up:
            corners += 1
        if (x + 1, y + 1) in up and (x, y) not in down:
            corners += 1

    return corners

# corners = count_corners(plots_sorted)
# print(corners)

part2 = 0
for k, v in plots.items():
    area_sorted = sorted(v["points"], key=lambda x: tuple(reversed(x)))
    part2 += v["count"] * count_corners(area_sorted)
    
print(part2)