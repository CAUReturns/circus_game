from models.model import *
from controllers.scene import *


setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.ROOM_TITLE, False)

scene = CircusScene()
scene.add_user(User(scene))
scene.add_obstacle(Obstacle(scene, 1))
scene.add_obstacle(Obstacle(scene, 2))
scene.add_landscape(Landscape(scene, 1))

startGame(scene)
