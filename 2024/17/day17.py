import re
import time

with open("./17/input.txt") as f:
    input = f.read().strip()


class Computer:

    def __init__(self, input: str, init_A: int = None) -> None:
        self.A: int = 0
        self.B: int = 0
        self.C: int = 0
        self.pointer: int = 0
        self.output: list = []
        self.input = input
        registers, program = input.split("\n\n")
        for r in registers.split("\n"):
            r_re = re.search(r"Register ([ABC]): (\d+)", r)
            setattr(self, r_re.group(1), int(r_re.group(2)))
        self.program = [int(c) for c in program.split(": ")[1].split(",")]
        if init_A:
            self.init_A = init_A
            self.A = init_A
        self.init_B = self.B
        self.init_C = self.C

    # reset computer with new initial A register
    def reset(self, init_A: int) -> None:
        self.A = self.init_A = init_A
        self.B = self.init_B
        self.C = self.init_C
        self.output = []
        self.pointer = 0

    # run program until opcode is past end of program
    def run(self) -> None:
        while self.pointer < len(self.program):
            print(self.output)
            self.execute()

    # run but exit early if out and program don't align
    def run_to_copy(self) -> None:
        while self.pointer < len(self.program):
            if self.output == self.program[0 : len(self.output)] and len(
                self.output
            ) <= len(self.program):
                self.execute()
            else:
                break

    # execute program block of opcode and operand
    def execute(self) -> None:
        opcode = self.program[self.pointer]
        operand = self.program[self.pointer + 1]
        adv_pointer = True
        match opcode:
            case 0:  # adv
                self.A = self.A // 2 ** self.get_combo(operand)
            case 1:  # bxl
                self.B = self.B ^ operand
            case 2:  # bst
                self.B = self.get_combo(operand) % 8
            case 3:  # jnz
                if self.A == 0:
                    pass
                else:
                    self.pointer = operand
                    adv_pointer = False
            case 4:  # bxc
                self.B = self.B ^ self.C
                pass
            case 5:  # out
                out = self.get_combo(operand) % 8
                self.output.append(out)
            case 6:  # bdv
                self.B = self.A // 2 ** self.get_combo(operand)
            case 7:  # cdv
                self.C = self.A // 2 ** self.get_combo(operand)
            case _:
                raise ValueError

        self.pointer += 2 if adv_pointer else 0

    # return combo case for operand
    def get_combo(self, operand) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case 7:
                print("7 is reserved")
                raise ValueError
            case _:
                raise ValueError

    def print(self) -> None:
        print(",".join([str(i) for i in self.output]))


computer = Computer(input)
computer.run()
computer.print()

# part 2 - brute force does not work...

# init_A = 117440
# init_A = 8
# c2 = Computer(input, init_A)

# c2 = Computer(input, 2)
# output = None
# program = c2.program
# start_time = time.time()
# while output != program:
#     # init_A += 1
#     init_A = init_A ** 8
#     c2.reset(init_A)
#     # c2.run_to_copy()
#     c2.run()
#     output = c2.output

# print(f"copy at A = {init_A}")
# end_time = time.time()
# print(f"time to run: {end_time-start_time}s")
