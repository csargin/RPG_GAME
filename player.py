import config

class Player:
    def __init__(self, x_position, y_position):
        print("Player created")
        self.attack = 2
        self.defense = 1
        self.health = 60
        self.position = [x_position, y_position ]

    def update_position(self, direction):     
        r, c = self.position
        if direction == "up": r = max(0, r - 1)
        elif direction == "down": r = min(config.ROWS - 1, r + 1)
        elif direction == "left": c = max(0, c - 1)
        elif direction == "right": c = min(config.COLS - 1, c + 1)
        self.position = [r, c]
      