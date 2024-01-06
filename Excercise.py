import pygame
pygame.init()

wnHt = 480
wnWdth = 500
bg = pygame.image.load('bg.jpg')
clock = pygame.time.Clock()
velocity = 5
projSpeed = 8
font = pygame.font.SysFont('comicsans', 25, True)
score = 0


class player(object):
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.isJump = False
        self.left = False
        self.right = False
        self.vel = velocity
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.health = 3
        self.isAlive = True

    def draw(self, wn):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                wn.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                wn.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                wn.blit(walkRight[0], (self.x, self.y))
            else :
                wn.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(wn,(0, 255, 255), self.hitbox, 2)

    def hit(self):
        if self.health >= 0:
            self.health -= 1
        else:
            self.isAlive = False
        font1 = pygame.font.SysFont('comicsans', 60, True)
        text1 = font1.render("-5", 1, (0, 0, 0))
        wn.blit(text1, ((250 - text1.get_width()), (240 - text1.get_height())))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = projSpeed * facing

    def draw(self, wn):
        pygame.draw.circle(wn, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRightE = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                  pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                  pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                  pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeftE = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                 pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                 pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                 pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    charE = pygame.image.load('standing.png')

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walkCount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.hitbox = (self.x + 17, self.y + 2, 32, 57)
        self.visible = True
        self.health = 10

    def draw(self, wn):
        self.move()
        if self.visible:
            if self.walkCount +1 >= 33:
                self.walkCount = 0
            if self.vel > 0:
                wn.blit(self.walkRightE[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                wn.blit(self.walkLeftE[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            self.hitbox = (self.x + 17, self.y + 2, 32, 57)

            pygame.draw.rect(wn, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 10, 50, 10))
            pygame.draw.rect(wn, (34, 139, 34), (self.hitbox[0], self.hitbox[1] - 10, 50 - (5 * (10 - self.health)), 10))


            #pygame.draw.rect(wn, (0, 255, 255), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1] :
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False





shootCount = 0
man = player(300, 420, 64, 64)
goblin = enemy(0, 425, 64, 64, 450)
bullets = []
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
char = pygame.image.load('standing.png')
wn = pygame.display.set_mode((wnWdth, wnHt))
pygame.display.set_caption("Exercise")
bulletSound = pygame.mixer.Sound('bullet_hit.wav')
hitSound = pygame.mixer.Sound('hit.wav')
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

def redrawGameWn():
    wn.blit(bg, (0, 0))
    text = font.render(f'Score: {score}', 1, (0, 0, 0))
    wn.blit(text, (200, 10))
    man.draw(wn)
    goblin.draw(wn)
    for bullet in bullets:
        bullet.draw(wn)
    pygame.display.update()


run = True

while run:
    clock.tick(27)
    redrawGameWn()

    if goblin.visible:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5
                man.x = 250
                goblin.x = 100

    if shootCount > 0:
        shootCount += 1
    if shootCount > 10:
        shootCount = 0
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            run = False
    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                hitSound.play()
                goblin.hit()
                if goblin.visible:
                    bullets.pop(bullets.index(bullet))
                    score += 10

        if bullet.x < 500 and bullet.x > 0 :
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_f] and shootCount == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 5, (0, 0, 0), facing ))
        shootCount += 1
        bulletSound.play()
    if keys[pygame.K_r] and not goblin.visible:
        goblin.health = 10
        goblin.visible = True
        man.isAlive = True

    if keys[pygame.K_a] and man.x > man.vel:
        man.x -= man.vel
        man.right = False
        man.left = True
        man.standing = False
    elif keys[pygame.K_d] and man.x < wnHt - man.vel - man.width:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
    if not man.isJump:
        if keys[pygame.K_SPACE]:
            man.isJump = True
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    while not man.isAlive:
        man.hit()
        if keys[pygame.K_r] and not goblin.visible:
            goblin.health = 10
            goblin.visible = True
            man.isAlive = True
            score = 0

pygame.quit()
