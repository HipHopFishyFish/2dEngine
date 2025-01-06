import r2d

MOVESPEED = 150


class Player(r2d.sceneObj):
    timer = 0.0

    def update(self):
        self.timer += self.time_delta
        if self.events.key("w"):
            self.position = (
                self.position[0],
                self.position[1] + (self.time_delta * MOVESPEED),
            )

        if self.events.key("s"):
            self.position = (
                self.position[0],
                self.position[1] - (self.time_delta * MOVESPEED),
            )

        if self.timer > 3:
            sceneManager.load_scene("scene2")


r2d.initialise()

window = r2d.Window()

player = Player(window, "Player", (0, 0))
rend = r2d.BoxRenderer(player, 50, "#FF0000")

myBox = r2d.sceneObj(window, "myBox", (0, 0))
rend2 = r2d.BoxRenderer(myBox, 20, "#00FF00")

cam = r2d.Camera(window, (0, 0))

sceneManager = r2d.SceneManager(
    window, {"scene1": [r2d.copy(player), cam], "scene2": [r2d.copy(player), myBox, cam]}
)

window.run()
