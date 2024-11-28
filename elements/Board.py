from .Car import Car


class Board:
    def __init__(self, grid):
        self.grid = grid
        self.cars = self._parse_cars()

    def _parse_cars(self):
        cars = {}  ##словник, ключі - букви A, B, C... значення - об'єкти класу Car
        for row_idx, row in enumerate(self.grid):  # enumerate — дозволяє обирати одночасно індекс і значення об'єкта
            for col_idx, cell in enumerate(row):  ##col_idx - індекс клітинки, cell - значення A, B, C
                if cell != '.':
                    if cell not in cars:
                        cars[cell] = Car(cell)  ##створення об'єкта Car з cell
                    cars[cell].add_position(row_idx, col_idx)  ##додаємо індекс до машини
        return cars

    @staticmethod
    def init_board(file):
        grid = []
        with open(file, 'r') as f:
            for line in f:
                grid.append(line.strip().split())
        return grid
