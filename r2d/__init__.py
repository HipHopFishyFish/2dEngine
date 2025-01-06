"""
r2d: Framework used for creating games

Simple player:
### player.py
--------------------------------------------------------------------
```python
from r2d import sceneObj

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
```
--------------------------------------------------------------------
Startup code:
### main.py
---------------------------------------------------------------
```python
from r2d import initialise, Window, Camera, Player, BoxRenderer
from player import Player
initialise()

win = Window(resizable=True)
cam = Camera(win, (0, 0))
player = Player(win, "player", (0, 0))
rend = BoxRenderer(player, 20, "red")
win.run()
```
---------------------------------------------------------------

This will make a small red box on the screen that can be moved with the
WASD keys. If you press the `#` key, the box will change colour
"""

import copy as _copy
import string
import threading
import time
import tkinter as tk
import r2d.events as events_module
import keyboard

FRAME_BETWEEN = 0.016665

key_dictionary = {key: False for key in string.ascii_lowercase}


def createMasterWindow(geometryX, geometryY, resizable, title):
    win = tk.Tk()
    win.title(title)
    win.geometry(f"{geometryX}x{geometryY}")
    win.resizable(resizable, resizable)
    return win


def createCanvas(master, geometryX, geometryY):
    canvas = tk.Canvas(master, bg="#000000", width=geometryX, height=geometryY)
    canvas.pack()
    return canvas


def keyPressHook(event):
    key_dictionary[event.name] = event.event_type == "down"

def copy(obj):
    return _copy.copy(obj)

def copy_list(objs):
    return [copy(obj) for obj in objs]


stopped = False
id = 0
windows = []
all_scene_objects = {}
current_scene_manager = None


def initialise():
    keyboard.hook(keyPressHook, suppress=True)


def _stop(e=None):
    global stopped
    if not stopped:
        print("Stopping...")
        stopped = True
        keyboard.unhook_all()
        for window in windows:
            window.stop()


class Window:
    def __init__(
        self,
        geometryX: int = 500,
        geometryY: int = 500,
        resizable: bool = False,
        title="2Dengine game",
    ):
        global windows

        windows.append(self)
        self.master = createMasterWindow(geometryX, geometryY, resizable, title)
        self.canvas = createCanvas(self.master, geometryX, geometryY)
        self.listeners = []
        self.positions = {}
        self.events = events_module.Events()
        self.stop_event = threading.Event()  # Used to signal stopping the update loop
        self.update_thread = threading.Thread(target=self.update_loop)
        self.time_delta = 0.0
        self.geometryX = geometryX
        self.geometryY = geometryY
        self.master.protocol(
            "WM_DELETE_WINDOW", _stop
        )  # Bind close window to stop function

    def update_loop(self):
        for listener in self.listeners:
            listener.pre_start()
            for component in listener.components:
                component.pre_start()

        if current_scene_manager:
            current_scene_manager.load_scene(current_scene_manager.current_scene)

        curr_time = time.time()
        frame = 0
        while not self.stop_event.is_set():  # Check if stop signal is set
            self.geometryX, self.geometryY = self.master.geometry().split("x")
            self.geometryX, self.geometryY = int(self.geometryX.split("+")[0]), int(
                self.geometryY.split("+")[0]
            )
            self.record_events()
            for listener in self.listeners:
                if listener.is_active:
                    if frame == 0:
                        listener.start()
                        for component in listener.components:
                            component.start()
                    listener._pre_update(self.events, self.positions[listener.id])
                    listener.update()
                    self.positions[listener.id] = listener.position

            self.events = events_module.Events()
            self.time_delta = time.time() - curr_time

            if self.time_delta < FRAME_BETWEEN:
                time.sleep(FRAME_BETWEEN - self.time_delta)
                self.time_delta = time.time() - curr_time
            curr_time = time.time()

        print("Exiting update loop...")

    def add_listener(self, listener):
        self.listeners.append(listener)

    def record_events(self):
        for key, pressed in key_dictionary.items():
            if pressed:
                self._key_press(key)

    def _key_press(self, key):
        self.events.add_event(events_module.Event("keypress", key))

    def run(self):
        self.update_thread.start()  # Start the update loop in a separate thread
        self.master.mainloop()  # Run the Tkinter main loop

    def stop(self):
        print("Stopping the update loop...")
        self.stop_event.set()  # Signal the thread to stop
        if self.update_thread.is_alive():
            self.update_thread.join(timeout=1) # Wait for the update loop to stop
        print("Update thread stopped.")
        self.master.quit()  # Stop the Tkinter main loop
        self.master.destroy()  # Destroy the Tkinter window


class sceneObj:
    def __init__(self, master, name, position):
        global id
        id += 1
        self.id = id
        self.name = name
        self.is_active = True
        self.components = []
        self.master = master
        self.master.positions[id] = position
        self.position = position
        self.master.add_listener(self)

        all_scene_objects[self.name] = self

    @staticmethod
    def find(name):
        return all_scene_objects[name]

    def _pre_update(self, events, position):
        self.events = events
        self.time_delta = self.master.time_delta
        self.position = position
        for component in self.components:
            component.sceneObj = self
            component.update()

    def pre_start(self): ...
    def start(self): ...

    def has_component(self, component_name):
        for component in self.components:
            if component.name == component_name:
                return True
        return False

    def add_component(self, component):
        self.components.append(component)

    def get_component(self, component_name):
        for component in self.components:
            if component.name == component_name:
                return component
        return None

    def update(self):
        pass


class Component:
    def __init__(self, sceneObj):
        self.sceneObj = sceneObj
        self.sceneObj.components.append(self)
        self.name = "<component>"

    def pre_start(self):
        pass

    def start(self):
        pass

    def update(self):
        pass


class Renderer(Component):
    pass


class BoxRenderer(Renderer):
    def __init__(self, sceneObj, size, colour):
        super().__init__(sceneObj)
        self.name = "PolyRenderer"
        self.size = size
        self.colour = colour
        self.corners = [
            self.sceneObj.position[0] - self.size,
            self.sceneObj.position[1] - self.size,
            self.sceneObj.position[0] + self.size,
            self.sceneObj.position[1] + self.size,
        ]

    def update(self):
        self.corners = [
            self.sceneObj.position[0] - self.size,
            self.sceneObj.position[1] - self.size,
            self.sceneObj.position[0] + self.size,
            self.sceneObj.position[1] + self.size,
        ]


class Camera(sceneObj):
    def __init__(self, master, name, position):
        super().__init__(master, name, position)
        self.lastobjects = []
        self.newobjects = []

    def update(self):
        canvas = self.master.canvas
        self.lastobjects = self.newobjects
        self.newobjects = []
        for obj in self.master.listeners:
            if obj.has_component("PolyRenderer"):
                rend = obj.get_component("PolyRenderer")
                corners = rend.corners
                colour = rend.colour
                screenwidth = self.master.geometryX
                screenheight = self.master.geometryY
                corners = [
                    (
                        screenwidth // 2 - corner
                        if i % 2 == 0
                        else screenheight // 2 - corner
                    )
                    for i, corner in enumerate(corners)
                ]
                if len(corners) < 6:
                    self.newobjects.append(
                        canvas.create_rectangle(corners, fill=colour)
                    )
                else:
                    self.newobjects.append(canvas.create_polygon(corners, fill=colour))
        for obj in self.lastobjects:
            canvas.delete(obj)


class SceneManager:
    def __init__(self, window, scenes: dict[str, list[sceneObj]]):
        global current_scene_manager
        self.scenes = scenes
        self.window = window
        self.window.listeners = []
        self.dont_destroy = []
        self.current = []

        self.current_scene = list(scenes)[0]
        current_scene_manager = self

    def load_scene(self, scene_name):
        print(f"Loading {scene_name}")
        self.dont_destroy = []

        for listener in self.window.listeners + self.scenes[scene_name]:
            listener.pre_start()

        self.window.listeners = self.scenes[scene_name] + self.dont_destroy

        for listener in self.window.listeners:
            listener.start()

    def dont_destroy_on_load(self, obj):
        self.dont_destroy.append(copy(obj))
