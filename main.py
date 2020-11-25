from models.model import *
from controllers.scene import *


setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.ROOM_TITLE, False)

scene = CircusScene()
scene.add_user(User(scene))
scene.add_obstacle(Dooli(scene, start_time=1))
scene.add_obstacle(Douner(scene, y=200, start_time=4))
scene.add_obstacle(Douner(scene, start_time=7))
scene.add_obstacle(Dooli(scene, start_time=10))
scene.add_obstacle(Dooli(scene, y=200, start_time=14))
scene.add_landscape(Landscape(scene))

startGame(scene)
