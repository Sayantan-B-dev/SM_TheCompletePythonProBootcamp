import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
from input_handler import InputHandler


# COLLISION (AABB HITBOX)
def check_collision(car, player):
    # CAR hitbox (rectangle)
    CAR_WIDTH = 40
    CAR_HEIGHT = 20

    # PLAYER hitbox (biased upward for turtle head)
    PLAYER_WIDTH = 18
    PLAYER_HEIGHT = 28     # taller than visual body
    HEAD_OFFSET = 8        # pushes hitbox upward
    PADDING = 2

    # --- car bounds ---
    car_left = car.xcor() - CAR_WIDTH / 2
    car_right = car.xcor() + CAR_WIDTH / 2
    car_top = car.ycor() + CAR_HEIGHT / 2
    car_bottom = car.ycor() - CAR_HEIGHT / 2

    # --- player bounds (shifted upward) ---
    player_left = player.xcor() - PLAYER_WIDTH / 2
    player_right = player.xcor() + PLAYER_WIDTH / 2
    player_top = player.ycor() + PLAYER_HEIGHT / 2 + HEAD_OFFSET
    player_bottom = player.ycor() - PLAYER_HEIGHT / 2 + HEAD_OFFSET

    return (
        car_right > player_left + PADDING and
        car_left < player_right - PADDING and
        car_top > player_bottom + PADDING and
        car_bottom < player_top - PADDING
    )


# SCREEN SETUP
screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)
screen.bgcolor("black")


# GAME OBJECTS
player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()
input_handler = InputHandler(screen)


# GAME STATE
game_is_on = True
game_over = False


def restart_game():
    global game_is_on, game_over
    game_is_on = True
    game_over = False

    player.reset_position()
    car_manager.reset()
    scoreboard.reset_scoreboard()


# MAIN LOOP
while True:
    time.sleep(car_manager.car_speed)
    screen.update()

    # -------- GAME RUNNING --------
    if game_is_on:
        car_manager.create_car()
        car_manager.move_cars()

        # player input
        if input_handler.is_pressed("Up") or input_handler.is_pressed("w"):
            player.move()
        if input_handler.is_pressed("Left") or input_handler.is_pressed("a"):
            player.move_left()
        if input_handler.is_pressed("Right") or input_handler.is_pressed("d"):
            player.move_right()

        # collision detection (RECTANGLE BASED)
        for car in car_manager.all_cars:
            if check_collision(car, player):
                game_is_on = False
                game_over = True
                scoreboard.game_over()
                break

        # successful crossing
        if player.is_at_finish_line():
            player.reset_position()
            car_manager.increase_speed()
            scoreboard.increase_level()

    # -------- GAME OVER STATE --------
    else:
        if input_handler.is_pressed("r"):
            restart_game()
