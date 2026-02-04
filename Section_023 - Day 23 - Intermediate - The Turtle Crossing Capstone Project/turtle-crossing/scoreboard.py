from turtle import Turtle

FONT = ("Courier", 16, "bold")
SCOREBOARD_POSITION = (-230, 250)

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.color("white")
        self.level = 1
        self.goto(SCOREBOARD_POSITION)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(f"Level: {self.level}", align="center", font=FONT)

    def increase_level(self):
        self.level += 1
        self.clear()
        self.update_scoreboard() 

    def game_over(self):
        self.goto(0, -280)
        self.write("GAME OVER (Press R to restart)", align="center", font=FONT)

    def reset_scoreboard(self):
        self.level = 1
        self.clear()
        self.goto(SCOREBOARD_POSITION)
        self.update_scoreboard()

