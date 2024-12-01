from .Car import Car


class Board:
    def __init__(self, grid):
        self.gui = None
        self.grid = grid
        self.cars = self._parse_cars()
        self.grid_size = 6

    #метод для парсингу даних з файлу, запис позицій машинок
    def _parse_cars(self):
        cars = {}
        for row_idx, row in enumerate(self.grid):
            for col_idx, cell in enumerate(row):
                if cell != '.':
                    if cell not in cars:
                        cars[cell] = Car(cell)
                    cars[cell].add_position(row_idx, col_idx)
        return cars

    def is_valid_move(self, car, direction):
        dx, dy = 0, 0
        #рух машинок за допомогою стрілочок відносно орієнтації машинок на полі (якщо машинка знаходиться горизонтально на полі, то рухатися вона теж може тільки по горизонталі)
        if direction == "up" and car.orientation == "vertical":
            dx = -1
        elif direction == "down" and car.orientation == "vertical":
            dx = 1
        elif direction == "left" and car.orientation == "horizontal":
            dy = -1
        elif direction == "right" and car.orientation == "horizontal":
            dy = 1
        else:
            return False

        new_positions = [(x + dx, y + dy) for x, y in car.positions]

        #перевірка на межі (чи не виходить машинка за межі)
        if not all(0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]) for x, y in new_positions):
            return False

        #перевірка на перешкоди (чи нема іншої машинки)
        for x, y in new_positions:
            if self.grid[x][y] != "." and self.grid[x][y] != car.name:
                return False

        return True

    def move_car(self, car, direction):
        dx, dy = 0, 0
        if direction == "up":
            dx = -1
        elif direction == "down":
            dx = 1
        elif direction == "left":
            dy = -1
        elif direction == "right":
            dy = 1

        #очищення старих позицій
        for x, y in car.positions:
            self.grid[x][y] = "."

        #оновлення позицій
        car.positions = [(x + dx, y + dy) for x, y in car.positions]

        #запис нових позицій
        for x, y in car.positions:
            self.grid[x][y] = car.name

    @staticmethod
    #зчитування даних з файлу
    def init_board(file):
        grid = []
        with open(file, 'r') as f:
            for line in f:
                grid.append(line.strip().split())
        return grid