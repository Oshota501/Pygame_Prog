import PyGame3d
from PyGame3d.GameObject.Cube import Cube

game = PyGame3d.Application()

game.init() 

cube = Cube(game)
game.get_scene().add_child(cube)

game.start_rendering()