import pygame as py   
import random as rand 

# initialize pygame
py.init()

# screen dimensions
screen_width = 500  # screen width
screen_height = 500  # screen height

# set up the screen display
screen = py.display.set_mode((screen_width, screen_height))

# define colors using rgb values
BLACK = (0, 0, 0)
GREEN = (14, 60, 21)
RED = (255, 0, 0)
BLUE = (50, 105, 5)

# fill the screen with black background
screen.fill(BLACK)


# cube class representing a basic game object (e.g., snake, food)
class Cube():
    def __init__(self, x, y, width, height, color=None, filename=None) -> None:
        self.rect = py.Rect(x, y, width, height)  # define the rectangle for the cube
        self.fill_color = color  # color to fill the cube
        self.img = filename  # image file for the cube
        if self.img:
            self.image = py.image.load(filename)  # load image if provided
    
    # method to draw the cube (either as a colored rectangle or an image)
    def draw(self):
        if self.fill_color:
            py.draw.rect(screen, self.fill_color, self.rect)  # draw a filled rectangle
        if self.img:
            screen.blit(self.image, (self.rect.x, self.rect.y))  # draw the image
    
    # method to randomly move the cube to a different position on the screen
    def rand_move(self):
        x_rand = rand.randint(0, 19) * 25  # random x position
        y_rand = rand.randint(0, 19) * 25  # random y position
        self.rect.x = x_rand
        self.rect.y = y_rand
    
    # collision detection with another cube (like the snake colliding with itself or the food)
    def colliderect(self, enm):
        return self.rect.colliderect(enm)

# starting position of the snake's head
start_x = 50
start_y = 50

# size of the snake cells
snake_cell = screen_width // 20

# initialize the snake's head
snake_head = Cube(start_x, start_y, snake_cell, snake_cell, BLUE)

# initialize food (it will use an image for the food)
food = Cube(100, 100, snake_cell, snake_cell, filename='food_2.png')  # food image import

# draw the snake's head
snake_head.draw()

# speed of the snake's movement
snake_speed = 25

# function to move the snake's body (each segment follows the previous one)
def body_move(body): 
    size = len(body)  # get the size of the snake's body
    for ind in range(size - 1, 0, -1):  # start from the last body segment
        body[ind].rect.x = body[ind - 1].rect.x  # move the segment to the position of the one before it
        body[ind].rect.y = body[ind - 1].rect.y  # move the segment to the position of the one before it

# function to add a new segment (tail) to the snake's body
def add_new_cell(body):
    last_cell = body[-1]  # get the last segment of the body
    new_cell = Cube(last_cell.rect.x, last_cell.rect.y, snake_cell, snake_cell, GREEN)  # create a new cube to add to the body
    body.append(new_cell)  # append the new segment to the body

# list representing the snake's body, starting with just the head
body = [snake_head]

# snake's movement direction flags (horizontal or vertical)
horizontal = True
vertical = False

# load background image for the screen
background = py.image.load('background.webp')

# initialize a counter for the game (can be used for scoring or tracking time)
counter = 0

# main game loop
running = True
while running:
    for ev in py.event.get():  # check for events (like key presses or window closure)
        if ev.type == py.QUIT:
            running = False  # quit the game if the window is closed
        if ev.type == py.KEYDOWN:  # check for key presses
            if ev.key == py.K_d and not horizontal:
                snake_speed = 25
                horizontal = True
                vertical = False  # move right if 'd' key is pressed
            elif ev.key == py.K_a and not horizontal:
                snake_speed = -25
                horizontal = True
                vertical = False  # move left if 'a' key is pressed
            elif ev.key == py.K_w and not vertical:
                snake_speed = -25
                horizontal = False
                vertical = True  # move up if 'w' key is pressed
            elif ev.key == py.K_s and not vertical:
                snake_speed = 25
                horizontal = False
                vertical = True  # move down if 's' key is pressed

    # draw the background image on the screen
    screen.blit(background, (0,0))
    
    # move the snake's body
    body_move(body)

    # update the snake's head position based on its direction
    if horizontal:
        snake_head.rect.x += snake_speed  # move horizontally
    elif vertical:
        snake_head.rect.y += snake_speed  # move vertically
    
    # draw the entire snake body (each segment)
    for cell in body:
        cell.draw()

    # draw the food on the screen
    food.draw()

    # draw the snake's head again on top (since we updated the position)
    snake_head.draw()

    # check if the snake eats the food (collides with it)
    if snake_head.rect.colliderect(food):
        food.rand_move()  # move the food to a new random position
        add_new_cell(body)  # add a new segment to the snake's body

    # check if the snake goes off the screen (wrap it around)
    if snake_head.rect.x >= 500:
        snake_head.rect.x = 0  # wrap around to the left side
    elif snake_head.rect.x < 0:
        snake_head.rect.x = 500  # wrap around to the right side
    
    if snake_head.rect.y >= 500:
        snake_head.rect.y = 0  # wrap around to the top side
    elif snake_head.rect.y < 0:
        snake_head.rect.y = 500  # wrap around to the bottom side
    
    # check if the snake collides with itself
    for i in body:  
        if body[0].rect.colliderect(i.rect) and body.index(i) > 1:  # ignore the first two segments (head and neck)
            running = False  # end the game if it collides with itself

    # update the display
    py.display.update()
    
    # control the game's frame rate
    py.time.Clock().tick(10)

# quit pygame when the game loop ends
py.quit()
