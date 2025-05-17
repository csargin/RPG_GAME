from enum import Enum

class GameState(Enum):
    """Enum representing the state of the game."""
    NONE = 0, # No state
    RUNNING = 1, # Game is running
    ENDED = 2, # Game has ended
