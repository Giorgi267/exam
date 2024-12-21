import pygame

pygame.init()#xelsawyoebis aqtivacia


screen = pygame.display.set_mode((500,500))#ekranis obieqti

clock = pygame.time.Clock()#saatis obieqti

#perebi
BACKGROUND = (200, 255, 255)#beqraundis feri

#######

screen.fill(BACKGROUND)#ekranshi feris chasxma
#klasebi
class Area():
    def __init__(self,x = -0, y = 0, width = 10, height = 10, color = None):
        self.rect = pygame.Rect(x,y,width,height)
        self.fill_color = BACKGROUND
        if color:
            self.fill_color = color

    def color(self, new_color):#feris shecvlis metodi
        self.fill_color = new_color

    def fill(self):               #obieqtis martkutxedis daxatva
        pygame.draw.rect(screen, self.fill_color, self.rect)
    
    def colliderect(self, enemy):  #განსაზღვრავს შეჯახებას ორ ობიექტს შორის
        return self.rect.colliderect(enemy)

class Picture(Area):
    
    def __init__(self, filename, x = 0, y = 0, width = 10, height = 10):
        Area.__init__(self, x=x, y=y, width=width, height=height)
        self.image =pygame.image.load(filename)

    def draw(self):
        screen.blit(self.image,(self.rect.x, self.rect.y))
    #obieqtebi
ball = Picture("ball.png", 160, 200, 50, 50)# burtis obieqti
platform = Picture("platform.png", 200, 330, 100, 30)

#mtris obieqti
start_x = 5
start_y = 5
count = 9
monsters = [] #mtris sia

for i in range(3):
    x = start_x + (27.5 * i)
    y = start_y + (55 * i)
    for j in range(count):
        new_monster = Picture("enemy.png", x, y, 50, 50)
        monsters.append(new_monster)
        x = x + 55
    count = count - 1 #sheamcire monstrebis raodenoba

#პლატფორმის ბერკეტები
move_right = False
move_left = False

#burtis sichqare

dx = 5
dy = 5


#tamashis cikli
game_running = True

while game_running:
    ball.fill()
    platform.fill()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False #tamashis gatishva
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

    if move_right:
        platform.rect.x += 5
    elif move_left:
        platform.rect.x -= 5            

    for monster in monsters:
        monster.draw()
        if monster.rect.colliderect(ball.rect):
            monsters.remove(monster)
            monster.fill()
            dy *= -1

    #burtis modzraobis logka
    ball.rect.x += dx
    ball.rect.y += dy
    #kedlis logika 

    if ball.rect.y < 0:
        dy *= -1

    if ball.rect.x < 0 or ball.rect.x > 450:
        dx *= -1

    #პლატპორმის შეჯახების ლოგიკა
    
    if ball.rect.colliderect(platform.rect):
        dy *= -1



    #obieqtis daxatva
    ball.draw()
    platform.draw()

    #wagebis logika

    if ball.rect.y > (platform.rect.y + 10):
        lose_font = pygame.font.SysFont('verdana', 50)
        lose_text = lose_font.render('You Lose!',True, (255,0,0) )
        screen.blit(lose_text,(150,200))
        game_running = False
    
    #mogebis logika
    if len(monsters) == 0:
        win_font = pygame.font.SysFont('verdana', 50)
        win_text = win_font.render('You Win!', True , (0,255,0))
        screen.blit(win_text, (150,200))
        game_running = False


    pygame.display.update()
    clock.tick(40) #tamashis fps