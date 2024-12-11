from collections import defaultdict

with open("./11/input.txt") as f:
    input = {int(s): 1 for s in f.read().split(" ")}
    # input = {125: 1, 17: 1}


def blink(stones: list) -> list:
    new_stones = defaultdict(int)
    for stone, v in stones.items():
        if stone == 0:
            new_stones[1] += v
        elif len(str(stone)) % 2 == 0:
            middle = int(len(str(stone)) / 2)
            new_stones[(int(str(stone)[:middle]))] += v
            new_stones[(int(str(stone)[middle:]))] += v
        else:
            new_stones[stone * 2024] += v
    # print(new_stones.keys())
    return new_stones


# stones_test = input.copy()
# for i in range(6):
    # stones_test = blink(stones_test)

# print(stones_test.keys())
# print(sum(stones_test.values()))

stones = input.copy()
for i in range(25):
    stones = blink(stones)

print(sum(stones.values()))

stones2 = input.copy()
for i in range(75):
    stones2 = blink(stones2)

print(sum(stones2.values()))
