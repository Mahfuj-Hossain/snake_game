from turtle import Turtle, Screen
import random

score = 0
high_score = 0

# Functions to move the snake
def move():
    global score
    global high_score

    # Move the head
    snake[0].forward(20)

    # Check for collisions with food
    if snake[0].distance(food) < 15:
        create_food()
        extend_snake()
        update_score()

    # Check for collisions with walls or own tail
    if (
        snake[0].xcor() > 290
        or snake[0].xcor() < -290
        or snake[0].ycor() > 290
        or snake[0].ycor() < -290
        or check_collision()
    ):
        game_over()

    # Move the rest of the body
    for i in range(len(snake) - 1, 0, -1):
        x_cor = snake[i - 1].xcor()
        y_cor = snake[i - 1].ycor()
        snake[i].goto(x_cor, y_cor)

    screen.update()
    screen.ontimer(move, 100)  # Update every 100 milliseconds

def extend_snake():
    new_segment = Turtle('square')
    new_segment.color('white')
    new_segment.penup()
    snake.append(new_segment)

def create_food():
    food.goto(random.randint(-290, 290), random.randint(-290, 290))

def update_score():
    global score
    global high_score

    score += 10

    # Check if high_score is initialized
    if high_score >= 0 and score > high_score:
        high_score = score
        update_high_score()

    update_score_display()

def update_score_display():
    score_display.clear()
    score_display.write(f"Score: {score} High Score: {high_score}", align="center", font=("Courier", 18, "normal"))

def update_high_score():
    with open("highscore.txt", "w") as file:
        file.write(str(high_score))

def check_collision():
    # Check for collisions with walls
    if (
        snake[0].xcor() > 290
        or snake[0].xcor() < -290
        or snake[0].ycor() > 290
        or snake[0].ycor() < -290
    ):
        return True

    # Check for collisions with own tail
    for segment in snake[1:]:
        if snake[0].distance(segment) < 10:
            return True

    return False

def game_over():
    global score

    # Display game over message and final score
    user_input = screen.textinput("Game Over", f"Your Score: {score}\nGame Over. Play again? (yes/no)").lower()

    if user_input == "yes":
        reset_game()
    else:
        exit_game()

def reset_game():
    global score
    score = 0
    update_score_display()
    reset_snake()
    create_food()
    bind_keys()  # Re-bind keys after restarting the game

def reset_snake():
    for segment in snake:
        segment.goto(1000, 1000)  # Move segments off-screen
    snake.clear()
    new_snake()

def new_snake():
    global snake
    snake = [Turtle('square') for _ in range(3)]  # Initial snake with 3 segments
    for segment in snake:
        segment.color('white')
        segment.penup()
    snake[0].goto(0, 0)  # Initial position

def exit_game():
    screen.bye()  # Close the turtle graphics window

def bind_keys():
    # Re-bind arrow keys
    screen.listen()
    screen.onkey(move_up, 'Up')
    screen.onkey(move_down, 'Down')
    screen.onkey(move_left, 'Left')
    screen.onkey(move_right, 'Right')

# Set up the screen and snake
screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

snake = []
new_snake()

food = Turtle('circle')
food.color('red')
food.penup()

# Set up key bindings
def move_up():
    if snake[0].heading() != 270:
        snake[0].setheading(90)

def move_down():
    if snake[0].heading() != 90:
        snake[0].setheading(270)

def move_left():
    if snake[0].heading() != 0:
        snake[0].setheading(180)

def move_right():
    if snake[0].heading() != 180:
        snake[0].setheading(0)

bind_keys()  # Initial binding of keys

# Set up score display
score_display = Turtle()
score_display.hideturtle()
score_display.penup()
score_display.color('white')
score_display.goto(0, 260)
update_score_display()

# Load high score from file
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

# Start moving the snake
move()

# Create initial food
create_food()

# Set the background color
screen.bgcolor('black')

# Close the window when clicked
screen.exitonclick()
