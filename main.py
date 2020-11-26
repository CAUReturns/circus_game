from controllers.manager import *
from controllers.scene import *
from bangtal import *

setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.ROOM_TITLE, False)

game_manager = GameManager()
game_manager.start_game()
startGame(game_manager.get_stage())
