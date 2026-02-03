import turtle

# Setup
screen = turtle.Screen()
screen.bgcolor("lightblue")
screen.title("Weather Data")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

# Weather data (temperature for 7 days)
temperatures = [72, 75, 68, 80, 82, 78, 74]
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
weather = ["☀️", "⛅", "🌧️", "☀️", "☀️", "⛅", "🌤️"]

# Draw temperature line
t.penup()
t.goto(-300, 0)
t.pendown()
t.color("red")
t.width(3)

for i, temp in enumerate(temperatures):
    x = -300 + i * 100
    y = (temp - 70) * 10  # Scale for visualization
    
    t.goto(x, y)
    
    # Draw temperature point
    t.dot(15)
    
    # Add temperature label
    t.penup()
    t.goto(x, y + 20)
    t.color("black")
    t.write(f"{temp}°F", align="center", font=("Arial", 12, "bold"))
    
    # Add day label
    t.goto(x, -100)
    t.write(days[i], align="center", font=("Arial", 14))
    
    # Add weather icon
    t.goto(x, -70)
    t.write(weather[i], align="center", font=("Arial", 24))
    
    t.color("red")
    t.penup()
    t.goto(x, y)
    t.pendown()

# Add title
t.penup()
t.goto(0, 200)
t.color("navy")
t.write("Weekly Temperature Forecast", align="center", font=("Arial", 18, "bold"))

# Draw horizontal line at 70°F
t.penup()
t.goto(-350, 0)
t.pendown()
t.color("gray")
t.width(1)
t.goto(350, 0)
t.write("70°F", font=("Arial", 10))

screen.mainloop()