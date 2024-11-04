import os
import random
import time
import pygame


# Import the turtle graphics module for game visuals
import turtle

# Initialize pygame for sound management
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound

# Play background music in a loop
pygame.mixer.music.load("space.mp3")  # Load the music file
pygame.mixer.music.play(-1)  # -1 ensures the music loops indefinitely

# Configure the turtle window
turtle.speed(0)              # Max animation speed
turtle.bgcolor("black")      # Set background color to black
turtle.title("Space Sniper") # Title of the game window
turtle.bgpic("starfield.gif") # Load and display background image
turtle.ht()                  # Hide the default turtle cursor
turtle.setundobuffer(1)      # Set undo buffer size to 1 (optimize memory usage)
turtle.tracer(0)             # Disable automatic screen updates (manual updates for smoother animation)

# Define the base class for all game sprites
class Sprite(turtle.Turtle):
    def __init__(self, shape_type, color, initial_x, initial_y):
        super().__init__(shape=shape_type)  # Initialize as a turtle object
        self.speed(0)         # Max speed (instant movement)
        self.penup()           # Disable drawing when moving
        self.color(color)      # Set the color of the sprite
        self.goto(initial_x, initial_y)  # Place sprite at the starting position
        self.speed = 1         # Default movement speed

    def move(self):
        self.fd(self.speed)  # Move sprite forward based on speed

        # Boundary detection to keep sprite within the game area
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)  # Turn right upon hitting a boundary
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def is_collision(self, other):
        # Check for collision with another sprite (within 20 units distance)
        if (self.xcor() >= other.xcor() - 20) and \
           (self.xcor() <= other.xcor() + 20) and \
           (self.ycor() >= other.ycor() - 20) and \
           (self.ycor() <= other.ycor() + 20):
            return True
        return False

# Define the Player class (inherits from Sprite)
class Player(Sprite):
    def __init__(self, shape_type, color, initial_x, initial_y):
        super().__init__(shape_type, color, initial_x, initial_y)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1)  # Adjust shape size
        self.speed = 4  # Set initial speed
        self.lives = 3  # Player starts with 3 lives

    # Define player controls
    def turn_left(self):
        self.lt(45)  # Rotate left by 45 degrees

    def turn_right(self):
        self.rt(45)  # Rotate right by 45 degrees

    def accelerate(self):
        self.speed += 1  # Increase speed

    def decelerate(self):
        self.speed -= 1  # Decrease speed

# Define Enemy class (inherits from Sprite)
class Enemy(Sprite):
    def __init__(self, shape_type, color, initial_x, initial_y):
        super().__init__(shape_type, color, initial_x, initial_y)
        self.speed = 6  # Set higher speed for enemy_fleet
        self.setheading(random.randint(0, 360))  # Random movement direction

# Define Missile class (inherits from Sprite)
class Missile(Sprite):
    def __init__(self, shape_type, color, initial_x, initial_y):
        super().__init__(shape_type, color, initial_x, initial_y)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4)  # Adjust missile size
        self.speed = 20  # Fast speed for missiles
        self.status = "ready"  # Track if missile is ready to fire
        self.goto(-1000, 1000)  # Hide missile off-screen initially

    def fire(self):
        if self.status == "ready":
            # Fire the missile from the player's position
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())  # Follow player's direction
            self.status = "firing"

    def move(self):
        if self.status == "firing":
            self.fd(self.speed)  # Move forward if fired

            # Reset if it goes out of bounds
            if self.xcor() < -290 or self.xcor() > 290 or \
               self.ycor() < -290 or self.ycor() > 290:
                self.goto(-1000, 1000)
                self.status = "ready"

# Define Ally class (inherits from Sprite)
class Ally(Sprite):
    def __init__(self, shape_type, color, initial_x, initial_y):
        super().__init__(shape_type, color, initial_x, initial_y)
        self.speed = 8  # Faster than player
        self.setheading(random.randint(0, 360))  # Random direction

# Define Particle class (used for explosion effects)
class Particle(Sprite):
    def __init__(self, shape_type, color, initial_x, initial_y):
        super().__init__(shape_type, color, initial_x, initial_y)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1)  # Small size
        self.goto(-1000, -1000)  # Hide off-screen initially
        self.frame = 0  # Frame counter for explosion effect

    def explode(self, initial_x, initial_y):
        self.goto(initial_x, initial_y)  # Start explosion at given position
        self.setheading(random.randint(0, 360))  # Random explosion direction
        self.frame = 1  # Start the explosion animation

    def move(self):
        if self.frame > 0:
            self.fd(10)  # Move outward
            self.frame += 1  # Increment frame

        if self.frame > 15:  # End explosion after 15 frames
            self.frame = 0
            self.goto(-1000, -1000)  # Hide off-screen

# Define Game class to manage game state and logic
class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()  # For displaying game info
        self.lives = 3

    def draw_border(self):
        # Draw the game boundary
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()

    def show_status(self):
        # Display the current score
        self.pen.undo()  # Clear previous message
        msg = f"Score: {self.score}"
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial", 16, "normal"))

# Create game object and initialize
game = Game()
game.draw_border()  # Draw the game border
game.show_status()  # Show the initial score

# Create player, enemy_fleet, ally_group, and particles
player = Player("triangle", "white", 0, 0)
missile = Missile("triangle", "yellow", 0, 0)
enemy_fleet = [Enemy("circle", "red", -100, 0) for _ in range(6)]
ally_group = [Ally("square", "blue", 100, 0) for _ in range(6)]
particles = [Particle("circle", "orange", 0, 0) for _ in range(20)]

# Set up keyboard controls
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.listen()  # Listen for key presses

# Main game loop
while True:
    turtle.update()  # Update the screen
    time.sleep(0.02)  # Control game speed

    player.move()
    missile.move()

    for enemy in enemy_fleet:
        enemy.move()
        if player.is_collision(enemy):
            os.system("afplay explosion.mp3&")  # Play explosion sound
            enemy.goto(random.randint(-250, 250), random.randint(-250, 250))
            game.score -= 100  # Decrease score
            game.show_status()

        if missile.is_collision(enemy):
            os.system("afplay explosion.mp3&")
            enemy.goto(random.randint(-250, 250), random.randint(-250, 250))
            missile.status = "ready"
            game.score += 100  # Increase score
            game.show_status()
            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())

    for ally in ally_group:
        ally.move()
        if missile.is_collision(ally):
            os.system("afplay explosion.mp3&")
            ally.goto(random.randint(-250, 250), random.randint(-250, 250))
            missile.status = "ready"
            game.score -= 50  # Decrease score
            game.show_status()

    for particle in particles:
        particle.move()

delay = input("Please press enter to finish. >")
