import pygame

pygame.init()
win = pygame.display.set_mode((852, 480))
window_width = 852

pygame.display.set_caption("MyGame!")

walk_right = [pygame.image.load('assets/R1.png'), pygame.image.load('assets/R2.png'), pygame.image.load('assets/R3.png'), pygame.image.load('assets/R4.png'), pygame.image.load('assets/R5.png'), pygame.image.load('assets/R6.png'), pygame.image.load('assets/R7.png'), pygame.image.load('assets/R8.png'), pygame.image.load('assets/R9.png')]
walk_left = [pygame.image.load('assets/L1.png'), pygame.image.load('assets/L2.png'), pygame.image.load('assets/L3.png'), pygame.image.load('assets/L4.png'), pygame.image.load('assets/L5.png'), pygame.image.load('assets/L6.png'), pygame.image.load('assets/L7.png'), pygame.image.load('assets/L8.png'), pygame.image.load('assets/L9.png')]
bg = pygame.image.load('assets/bg.jpg')
bullet_sound = pygame.mixer.Sound('sounds/bullet.wav')
hit_sound = pygame.mixer.Sound('sounds/hit.wav')
music = pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.play(-1)
score = 0

clock = pygame.time.Clock()
class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.jump_count = 9
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.hitbox = (self.x + 19, self.y + 13, 25, 50)
    def draw(self, win):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0
        if not self.standing:
            if self.left:
                win.blit(walk_left[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
            elif self.right:
                win.blit(walk_right[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.left:
                win.blit(walk_left[0], (self.x, self.y))
            else:
                win.blit(walk_right[0], (self.x, self.y))
        self.hitbox = (self.x + 19, self.y + 13, 25, 50)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def hit(self):
        self.is_jump = False
        self.jump_count = 9
        self.x = 50
        self.y = 400
        self.walk_count = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render("-5", 1, (255, 0, 0))
        win.blit(text, (window_width /2 - text.get_width(), 220))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()

class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * self.facing
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Enemy(object):
    walk_right = [pygame.image.load('assets/R1E.png'), pygame.image.load('assets/R2E.png'), pygame.image.load('assets/R3E.png'), pygame.image.load('assets/R4E.png'), pygame.image.load('assets/R5E.png'), pygame.image.load('assets/R6E.png'), pygame.image.load('assets/R7E.png'), pygame.image.load('assets/R8E.png'), pygame.image.load('assets/R9E.png'), pygame.image.load('assets/R10E.png'), pygame.image.load('assets/R11E.png')]
    walk_left = [pygame.image.load('assets/L1E.png'), pygame.image.load('assets/L2E.png'), pygame.image.load('assets/L3E.png'), pygame.image.load('assets/L4E.png'), pygame.image.load('assets/L5E.png'), pygame.image.load('assets/L6E.png'), pygame.image.load('assets/L7E.png'), pygame.image.load('assets/L8E.png'), pygame.image.load('assets/L9E.png'), pygame.image.load('assets/L10E.png'), pygame.image.load('assets/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walk_count = 0
        self.vel = 3
        self.hitbox = (self.x + 18, self.y + 3, 32, 54)
        self.health = 9
        self.visible = True
    def draw(self, win):
        self.move()
        if self.visible:
            if self.walk_count + 1 >= 33:
                self.walk_count = 0
            if self.vel > 0:
                win.blit(self.walk_right[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
            else:
                win.blit(self.walk_left[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 18, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 18, 5*(self.health+1), 10))
            self.hitbox = (self.x + 18, self.y + 3, 32, 54)
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                # self.x += self.vel
                self.walk_count = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                # self.x += self.vel
                self.walk_count = 0
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

def redraw_window():
    win.blit(bg, (0, 0))
    text = font.render("Score: " + str(score), 1, (0, 0, 0))
    win.blit(text, (0.84*window_width, 16))
    gameplay.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    goblin.draw(win)
    pygame.display.update()

# mainloop
font = pygame.font.SysFont('comicsans', 30, True)
gameplay = Player(50, 400, 64, 64)
goblin = Enemy(100, 404, 64, 64, 400)
shoot_thread = 0
bullets = []
run = True
while run:
    clock.tick(27)

    if goblin.visible == True:
        if gameplay.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and gameplay.hitbox[1] + gameplay.hitbox[3] > goblin.hitbox[1]:
            if gameplay.hitbox[0] + gameplay.hitbox[2] > goblin.hitbox[0] and gameplay.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                gameplay.hit()
                score -= 5

    if shoot_thread > 0:
        shoot_thread += 1
    if shoot_thread > 3:
        shoot_thread = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if goblin.visible == True:
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    hit_sound.play()
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
        if bullet.x < window_width and bullet.x > 0:
            bullet.x += bullet.vel
        else: bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shoot_thread == 0:
        bullet_sound.play()
        facing = -1 if gameplay.left else 1
        if len(bullets) < 5:
            bullets.append(Projectile(round(gameplay.x + gameplay.width //2), round(gameplay.y + gameplay.height //2), 6, (0,0,0), facing))
        shoot_thread = 1

    if keys[pygame.K_LEFT]:
        if 0 < gameplay.x - gameplay.vel:
            gameplay.x -= gameplay.vel
            gameplay.left = True
            gameplay.right = False
            gameplay.standing = False
    elif keys[pygame.K_RIGHT]:
        if gameplay.x + gameplay.width < window_width - gameplay.vel:
            gameplay.x += gameplay.vel
            gameplay.left = False
            gameplay.right = True
            gameplay.standing = False
    else:
        gameplay.standing = True
        gameplay.walk_count = 0

    if not gameplay.is_jump:
        if keys[pygame.K_UP]:
            gameplay.is_jump = True
            gameplay.left = False
            gameplay.right = False
            gameplay.walk_count = 0

    else:
        if gameplay.jump_count >= -9:
            neg = 1
            if gameplay.jump_count < 0:
                neg = -1
            gameplay.y -=  (gameplay.jump_count**2) * 0.5 * neg
            gameplay.jump_count -= 1
        else:
            gameplay.is_jump = False
            gameplay.jump_count = 9

    redraw_window()

pygame.quit()
