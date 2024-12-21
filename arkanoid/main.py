import pygame

pygame.init()  # Initialize pygame

screen = pygame.display.set_mode((500, 500))  # Screen setup
clock = pygame.time.Clock()  # FPS control

# Background color
BACKGROUND = (200, 255, 255)

# Screen fill
screen.fill(BACKGROUND)

# Area class for the objects
class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = BACKGROUND
        if color:
            self.fill_color = color

    def color(self, new_color):  # Change fill color
        self.fill_color = new_color

    def fill(self):  # Draw rectangle
        pygame.draw.rect(screen, self.fill_color, self.rect)

    def colliderect(self, enemy):  # Check for collision
        return self.rect.colliderect(enemy)

class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        super().__init__(x, y, width, height)
        self.image = pygame.image.load(filename)

    def draw(self):  # Draw image
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Game objects
ball = Picture("arkanoid/ball.png", 160, 200, 50, 50)
platform = Picture("arkanoid/platform.png", 200, 330, 100, 30)

# Monsters creation
start_x = 5
start_y = 5
count = 9
monsters = []

for i in range(3):
    x = start_x + (27.5 * i)
    y = start_y + (55 * i)
    for j in range(count):
        new_monster = Picture("arkanoid/enemy.png", x, y, 50, 50)
        monsters.append(new_monster)
        x = x + 55
    count = count - 1  # Adjust the number of monsters per row

# Platform movement variables
move_right = False
move_left = False

# Ball movement speed
dx = 5
dy = 5

# Game loop
game_running = True

while game_running:
    screen.fill(BACKGROUND)  # Clear screen

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                move_right = True
            elif event.key == pygame.K_a:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            elif event.key == pygame.K_d:
                move_right = False

    # Platform movement
    if move_right and platform.rect.x < 400:  # Prevent platform from going off-screen
        platform.rect.x += 5
    elif move_left and platform.rect.x > 0:  # Prevent platform from going off-screen
        platform.rect.x -= 5

    # Ball movement
    ball.rect.x += dx
    ball.rect.y += dy

    # Ball collision with walls
    if ball.rect.y < 0:
        dy *= -1  # Bounce on top wall

    if ball.rect.x < 0 or ball.rect.x > 450:  # Ball bounce on side walls
        dx *= -1

    # Ball and platform collision
    if ball.rect.colliderect(platform.rect):
        dy *= -1  # Bounce when hitting platform

    # Ball and monster collision
    for monster in monsters[:]:
        if monster.rect.colliderect(ball.rect):
            monsters.remove(monster)
            dy *= -1  # Bounce the ball
            break  # Prevent multiple removals in the same frame

    # Lose condition
    if ball.rect.y > (platform.rect.y + 10):
        lose_font = pygame.font.SysFont('verdana', 50)
        lose_text = lose_font.render('You Lose!', True, (255, 0, 0))
        screen.blit(lose_text, (150, 200))
        game_running = False

    # Win condition
    if len(monsters) == 0:
        win_font = pygame.font.SysFont('verdana', 50)
        win_text = win_font.render('You Win!', True, (0, 255, 0))
        screen.blit(win_text, (150, 200))
        game_running = False

    # Draw game objects
    ball.draw()
    platform.draw()
    for monster in monsters:
        monster.draw()

    pygame.display.update()  # Update screen
    clock.tick(40)  # Control frame rate
