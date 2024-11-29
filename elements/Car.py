class Car:
    def __init__(self, name):
        self.name = name
        self.positions = []

    def add_position(self, x, y):
        self.positions.append((x, y))