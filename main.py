import random
import config
from pyweb import pydom
from pyscript import document
from pyodide.ffi import create_proxy
from player import Player
from game_state import GameState

class Game:
    """
        A RPG game written in PyScript
    """
    def __init__(self):
        self.log = document.getElementById("output_div")
        self.log_el = document.getElementById("log")
        self.game_el = document.getElementById("game")
        self.console = pydom["script#console"][0]

        # Initialize player
        self.player = Player(5,5)

        # start game
        self.new_game(None)
        
        # Set up event listeners for buttons
        document.getElementById("move_up_btn").addEventListener("click", create_proxy(lambda e: self.move("up")))
        document.getElementById("move_down_btn").addEventListener("click", create_proxy(lambda e: self.move("down")))
        document.getElementById("move_left_btn").addEventListener("click", create_proxy(lambda e: self.move("left")))
        document.getElementById("move_right_btn").addEventListener("click", create_proxy(lambda e: self.move("right")))

    def new_game(self, event):
        """
            Starts new game        
        """

        self.clear_terminal()
        self.gamestate = GameState.RUNNING 
        self.log.innerHTML =""
        
        # Enemies: (row, col)        
        self.enemies = []
        while len(self.enemies) < config.NUM_ENEMY:
            pos = [random.randint(0, config.ROWS-1), random.randint(0, config.COLS-1)]
            if pos != self.player.position and pos not in self.enemies:
                self.enemies.append(pos)

        self.render()
        print('=================')
        print('NEW GAME STARTING')              

    def render(self):
        """
            Draws objects on map.        
        """
        self.game_el.innerHTML = ""
        for r in range(config.ROWS):
            for c in range(config.COLS):
                tile = document.createElement("div")
                tile.classList.add("tile")
                if [r, c] == self.player.position:
                    tile.classList.add("player")
                    img = document.createElement("img")
                    img.setAttribute("src", config.PLAYER_IMAGE )  # Adjust path as needed
                    img.setAttribute("width", config.SCALE )   # Set width in pixels
                    img.setAttribute("height", config.SCALE)  # Set height in pixels
                    img.classList.add("sprite")
                    tile.appendChild(img)                    
                elif [r, c] in self.enemies:
                    tile.classList.add("enemy")
                    tile.innerText = "E"
                self.game_el.appendChild(tile)
    
    def move(self, direction):
        if self.gamestate == GameState.RUNNING: 
            self.player.update_position(direction)
            if self.player.position in self.enemies:
                self.fight(self.player.position)
            self.render()
        
    def log_message(self, text):
        self.log_el.innerHTML += text + "<br>"
        self.log_el.scrollTop = self.log_el.scrollHeight

    def fight(self , enemy_pos):        
        damage = random.randint(5, 20)
        self.player.health -= damage
        self.log_message(f"Fought an enemy! Lost {damage} HP. HP: {self.player.health}")
        if self.player.health <= 0:
            self.log_message("You died! Refresh to restart.")
            self.gamestate = GameState.ENDED
        else:
            self.enemies.remove(enemy_pos)

        if not self.enemies:
            self.log_message("All enemies defeated! You win!")
            self.gamestate = GameState.ENDED

    def clear_terminal(self):
        self.console._js.terminal.clear()
    
    def toggle_terminal(self, event):
        hidden = self.console.parent._js.getAttribute("hidden")
        if hidden:
            self.console.parent._js.removeAttribute("hidden")
        else:
            self.console.parent._js.setAttribute("hidden", "hidden")

GAME = Game()