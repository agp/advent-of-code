from functools import cache

with open("./19/input.txt") as f:
    input = f.read().strip()

input_p, input_d = input.split("\n\n")

patterns = [pat.strip() for pat in input_p.split(",")]
designs = [colors for colors in input_d.split("\n")]

@cache
def solve_design(design: str) -> int:
    if design == '':
        return 1
    count = 0
    for p in patterns:
        if design.startswith(p):
            remains = design.removeprefix(p)
            count += solve_design(remains)
            
    return count


possible = 0
ways = 0
for d in designs:
    solved = solve_design(d) 
    if solved:
        possible += 1
        ways += solved
        
        
print(possible)
print(ways)