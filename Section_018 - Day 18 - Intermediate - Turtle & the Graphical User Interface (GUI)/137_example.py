import turtle as t
from random import choice
from palette import RGB_COLORS

screen = t.Screen()
screen.colormode(255)

tim = t.Turtle()
tim.speed(0)
tim.hideturtle()
tim.penup()

tim.setheading(225)
tim.forward(300)
tim.setheading(0)

number_of_dots = 100
for dot_count in range(1, number_of_dots + 1):
    tim.dot(20, choice(RGB_COLORS))
    tim.forward(50)
    
    if dot_count % 10 == 0:
        tim.setheading(90)
        tim.forward(50)
        tim.setheading(180)
        tim.forward(500)
        tim.setheading(0)
    

screen.exitonclick()
