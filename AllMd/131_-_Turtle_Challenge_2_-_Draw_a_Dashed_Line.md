import turtle
from random import choice

screen = turtle.Screen()
screen.setup(800, 600)

t = turtle.Turtle()
t.speed(0)
t.width(3)
t.hideturtle()

colors = ["red", "blue", "green", "purple", "orange", "cyan"]

def move(x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()

move(-350, 200)
t.pencolor(choice(colors))
t.forward(300)

move(-350, 150)
t.pencolor(choice(colors))
for _ in range(15):
    t.forward(10)
    t.penup()
    t.forward(10)
    t.pendown()

move(-350, 100)
t.pencolor(choice(colors))
t.width(6)
t.forward(300)
t.width(3)

move(-350, 50)
t.pencolor(choice(colors))
for _ in range(20):
    t.forward(10)
    t.right(2)

move(-350, 0)
t.pencolor(choice(colors))
for _ in range(30):
    t.forward(8)
    t.left(5)

move(-350, -50)
t.pencolor(choice(colors))
for _ in range(15):
    t.forward(15)
    t.penup()
    t.forward(5)
    t.pendown()

move(-350, -100)
t.pencolor(choice(colors))
for _ in range(40):
    t.forward(5)
    t.right(3)

move(-350, -150)
t.pencolor(choice(colors))
for _ in range(40):
    t.forward(5)
    t.left(3)

turtle.done()
