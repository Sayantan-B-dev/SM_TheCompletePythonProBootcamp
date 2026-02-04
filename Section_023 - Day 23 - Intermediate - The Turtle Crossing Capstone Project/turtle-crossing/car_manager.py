from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
LANES = [-230, -190, -150, -110, -70, -30, 10, 50, 90, 130, 170, 210]
MIN_GAP = 80
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10
FINISH_LINE_Y = 230


class CarManager(Turtle):
    def __init__(self):
        super().__init__()
        self.all_cars = []
        self.car_speed = 0.07
        self.hideturtle()
        self.create_road()
        self.draw_finish_line()
        self.create_lanes()

    def create_lanes(self):
        for _ in range(20):
            self.create_car()
            for car in self.all_cars:
                car.backward(random.randint(0, 600))

    def draw_finish_line(self):
        finish_line = Turtle()
        finish_line.hideturtle()
        finish_line.speed(0)
        finish_line.color("red")
        finish_line.pensize(2)
        finish_line.penup()
        finish_line.goto(-300, FINISH_LINE_Y)
        finish_line.pendown()
        finish_line.goto(300, FINISH_LINE_Y)
        finish_line.penup()
        finish_line.goto(0, FINISH_LINE_Y + 5)
        finish_line.write("Finish Line", align="center", font=("Courier", 16, "bold"))

    def create_car(self):
        if random.randint(1, 6) != 1:
            return

        lane = random.choice(LANES)

        for car in self.all_cars:
            if car.ycor() == lane and car.xcor() > 300 - MIN_GAP:
                return

        new_car = Turtle("square")
        new_car.color("white", random.choice(COLORS))
        new_car.pensize(2)
        new_car.penup()
        new_car.shapesize(stretch_wid=1, stretch_len=2)
        new_car.goto(random.randint(280, 300), lane)
        self.all_cars.append(new_car)


    
    def move_cars(self):
        for car in self.all_cars:
            car.setheading(180)
            car.forward(STARTING_MOVE_DISTANCE)

    def create_road(self):
        roadborder = Turtle()
        roadborder.color("white")
        roadborder.hideturtle()
        roadborder.speed(0)
        roadborder.penup()

        top = 230
        bottom = -250
        left = -300
        right = 300

        roadborder.goto(left, top)
        roadborder.pendown()
        roadborder.goto(right, top)
        roadborder.goto(right, bottom)
        roadborder.goto(left, bottom)
        roadborder.goto(left, top)

    def increase_speed(self):
        self.car_speed *= 0.9

    def reset(self):
        for car in self.all_cars:
            car.hideturtle()
        self.all_cars.clear()
        self.car_speed = 0.07
        self.create_lanes()
