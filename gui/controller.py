
import tkinter as tk
from elements.Board import Board
from algorithms.dfs import RushHourSolverDFS  # Ваш клас RushHourSolver


class RushHourGame:
    def __init__(self, root, level_file):
        self.root = root
        self.board = Board(Board.init_board(level_file))
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        # Додамо кнопку для автоматичного рішення гри
        self.solve_button = tk.Button(root, text="Auto Solve", command=self.auto_solve)
        self.solve_button.pack()

        self.selected_car = None

        self.draw_board()

        # Зв'язуємо клавіші для переміщення машинок
        self.root.bind("<Up>", lambda event: self.move_car("up"))
        self.root.bind("<Down>", lambda event: self.move_car("down"))
        self.root.bind("<Left>", lambda event: self.move_car("left"))
        self.root.bind("<Right>", lambda event: self.move_car("right"))

    def draw_board(self):
        self.canvas.delete("all")
        cell_size = 400 // self.board.grid_size

        for row_idx, row in enumerate(self.board.grid):
            for col_idx, cell in enumerate(row):
                x1, y1 = col_idx * cell_size, row_idx * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                color = "white" if cell == "." else "lightblue"
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                if cell != ".":
                    self.canvas.create_text(
                        (x1 + x2) // 2, (y1 + y2) // 2, text=cell, font=("Arial", 14)
                    )
                    # Додаємо обробник події для вибору машинки при натисканні
                    self.canvas.tag_bind(rect, "<Button-1>", lambda event, car_name=cell: self.select_car(car_name))

    def update_board_view(self):
        """Оновлює візуальне представлення стану гри."""
        self.draw_board()

    def auto_solve(self):
        solver = RushHourSolverDFS(self.board)
        solution = solver.solve()
        if solution:
            print(f"Solution found in {len(solution)} steps.")
            self.animate_solution(solution)
        else:
            print("No solution found!")

    def animate_solution(self, solution):
        def perform_step(index):
            if index >= len(solution):
                return
            car_name, direction = solution[index]
            self.board.move_car(self.board.cars[car_name], direction)
            self.update_board_view()
            self.root.after(500, perform_step, index + 1)

        perform_step(0)

    def move_car(self, direction):
        """Рух вибраної машинки за допомогою клавіатури."""
        if self.selected_car is None:
            print("No car selected!")
            return

        car = self.board.cars[self.selected_car]
        if not self.board.is_valid_move(car, direction):
            print("Invalid move!")
            return

        self.board.move_car(car, direction)

        # Оновлення GUI
        self.update_board_view()

        # Перевірка на виграш
        self.check_win()

    def check_win(self):
        """Перевіряє, чи виграв користувач."""
        car = self.board.cars.get("A")
        if car and (2, 5) in car.positions:
            print("You win!")
            self.root.quit()

    def select_car(self, car_name):
        """Вибір машинки для руху користувачем."""
        self.selected_car = car_name
        print(f"Selected car: {car_name}")
