
import turtle
from random import choice, randint

screen = turtle.Screen()
screen.tracer(0)

t = turtle.Turtle()
t.speed(0)
t.width(2)
t.hideturtle()

colors = [
    "red", "green", "blue", "yellow", "purple",
    "orange", "cyan", "magenta", "white"
]

def dashed_line(steps=10, dash=2, gap=2):
    for _ in range(steps):
        t.forward(dash)
        t.penup()
        t.forward(gap)
        t.pendown()

for _ in range(50):
    t.pencolor(choice(colors))
    t.penup()
    t.goto(randint(-250, 250), randint(-250, 250))
    t.setheading(0)
    t.pendown()
    for _ in range(4):
        dashed_line()
        t.right(90)
    screen.update()

turtle.done()
