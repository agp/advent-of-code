import re
from itertools import permutations

with open("./13/input.txt") as f:
    input = [machine.split("\n") for machine in f.read().split("\n\n")]

machines = []
for machine in input:
    d = {}
    for line in machine:
        re_line = re.search(r"(?:Button )?([AB]|Prize): X[+=](\d+), Y[+=](\d+)", line)
        d[re_line.group(1)] = (int(re_line.group(2)), int(re_line.group(3)))
    machines.append(d)


def press_button(button, times):
    x = button[0] * times
    y = button[1] * times
    return (x, y)


# can't do the maths...
cost = 0
combos = [(b, a) for b, a in permutations(range(0, 100), 2)]
for m in machines:
    for b, a in combos:
        bx, by = press_button(m["B"], b)
        ax, ay = press_button(m["A"], a)
        if m["Prize"] == (bx + ax, by + ay):
            cost += b * 1 + a * 3

print(cost)
