import tkinter as tk


class RushHourGame:
    def __init__(self, roote):
        self.root = roote
        self.root.title("Rush Hour")

        # Розмір сітки
        self.grid_size = 6
        self.cell_size = 60

        # Створення основного фрейму
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Створення сітки
        self.grid = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Позиції машинок
        self.cars = {
            "A": [(2, 1), (2, 2)],  # Горизонтальна машинка
            "B": [(4, 2), (4, 3)],  # Горизонтальна машинка
            "C": [(1, 5), (2, 5), (3, 5)]  # Вертикальна машинка
        }

        # Орієнтація машинок (horizontal/vertical)
        self.car_orientations = {
            "A": "horizontal",
            "B": "horizontal",
            "C": "vertical"
        }

        self.selected_car = None  # Вибрана машинка

        # Створення інтерфейсу
        self.create_grid()
        self.place_cars()

        # Обробка стрілок
        self.root.bind("<Up>", lambda event: self.move_car("up"))
        self.root.bind("<Down>", lambda event: self.move_car("down"))
        self.root.bind("<Left>", lambda event: self.move_car("left"))
        self.root.bind("<Right>", lambda event: self.move_car("right"))

    def create_grid(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                btn = tk.Button(self.frame, text="", width=4, height=2,
                                command=lambda r=row, c=col: self.select_car(r, c))
                btn.grid(row=row, column=col, padx=1, pady=1)
                self.buttons[row][col] = btn

    def place_cars(self):
        car_buttons = {}

        # Створення кнопок для машинок
        for car, positions in self.cars.items():
            first_x, first_y = positions[0]
            last_x, last_y = positions[-1]

            # Горизонтальна машинка
            if first_x == last_x:
                colspan = len(positions)
                btn = tk.Button(self.frame, text=car, width=4 * colspan, height=2,
                                bg="red" if car == "A" else "blue",
                                command=lambda c=car: self.select_car_by_name(c))
                btn.grid(row=first_x, column=first_y, columnspan=colspan, padx=1, pady=1)
                car_buttons[car] = btn
                for x, y in positions:
                    self.grid[x][y] = car
                    self.buttons[x][y] = btn

            # Вертикальна машинка
            elif first_y == last_y:
                rowspan = len(positions)
                btn = tk.Button(self.frame, text=car, width=4, height=2 * rowspan,
                                bg="red" if car == "A" else "blue",
                                command=lambda c=car: self.select_car_by_name(c))
                btn.grid(row=first_x, column=first_y, rowspan=rowspan, padx=1, pady=1)
                car_buttons[car] = btn
                for x, y in positions:
                    self.grid[x][y] = car
                    self.buttons[x][y] = btn

    def select_car_by_name(self, car):
        self.selected_car = car
        print(f"Selected car: {car}")

    def select_car(self, row, col):
        car = self.grid[row][col]
        if car != ".":
            self.selected_car = car
            print(f"Selected car: {car}")

    def move_car(self, direction):
        if not self.selected_car:
            print("No car selected!")
            return

        positions = self.cars[self.selected_car]
        orientation = self.car_orientations[self.selected_car]

        # Заборона руху в неправильному напрямку
        if orientation == "horizontal" and direction in ["up", "down"]:
            print(f"Car {self.selected_car} can only move horizontally!")
            return
        if orientation == "vertical" and direction in ["left", "right"]:
            print(f"Car {self.selected_car} can only move vertically!")
            return

        # Оновлення позицій
        dx, dy = 0, 0
        if direction == "up":
            dx = -1
        elif direction == "down":
            dx = 1
        elif direction == "left":
            dy = -1
        elif direction == "right":
            dy = 1

        new_positions = [(x + dx, y + dy) for x, y in positions]

        # Перевірка меж поля
        if all(0 <= x < self.grid_size and 0 <= y < self.grid_size for x, y in new_positions):
            # Перевірка на перешкоди
            for x, y in new_positions:
                if self.grid[x][y] != "." and self.grid[x][y] != self.selected_car:
                    print("Move blocked!")
                    return

            # Оновлення позицій машинок
            for x, y in positions:
                self.grid[x][y] = "."

            self.cars[self.selected_car] = new_positions

            # Повне перемалювання фрейму
            for widget in self.frame.winfo_children():
                widget.destroy()

            self.create_grid()
            self.place_cars()
        else:
            print("Move out of bounds!")


root = tk.Tk()
# Запуск гри
game = RushHourGame(root)
root.mainloop()
