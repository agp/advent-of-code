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
    rows = []
    for y in range(bounds["row"]):
        cells = []
        for x in range(bounds["col"]):
            cell = 0
            for b in bots:
                at_xy = b["p"] == np.array([x, y])
                if at_xy.all():
                    cell += 1
            cells.append(cell)
        rows.append(cells)
    # print("  "+"".join([str(i) for i, c in enumerate(rows[0])]))
    # print("  " + "".join(["-" for c in enumerate(rows[0])]))
    for i, r in enumerate(rows):
        print(f"{i}|" + "".join([str(cell if cell else ".") for cell in r]))


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


for i in range(100):
    for b in bots:
        move_bot(b)

safety = get_safety_factor(bots)
print(safety)
