from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 240


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("white","black")
        self.shapesize(stretch_wid=1, stretch_len=1)
        self.penup()
        self.goto(STARTING_POSITION)
        self.setheading(90)
        self.reset_position()

    def reset_position(self):
        self.goto(STARTING_POSITION)

    def move(self):
        self.forward(MOVE_DISTANCE)

    def move_left(self):
        self.setheading(180)
        self.forward(MOVE_DISTANCE)
        self.setheading(90)

    def move_right(self):
        self.setheading(0)
        self.forward(MOVE_DISTANCE)
        self.setheading(90)

    def is_at_finish_line(self):
        return self.ycor() > FINISH_LINE_Y
