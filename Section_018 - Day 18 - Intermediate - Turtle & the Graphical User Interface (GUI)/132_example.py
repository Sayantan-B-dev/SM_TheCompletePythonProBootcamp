import turtle as t
from random import choice

tim=t.Turtle()
tim.speed(5)
tim.width(3)
tim.hideturtle()
color=["red","blue","green","purple","orange","cyan"]

def draw_shape(num_sides):
    for _ in range(num_sides):
        tim.forward(100)
        tim.right(360/num_sides)

for shape_side in range(3,11):
    tim.color(choice(color))
    draw_shape(shape_side)
turtle.done()