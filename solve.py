# import subprocess
class Cell:
    def __init__(self, _id, num):
        self.id = _id

        if num == "-":
            self.original = False
            self.number = None
            self.posibles = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        else:
            self.original = True
            self.number = int(num)
            self.posibles = set()

        self.neighbors = []

    @property
    def has_number(self):
        return self.number is not None

    def __repr__(self):
        return f"<Cell {self.id[0]}, {self.id[1]} - {self.number}>"

    def change_to(self, num):
        self.number = num
        self.posibles.clear()
        self.check()

    def check(self):
        if self.has_number:
            for neighbor in self.neighbors:
                Solver.ins.cells[neighbor].remove(self.number)
        elif len(self.posibles) == 1:
            self.number = self.posibles.pop()
            self.check()

    def add(self, number):
        self.posibles.add(number)

    def remove(self, number):
        if number in self.posibles:
            self.posibles.remove(number)
            if len(self.posibles) == 1:
                self.change_to(self.posibles.pop())

    def print(self, line, highlight=""):
        if self.has_number:
            if highlight != "":
                print(highlight, end="")
            elif self.original:
                print("\x1b[0;36;47m", end="")
            else:
                print("\x1b[0;37;44m", end="")

            if line == 0 or line == 2:
                print("   \x1b[0m", end="")
            else:
                print(f" {self.number} \x1b[0m", end="")
        else:
            texts = [" "] * 9
            for num in self.posibles:
                texts[num - 1] = str(num)

            text = "".join(texts)
            if highlight != "":
                print(highlight, end="")

            if line == 0:
                print(text[0: 3], end="\x1b[0m")
            elif line == 1:
                print(text[3: 6], end="\x1b[0m")
            else:
                print(text[6:], end="\x1b[0m")


class Solver:
    ins = None

    def __init__(self):
        Solver.ins = self
        self.cells = []

    @staticmethod
    def get_index(x, y=None):
        if y is None:
            y = x[1]
            x = x[0]
        return y * 9 + x

    @classmethod
    def get_block(cls, x, y):
        coords = []
        for _x in range(0, 3):
            for _y in range(0, 3):
                coords.append(cls.get_index(x * 3 + _x, y * 3 + _y))
        return coords

    @classmethod
    def get_neighbors(cls, _id):
        coords = set()

        x, y = _id
        for _x in range(0, 9):
            coords.add(cls.get_index(_x, y))

        for _y in range(0, 9):
            coords.add(cls.get_index(x, _y))

        blocks = cls.get_block(x // 3, y // 3)
        for block in blocks:
            if block != _id:
                coords.add(block)

        coords.remove(y * 9 + x)
        return coords

    def read(self, text):
        cells = text.replace("\n", "")

        x = y = 0
        for cell_num in cells:
            cell = Cell((x, y), cell_num)
            cell.neighbors = self.get_neighbors((x, y))
            self.cells.append(cell)

            x += 1
            if x >= 9:
                x = 0
                y += 1

    def print_map(self):
        for y in range(0, 9):
            for x in range(0, 9):
                self.cells[self.get_index(x, y)].print(0)
            print()
            for x in range(0, 9):
                self.cells[self.get_index(x, y)].print(1)
            print()
            for x in range(0, 9):
                self.cells[self.get_index(x, y)].print(2)
            print()

    def highlight_print(self, cell):
        for y in range(0, 9):
            for x in range(0, 9):
                _cell = self.cells[self.get_index(x, y)]
                if (x, y) == cell.id:
                    _cell.print(0, "\x1b[1;37;41m")
                elif self.get_index(x, y) in cell.neighbors:
                    _cell.print(0, "\x1b[0;37;43m")
                else:
                    _cell.print(0)
            print()
            for x in range(0, 9):
                _cell = self.cells[self.get_index(x, y)]
                if (x, y) == cell.id:
                    _cell.print(1, "\x1b[1;37;41m")
                elif self.get_index(x, y) in cell.neighbors:
                    _cell.print(1, "\x1b[0;37;43m")
                else:
                    _cell.print(1)
            print()
            for x in range(0, 9):
                _cell = self.cells[self.get_index(x, y)]
                if (x, y) == cell.id:
                    _cell.print(2, "\x1b[1;37;41m")
                elif self.get_index(x, y) in cell.neighbors:
                    _cell.print(2, "\x1b[0;37;43m")
                else:
                    _cell.print(2)
            print()

    def generate_posibles(self):
        for cell in self.cells:
            cell.check()

    def check_unique_cells(self, cells):
        num_sure = {}
        num_posible = {}

        for cell in cells:
            if cell.has_number:
                num_sure[cell.number] = cell.id
            else:
                for num in cell.posibles:
                    if num not in num_posible:
                        num_posible[num] = []
                    num_posible[num].append(cell.id)

        for num, cells in num_posible.items():
            if len(cells) == 1:
                self.cells[self.get_index(cells[0])].change_to(num)

    def check_unique(self):
        for i in range(0, 9):
            self.check_unique_cells(self.cells[i * 9: i * 9 + 9])


if __name__ == "__main__":
    with open("puzzles/5.txt") as file:
        solver = Solver()
        solver.read(file.read())
        solver.generate_posibles()
        solver.check_unique()
        solver.print_map()

    # solver = Solver()
    # solver.read("-316-7---6--8--2578---9-6-34-----832-1--"
    #             "69---7-324---69-24-1-78-85-----93-4----61")
    # solver.generate_posibles()
    # solver.print_map()
