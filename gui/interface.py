import tkinter as tk

class RushHourGUI:
    def __init__(self, root, board, move_callback):
        self.root = root
        self.board = board
        self.move_callback = move_callback
        self.selected_car = None

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.buttons = [[None for _ in range(board.grid_size)] for _ in range(board.grid_size)]

        self.create_grid()
        self.update_board()

    def create_grid(self):
        for row in range(self.board.grid_size):
            for col in range(self.board.grid_size):
                btn = tk.Button(self.frame, text="", width=4, height=2,
                                command=lambda r=row, c=col: self.select_car(r, c))
                btn.grid(row=row, column=col, padx=1, pady=1)
                self.buttons[row][col] = btn

    def update_board(self):
        # Очищення кнопок
        for row in self.buttons:
            for btn in row:
                btn.config(text="", bg="white")

        # Відображення машин
        for car in self.board.cars.values():
            for x, y in car.positions:
                btn = self.buttons[x][y]
                btn.config(text=car.name, bg="blue" if self.selected_car != car.name else "red")

    def select_car(self, row, col):
        car_name = self.board.grid[row][col]
        if car_name != ".":
            self.selected_car = car_name
            print(f"Selected car: {car_name}")
