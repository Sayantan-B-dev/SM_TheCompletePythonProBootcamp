from turtle import Screen
import time
from snake import Snake
from food import Food
from scoreboard import Scoreboard

# SCREEN SETUP
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)

# GAME OBJECTS
snake = Snake()
food = Food()
scoreboard = Scoreboard()

# GAME STATE
game_is_on = True

# CONTROLS
screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

def restart_game():
    global game_is_on
    scoreboard.reset()
    snake.reset()
    game_is_on = True

screen.onkey(restart_game, "r")

# GAME LOOP
while True:
    screen.update()
    time.sleep(0.1)

    if game_is_on:
        snake.move()

        # FOOD COLLISION
        if snake.head.distance(food) < 15:
            food.refresh()
            snake.extend()
            scoreboard.increase_score()

        # WALL COLLISION
        if (
            snake.head.xcor() > 280 or snake.head.xcor() < -280 or
            snake.head.ycor() > 280 or snake.head.ycor() < -280
        ):
            scoreboard.game_over()
            game_is_on = False

        # TAIL COLLISION
        for segment in snake.segments[1:]:
            if snake.head.distance(segment) < 10:
                scoreboard.game_over()
                game_is_on = False

screen.exitonclick()
