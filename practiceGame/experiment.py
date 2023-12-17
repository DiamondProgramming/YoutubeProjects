import pygame

pygame.init()

wnHt = 480
wnWdth = 500
x = 50
y = 400
height = 64
width = 64
vel = 5
bg = pygame.image.load('bg.jpg')
isJump = False
jumpCount = 10
left = False
right = False
walkCount = 0
clock = pygame.time.Clock()

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
char = pygame.image.load('standing.png')
wn = pygame.display.set_mode((wnWdth, wnHt))
pygame.display.set_caption("Exercise")


def redrawGameWn():
    global walkCount
    wn.blit(bg, (0, 0))
    if walkCount + 1 >= 27:
        walkCount = 0
    if left:
        wn.blit(walkLeft[walkCount//3], (x, y))
        walkCount = 0
    elif right:
        wn.blit(walkRight[walkCount//3], (x, y))
    else:
        wn.blit(char, (x, y))

    pygame.display.update()


run = True

while run:
    clock.tick(27)
    redrawGameWn()
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and x > vel:
        x -= vel
        right = False
        left = True
    elif keys[pygame.K_d] and x < wnHt - vel - width:
        x += vel
        right = True
        left = False
    else:
        right = False
        left = False
    if not isJump:
        if keys[pygame.K_SPACE]:
            isJump = True
            right = False
            left = False
            walkCount = 0
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10


pygame.quit()
