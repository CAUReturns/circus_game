from controllers.game_manager import *

setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.ROOM_TITLE, False)

curr_stage = 0

game_manager = GameManager()
game_manager.init_stage(curr_stage)
game_manager.start_game()
