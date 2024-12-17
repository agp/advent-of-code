import re

with open("./17/input.txt") as f:
    input = f.read().strip()


class Computer:
    output: list = []
    pointer: int = 0
    A: int
    B: int
    C: int

    def __init__(self, input):
        registers, program = input.split("\n\n")
        for r in registers.split("\n"):
            r_re = re.search(r"Register ([ABC]): (\d+)", r)
            setattr(self, r_re.group(1), int(r_re.group(2)))
        self.program = [int(c) for c in program.split(": ")[1].split(",")]

    # run program until opcode is past end of program
    def run(self):
        while self.pointer < len(self.program):
            self.execute()

    # execute program block of opcode and operand
    def execute(self):
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
    def get_combo(self, operand):
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

    def print(self):
        print(",".join([str(i) for i in self.output]))
        
computer = Computer(input)
computer.run()
computer.print()
