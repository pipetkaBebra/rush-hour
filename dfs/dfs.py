def get_neighbors(state):
    neighbors = []
    for r, row1 in enumerate(state):
        for c, cell in enumerate(row1):
            if cell != '.':
                if c < len(row1) - 1 and row1[c + 1] == cell:
                    if c > 0 and row1[c - 1] == '.':
                        new_state = [list(row2) for row2 in state]
                        new_state[r][c - 1] = cell
                        new_state[r][c + len(cell) - 1] = '.'
                        neighbors.append([''.join(row) for row in new_state])
                    if c + len(cell) < len(row1) and row1[c + len(cell)] == '.':
                        new_state = [list(row) for row in state]
                        new_state[r][c + len(cell)] = cell
                        new_state[r][c] = '.'
                        neighbors.append([''.join(row) for row in new_state])
                if r < len(state) - 1 and state[r + 1][c] == cell:
                    if r > 0 and state[r - 1][c] == '.':
                        new_state = [list(row) for row in state]
                        new_state[r - 1][c] = cell
                        new_state[r + len(cell) - 1][c] = '.'
                        neighbors.append([''.join(row) for row in new_state])
                    if r + len(cell) < len(state) and state[r + len(cell)][c] == '.':
                        new_state = [list(row) for row in state]
                        new_state[r + len(cell)][c] = cell
                        new_state[r][c] = '.'
                        neighbors.append([''.join(row) for row in new_state])
    return neighbors


class RushHour:
    def __init__(self):
        self.target_exit = None
        self.target_car = None
        self.board = None

    def init(self, board1):
        self.board = board1
        self.target_car = 'R'
        self.target_exit = len(board1[0]) - 1

    def is_goal(self, state):
        for row0 in state:
            if self.target_car in row0 and row0.index(self.target_car) == self.target_exit:
                return True
        return False

    def solve(self):
        stack = [(self.board, [])]
        visited = set()

        while stack:
            current_state, path = stack.pop()

            if self.is_goal(current_state):
                return path

            visited.add(tuple(tuple(row) for row in current_state))

            for neighbor in get_neighbors(current_state):
                if tuple(tuple(row) for row in neighbor) not in visited:
                    stack.append((neighbor, path + [neighbor]))

        return None


board = [
    ['.', '.', '.', '.', '.', '.'],
    ['.', 'B', 'B', '.', '.', '.'],
    ['.', '.', '.', 'R', '.', '.'],
    ['A', 'A', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.']
]

rush_hour = RushHour(board)
solution = rush_hour.solve()

if solution:
    print("Solve it")
    for step in solution:
        for row in step:
            print(row)
        print()
else:
    print("Cant solve it")