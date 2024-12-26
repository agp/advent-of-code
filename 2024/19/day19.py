from collections import deque, defaultdict

with open("./19/input.txt") as f:
    input = f.read().strip()

input_p, input_d = input.split("\n\n")

patterns = [pat.strip() for pat in input_p.split(",")]
designs = [colors for colors in input_d.split("\n")]

# designs = ['brwrr', 'brwrrr']
# test = 'bwurrg'

def solve_design(design: str):
    if design == '':
        return 1
    for p in patterns:
        if design.startswith(p):
            remains = design.removeprefix(p)
            # print("pattern",p)
            # print("remains",remains)
            solved = solve_design(remains)
            if solved:
                return 1
            else:
                continue
    return 0

# s = solve_design(test)
# print(s)

possible = 0
for d in designs:
    possible += solve_design(d) 

print(possible)