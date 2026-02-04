from turtle import Turtle, Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
from input_handler import InputHandler # chanded here
import time


screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong Game")
screen.tracer(0)

r_paddle=Paddle((350,0))
l_paddle=Paddle((-350,0))
ball=Ball()
scoreboard=Scoreboard()
input_handler = InputHandler(screen) # chanded here

screen.listen() 


game_is_on=True
while game_is_on:

    # replcaement of screen.onkey(..., "Up") from outside while loop
    if input_handler.is_pressed("Up"):
        r_paddle.go_up()
    if input_handler.is_pressed("Down"):
        r_paddle.go_down()
    if input_handler.is_pressed("w"):
        l_paddle.go_up()
    if input_handler.is_pressed("s"):
        l_paddle.go_down()


    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    # Detect ball collistion with top and bottom wall
    if ball.ycor()>280 or ball.ycor()<-280:
        ball.bounce_y()

    # Detect ball collision with right paddle
    if ball.distance(r_paddle)<50 and ball.xcor()>320:
        ball.bounce_x()

    # Detect ball collision with left paddle
    if ball.distance(l_paddle)<50 and ball.xcor()<-320:
        ball.bounce_x()

    # Detect when right paddle misses
    if ball.xcor()>380:
        ball.reset_position()
        scoreboard.l_point()

    # Detect when right paddle misses
    if ball.xcor()<-380:
        ball.reset_position()
        scoreboard.r_point()


screen.exitonclick()