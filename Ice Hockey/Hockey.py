#IMPORTS
import pygame
import sys
import random
import time
import os

#INITIALIZING PYGAME
pygame.init()
clock = pygame.time.Clock()
ai = False
ai1 = False
playerscore = 0
opponentscore = 0
bounce = pygame.mixer.Sound('bounce.wav')
effect = True


def restart():
    global ballx, bally
    ballx *= random.choice((-1, 1))
    bally *= random.choice((-1, 1))
    ball.center = (wnWdth / 2, wnHt / 2)
    time.sleep(0.5)


def ball_animation():
    global ballx, bally, opponentscore, playerscore
    ball.x += ballx
    ball.y += bally
    if ball.top <= 0 or ball.bottom >= wnHt:
        bally *= -1
    if ball.left <= 0:
        restart()
        playerscore += 1
    if ball.right >= wnWdth:
        restart()
        opponentscore += 1
    if ball.colliderect(player) or ball.colliderect(opponent):
        ballx *= -1
        if effect:
            bounce.play()

def playerreset():
    player.y += playerspeed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= wnHt:
        player.bottom = wnHt


def opponentreset():
    opponent.y += opponentspeed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= wnHt:
        opponent.bottom = wnHt

def playerai():
    if ai1:
        if player.top <= ball.y:
            player.top += playeraispeed
        if player.bottom >= ball.y:
            player.bottom -= playeraispeed

def opponentai():
    if ai:
        if opponent.top <= ball.y:
            opponent.top += opponentaispeed
        if opponent.bottom >= ball.y:
            opponent.bottom -= opponentaispeed


def scoredraw():
    font = pygame.font.SysFont("comicsans", 50, True)
    text = font.render(str(opponentscore), 1, (light_grey))
    wn.blit(text, (wnWdth/2 - (text.get_width()) - 10, (wnHt/2)))
    font1 = pygame.font.SysFont("comicsans", 50, True)
    text1 = font1.render(str(playerscore), 1, (light_grey))
    wn.blit(text1, (wnWdth / 2 + (text1.get_width()) - 10, (wnHt / 2)))
#SETTING UP THE WINDOW/SCREEN

wnHt = 960
wnWdth = 1280
wn = pygame.display.set_mode((wnWdth, wnHt))
pygame.display.set_caption("Ping Pong")
#DEFINE PLAYERS
ball = pygame.Rect((wnWdth/2 - 15), (wnHt/2 - 15), 30, 30)
player = pygame.Rect((wnWdth - 20), (wnHt/2 - 70), 10, 140)
opponent = pygame.Rect(10, wnHt/2 - 70, 10, 140)
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)
bally = 7
ballx = 7
playerspeed = 0
opponentspeed = 0
opponentaispeed = 7
playeraispeed = 7


#MAIN GAME LOOP
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if not ai1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    playerspeed -= 7
                if event.key == pygame.K_DOWN:
                    playerspeed += 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    playerspeed += 7
                if event.key == pygame.K_DOWN:
                    playerspeed -= 7
        #OPPONENT CONTROLS
        keys = pygame.key.get_pressed()
        if keys[pygame.K_g]:
            if ai:
                ai = False
            else:
                ai = True
        if keys[pygame.K_h]:
            if ai1:
                ai1 = False
            else:
                ai1 = True
        if not ai:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    opponentspeed -= 7
                if event.key == pygame.K_s:
                    opponentspeed += 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    opponentspeed += 7
                if event.key == pygame.K_s:
                    opponentspeed -= 7
        if keys[pygame.K_r]:
            opponentscore = 0
            playerscore = 0
            restart()
        if keys[pygame.K_e]:
            if effect:
                effect = False
            else:
                effect = True

    opponentreset()
    playerai()
    opponentai()
    playerreset()
    ball_animation()
    wn.fill(bg_color)
    pygame.draw.rect(wn, light_grey, player)
    pygame.draw.rect(wn, light_grey, opponent)
    pygame.draw.ellipse(wn, light_grey, ball)
    pygame.draw.aaline(wn, light_grey, (wnWdth/2, 0), (wnWdth/2, wnHt))
    scoredraw()
    pygame.display.flip()
    clock.tick(60)

