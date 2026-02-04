class InputHandler:
    def __init__(self, screen):
        self.keys = {
            "Up": False,
            "Left": False,
            "Right": False,
            "w": False,
            "a": False,
            "d": False,
            "r": False
        }

        screen.listen()

        screen.onkeypress(lambda: self._press("r"), "r")
        screen.onkeyrelease(lambda: self._release("r"), "r")
        
        screen.onkeypress(lambda: self._press("Up"), "Up")
        screen.onkeyrelease(lambda: self._release("Up"), "Up")

        screen.onkeypress(lambda: self._press("Left"), "Left")
        screen.onkeyrelease(lambda: self._release("Left"), "Left")

        screen.onkeypress(lambda: self._press("Right"), "Right")
        screen.onkeyrelease(lambda: self._release("Right"), "Right")

        screen.onkeypress(lambda: self._press("w"), "w")
        screen.onkeyrelease(lambda: self._release("w"), "w")

        screen.onkeypress(lambda: self._press("a"), "a")
        screen.onkeyrelease(lambda: self._release("a"), "a")

        screen.onkeypress(lambda: self._press("d"), "d")
        screen.onkeyrelease(lambda: self._release("d"), "d")

    def _press(self, key):
        self.keys[key] = True

    def _release(self, key):
        self.keys[key] = False

    def is_pressed(self, key):
        return self.keys[key]
