import turtle as t
from random import choice   

tim=t.Turtle()
tim.speed(0)
tim.width(3)
tim.hideturtle()
color=["red","blue","green","purple","orange","cyan"]
direction=[0,90,180,270]
tim.pensize(10)


for _ in range(200):
    tim.color(choice(color))
    tim.forward(55)
    tim.setheading(choice(direction))