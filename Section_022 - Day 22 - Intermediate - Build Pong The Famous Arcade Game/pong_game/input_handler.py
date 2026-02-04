class InputHandler:
    def __init__(self, screen):
        self.keys = {
            "Up": False,
            "Down": False,
            "w": False,
            "s": False
        }

        screen.listen()

        screen.onkeypress(lambda: self._press("Up"), "Up")
        screen.onkeyrelease(lambda: self._release("Up"), "Up")

        screen.onkeypress(lambda: self._press("Down"), "Down")
        screen.onkeyrelease(lambda: self._release("Down"), "Down")

        screen.onkeypress(lambda: self._press("w"), "w")
        screen.onkeyrelease(lambda: self._release("w"), "w")

        screen.onkeypress(lambda: self._press("s"), "s")
        screen.onkeyrelease(lambda: self._release("s"), "s")

    def _press(self, key):
        self.keys[key] = True

    def _release(self, key):
        self.keys[key] = False

    def is_pressed(self, key):
        return self.keys[key]
