import turtle as t

class MapManager:

    def __init__(self, image, width, height, title):
        self.screen = t.Screen()
        self.screen.title(title)
        self.screen.addshape(image)
        self.screen.setup(width=width, height=height)

        self.map_turtle = t.Turtle(shape=image)
        self.map_turtle.penup()

        self.writer = t.Turtle()
        self.writer.hideturtle()
        self.writer.penup()

    def ask_state(self, score, total):
        return self.screen.textinput(
            title=f"{score}/{total} Guess the State",
            prompt="Type a state name or 'Exit'"
        )

    def write_state(self, name, x, y):
        self.writer.goto(x, y)
        self.writer.write(name, align="center", font=("Arial", 8, "normal"))

    def close_on_click(self):
        self.screen.exitonclick()
