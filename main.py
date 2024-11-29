from gui.controller import RushHourGame
import tkinter as tk

def run_game():
    # level_grid = Board.init_board('levels/level1.txt')
    # board = Board(level_grid)
    #
    # print("Vehicles on the board:")
    # for vehicle_id, vehicle in board.cars.items():
    #     print(f"Vehicle {vehicle_id}: {vehicle.positions}")
    #
    # print("Game initialized!")
    root = tk.Tk()
    RushHourGame(root, 'levels/level1.txt')
    root.mainloop()


if __name__ == '__main__':
    run_game()