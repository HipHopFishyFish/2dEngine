import r2d

class Player(r2d.sceneObj):
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