import heapq
import itertools


class A_star:
        def __init__(self, board):
            self.start_state = board
            self.goal = (2, 5)
            self.counter = itertools.count()  # Унікальний індекс для кожного елемента

        def solve(self):
            open_set = []
            visited = set()  # Для уникнення дублювання станів
            heapq.heappush(open_set, (0, next(self.counter), self.start_state))
            came_from = {}
            g_score = {self.start_state: 0}
            f_score = {self.start_state: self.heuristic(self.start_state)}

            steps = 0
            while open_set:
                steps += 1
                if steps % 1000 == 0:
                    print(f"Steps processed: {steps}, Open set size: {len(open_set)}")

                _, _, current = heapq.heappop(open_set)
                if self.is_goal(current):
                    return self.reconstruct_path(came_from, current)

                visited.add(hash(current))
                for neighbor, action in self.get_neighbors(current):
                    if hash(neighbor) in visited:
                        continue

                    tentative_g_score = g_score[current] + 1
                    if tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = (current, action)
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor)
                        heapq.heappush(open_set, (f_score[neighbor], next(self.counter), neighbor))

            print("No solution found!")
            return None

        def get_neighbors(self, state):
            neighbors = []
            for car_name, car in state.cars.items():
                for direction in ["up", "down", "left", "right"]:
                    if state.is_valid_move(car, direction):
                        new_state = state.copy()
                        new_state.move_car(new_state.cars[car_name], direction)
                        neighbors.append((new_state, (car_name, direction)))
            return neighbors

        def heuristic(self, state):
            """Евристика для A*"""
            car = state.cars.get("A")
            if car:
                target_row, target_col = 2, 5
                blocking_cars = 0

                # Рахуємо кількість машин, які блокують шлях "A"
                for col in range(car.positions[0][1] + 1, target_col + 1):
                    if state.grid[car.positions[0][0]][col] != ".":
                        blocking_cars += 1

                # Відстань до цільової комірки
                return abs(car.positions[0][1] - target_col) + blocking_cars
            return float('inf')

        def is_goal(self, state):
            car = state.cars.get("A")
            if car and (2, 5) in car.positions:
                return True
            return False

        def reconstruct_path(self, came_from, current):
            path = []
            while current in came_from:
                current, action = came_from[current]
                path.append(action)
            return path[::-1]
