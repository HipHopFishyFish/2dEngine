class Event:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value


class Events:
    def __init__(self):
        self.events: list[Event] = []

    def add_event(self, event: Event):
        self.events.append(event)

    def key(self, key):
        for event in self.events:
            if event.type == "keypress" and event.value == key:
                return True

        return False

    def any_key(self):
        for event in self.events:
            if event.type == "keypress":
                return True

        return False
