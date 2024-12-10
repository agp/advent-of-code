with open("./10/input.txt") as f:
    input = [[int(s) for s in line] for line in f.read().splitlines()]


# check if next cell is in bounds and incrementing by 1 from current cell
def is_valid(
    row: int, col: int, matrix: list[list[int]], current_cell_value: int
) -> bool:
    return (
        0 <= row < len(matrix)
        and 0 <= col < len(matrix[0])
        and matrix[row][col] == current_cell_value + 1
    )


# recursively traverse valid paths for trail
def find_trail(
    row: int, col: int, matrix: list[list[int]], ans: set | list, path_start: str
) -> None:
    current_cell_value = matrix[row][col]
    # 9 means path is complete
    if matrix[row][col] == 9:
        start_end = f"{path_start}:{col}y{row}"
        if isinstance(ans, set):
            ans.add(f"{path_start}:{col}y{row}")
        elif isinstance(ans, list):
            ans.append(start_end)
        return

    # iterate over possible movement directions
    for i in range(len(dr)):
        next_row = row + dr[i]
        next_col = col + dc[i]
        # if next cell is valid, find next path
        if is_valid(next_row, next_col, matrix, current_cell_value):
            find_trail(next_row, next_col, matrix, ans, path_start)


# movement array
dr = [1, 0, 0, -1]
dc = [0, -1, 1, 0]

# unique start and end paths - part 1
result = set()
# total distinct paths - part 2
result_distinct = []

# iterate over input rows/cols
for i, row in enumerate(input):
    for j, col in enumerate(row):
        if input[i][j] == 0:
            start = f"x{j}y{i}"
            find_trail(i, j, input, result, start)
            find_trail(i, j, input, result_distinct, start)


print(len(result))
print(len(result_distinct))
