from r2d import sceneObj, initialise, Window, Camera, BoxRenderer


class Player(sceneObj):
    colours = {"green": "red", "red": "green"}
    timer = 0

    def update(self):
        self.timer += self.time_delta

        if self.events.key("a"):
            self.position = (self.position[0] + 2, self.position[1])
        if self.events.key("w"):
            self.position = (self.position[0], self.position[1] + 2)
        if self.events.key("d"):
            self.position = (self.position[0] - 2, self.position[1])
        if self.events.key("s"):
            self.position = (self.position[0], self.position[1] - 2)

        if self.events.key("#") and self.timer > 0.2:
            self.get_component("PolyRenderer").colour = self.colours[
                self.get_component("PolyRenderer").colour
            ]
            sceneObj.find("player2").get_component("PolyRenderer").colour = (
                self.colours[self.get_component("PolyRenderer").colour]
            )
            self.timer = 0


class Player2(sceneObj):
    def update(self):
        if self.events.key("j"):
            self.position = (self.position[0] + 2, self.position[1])
        if self.events.key("i"):
            self.position = (self.position[0], self.position[1] + 2)
        if self.events.key("l"):
            self.position = (self.position[0] - 2, self.position[1])
        if self.events.key("k"):
            self.position = (self.position[0], self.position[1] - 2)


initialise()

win = Window(resizable=True)
cam = Camera(win, (0, 0))
player = Player(win, "player", (0, 0))
rend = BoxRenderer(player, 20, "red")

player2 = Player2(win, "player2", (70, 0))
rend2 = BoxRenderer(player2, 20, "green")

win.run()
