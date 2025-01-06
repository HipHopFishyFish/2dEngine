import sys

sys.path.append(r"../")

import r2d
from player import Player


scenes = {}
r2d.initialise()

win = r2d.Window()
player = Player(win, 'player', (0,0))
r2d.BoxRenderer(player, 30, "#00FF00")

cam = r2d.Camera(win, 'cam', (0,0))

box = r2d.sceneObj(win, 'box', (200,0))
r2d.BoxRenderer(box, 25, "#FF0000")



scenes.update({"scene1": [player, cam, box]})



sceneManager = r2d.SceneManager(win, scenes)

win.run()