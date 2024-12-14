from collections import defaultdict
import numpy as np

with open("./14/input.txt") as f:
    input = [bot for bot in f.read().splitlines()]

# bounds = {"col": 11, "row": 7}
bounds = {"col": 101, "row": 103}

bots = []
for bot in input:
    d = {}
    pvs = bot.split(" ")
    for pv in pvs:
        k, v = pv.split("=")
        d[k] = np.array([int(v) for v in v.split(",")])
    bots.append(d)


def render_grid(bots: list[dict]) -> None:
    space = {f"{x},{y}": 0 for y in range(bounds["row"]) for x in range(bounds["col"])}
    for b in bots:
        x, y = b["p"]
        space[f"{x},{y}"] += 1
    space_values = np.array(list(space.values()))
    split = np.array_split(space_values, bounds["row"])
    for row in split:
        print("".join([f"\033[32;1m{cell}\033[0m" if cell else "." for cell in row]))
    
def move_bot(bot: dict) -> None:
    bot["p"] = bot["p"] + bot["v"]
    x = bot["p"][0]
    y = bot["p"][1]
    if x < 0:
        bot["p"][0] = bounds["col"] + x
    if x > bounds["col"] - 1:
        bot["p"][0] = x - bounds["col"]
    if y < 0:
        bot["p"][1] = bounds["row"] + y
    if y > bounds["row"] - 1:
        bot["p"][1] = y - bounds["row"]


def get_safety_factor(bots: list[dict]) -> int:
    d = defaultdict(int)
    for b in bots:
        xq = bounds["col"] // 2
        yq = bounds["row"] // 2
        q_divide = np.array([xq, yq])
        q_divide_comp = np.equal(b["p"], q_divide)
        # skip any bot on the dividing lines
        if q_divide_comp.any():
            continue
        q_comp = np.less_equal(b["p"], q_divide)
        if q_comp.all():
            d["q1"] += 1
        elif q_comp[0] == False and q_comp[1] == True:
            d["q2"] += 1
        elif q_comp[0] == True and q_comp[1] == False:
            d["q3"] += 1
        else:
            d["q4"] += 1
    return np.prod(list(d.values()))


bots1 = bots.copy()
for i in range(100):
    for b in bots1:
        move_bot(b)

safety = get_safety_factor(bots1)
print(safety)

bots2 = bots.copy()
i = 0
min_safety = np.inf

while(True):
    for b in bots2:
        move_bot(b)
    i += 1
    safety = get_safety_factor(bots2)
    if safety < min_safety:
        min_safety = safety
        print("***************************************")
        print(f"{i} seconds")
        render_grid(bots2)
        print("***************************************")
    
    