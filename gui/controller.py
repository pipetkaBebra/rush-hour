import tkinter as tk
from elements.Board import Board
from algorithms.dfs import RushHourSolverDFS  # Ваш клас RushHourSolver


class RushHourGame:
    def __init__(self, root, level_file):
        self.root = root
        self.level_file = level_file  # Збережемо шлях до файлу рівня
        self.board = Board(Board.init_board(level_file))
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        # Додамо кнопки
        self.solve_button = tk.Button(root, text="DFS", command=self.auto_solve)
        self.solve_button.pack(side=tk.LEFT)

        self.restart_button = tk.Button(root, text="Restart", command=self.restart_game)
        self.restart_button.pack(side=tk.LEFT)

        self.a_star_button = tk.Button(root, text="A*", command=self.a_star_solve)
        self.a_star_button.pack(side=tk.LEFT)

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
                    self.canvas.tag_bind(
                        rect, "<Button-1>", lambda event, car_name=cell: self.select_car(car_name)
                    )

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
        if not car:
            print("Car A not found!")
            return

        # Перевірка, чи машинка `A` досягла правого краю (наприклад, вихід на позиції (2, 5))
        for x, y in car.positions:
            if y == self.board.grid_size - 1:  # Правий край дошки
                print("You win!")
                self.root.quit()
                return

    def select_car(self, car_name):
        """Вибір машинки для руху користувачем."""
        self.selected_car = car_name
        print(f"Selected car: {car_name}")

    def restart_game(self):
        """Перезапускає гру, скидаючи стан поля."""
        print("Restarting the game...")
        self.board = Board(Board.init_board(self.level_file))
        self.selected_car = None
        self.update_board_view()

    def a_star_solve(self):
        """Метод для майбутньої реалізації A*."""
        print("A* solve is not implemented yet!")
