import turtle as t
from random import randint

screen = t.Screen()

tim = t.Turtle()
tim.speed(0)
tim.pensize(2)
tim.hideturtle()

t.colormode(255)

def random_rgb_color():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return (r, g, b)
def draw_spirograph(size_of_gap):
    for _ in range(int(360 / size_of_gap)):
        tim.color(random_rgb_color())
        tim.circle(100)
        tim.setheading(tim.heading() + size_of_gap)

draw_spirograph(5)
screen.exitonclick()
