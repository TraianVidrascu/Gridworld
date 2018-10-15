class Grid:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    ACTIONS = [NORTH, EAST, SOUTH, WEST]

    def __init__(self):
        self.size = 5

    def is_special(self, x, y):
        if x == 0 and y == 1:
            return 10, 4, 1
        elif x == 0 and y == 3:
            return 5, 2, 3
        return -1, 0, 0

    def move(self, x, y, action):
        v = self.is_special(x, y)
        if v[0] != -1:
            return v
        return self.basic_moves(x, y, action)

    def move_terminal(self, x, y, action):
        r, v1, v2 = self.is_special(x, y)
        if r != -1:
            return r, -1, -1
        if action == 0:
            if x - 1 >= 0:
                x -= 1
                return 0, x, y
            else:
                return -1, x, y

        elif action == 1:
            if y + 1 < self.size:
                y += 1
                return 0, x, y
            else:
                return -1, x, y

        elif action == 2:
            if x + 1 < self.size:
                x += 1
                return 0, x, y
            else:
                return -1, x, y

        elif action == 3:
            if y - 1 >= 0:
                y -= 1
                return 0, x, y
            else:
                return -1, x, y

    def basic_moves(self, x, y, action):
        if action == 0:
            if x - 1 >= 0:
                x -= 1
                return 0, x, y
            else:
                return -1, x, y

        elif action == 1:
            if y + 1 < self.size:
                y += 1
                return 0, x, y
            else:
                return -1, x, y

        elif action == 2:
            if x + 1 < self.size:
                x += 1
                return 0, x, y
            else:
                return -1, x, y

        elif action == 3:
            if y - 1 >= 0:
                y -= 1
                return 0, x, y
            else:
                return -1, x, y
