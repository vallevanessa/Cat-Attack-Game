import pygame
import random
import math
from pygame import mixer


# initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("cat escape")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Cat
playerImg = pygame.image.load('black-cat.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('mouse.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)


# claw
# Ready = you can't see the bullet on the screen
# Fire = the claw is moving currently
clawImg = pygame.image.load('claw.png')
clawX = 0
clawY = 480
clawX_change = 0
clawY_change = 0.5
claw_state = "ready"

# Score

score_value =  0
font = pygame.font.Font("freesansbold.ttf", 32)

testX = 10
testY = 10

# Game Over Font
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_claw(x, y):
    global claw_state
    claw_state = "fire"
    screen.blit(clawImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, clawX, clawY):
    distance = math.sqrt(math.pow(enemyX - clawX, 2) + math.pow(enemyY - clawY, 2))
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if claw_state is "ready":
                    claw_Sound = mixer.Sound("meow.wav")
                    claw_Sound.play()
                    clawX = playerX
                    fire_claw(clawX, clawY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    screen.fill((147, 112, 219))
    # player boundaries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movements
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], clawX, clawY)
        if collision:
            pew_Sound = mixer.Sound("shoot.wav")
            pew_Sound.play()
            clawY = 480
            claw_state = "ready"
            score_value += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # claw movement
    if clawY <= 0:
        clawY = 480
        claw_state = "ready"

    if claw_state is "fire":
        fire_claw(clawX, clawY)
        clawY -= clawY_change


    player(playerX, playerY)
    show_score(testX, testY)
    pygame.display.update()

