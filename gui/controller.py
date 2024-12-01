from .interface import RushHourGUI
from elements.Board import Board


class RushHourGame:
    def __init__(self, root, level_file):
        self.root = root
        self.root.title("Rush Hour")

        #завантаження рівня
        self.board = Board(Board.init_board(level_file))

        self.gui = RushHourGUI(self.root, self.board, self.move_car)

        #зв'язування клавіш для руху
        self.root.bind("<Up>", lambda event: self.move_car("up"))
        self.root.bind("<Down>", lambda event: self.move_car("down"))
        self.root.bind("<Left>", lambda event: self.move_car("left"))
        self.root.bind("<Right>", lambda event: self.move_car("right"))

    #логіка руху машинок, деякі обмеження для руху, оновлення поля, перевірка виграшу
    def move_car(self, direction):
        if self.gui.selected_car is None:
            print("No car selected!")
            return

        car = self.board.cars[self.gui.selected_car]
        if not self.board.is_valid_move(car, direction):
            print("Invalid move!")
            return

        self.board.move_car(car, direction)

        self.gui.update_board()

        self.check_win()

    #якщо машинка доходить до позиції [2,5] -> виграш
    def check_win(self):
        car = self.board.cars.get("A")
        if car and (2, 5) in car.positions:
            print("You win!")
            self.root.quit()
