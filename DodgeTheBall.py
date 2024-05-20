import pygame
import sys
import random
from math import *

pygame.init()

width = 400
height = 500
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dodge The Ball!")
clock = pygame.time.Clock()

background = (51, 51, 51)
playerColor = (249, 231, 159)

red = (203, 67, 53)
yellow = (241, 196, 15)
blue = (46, 134, 193)
green = (34, 153, 84)
purple = (136, 78, 160)
orange = (214, 137, 16)

colors = [red, yellow, blue, green, purple, orange]

score = 0
high_score = 0  # New variable to store high score


class Ball:
    def __init__(self, radius, speed):
        self.x = 0
        self.y = 0
        self.r = radius
        self.color = 0
        self.speed = speed
        self.angle = 0
    
    def createBall(self):
        self.x = width/2 - self.r
        self.y = height/2 - self.r
        self.color = random.choice(colors)
        self.angle = random.randint(-180, 180)
    
    def move(self):
        self.x += self.speed * cos(radians(self.angle))
        self.y += self.speed * sin(radians(self.angle))

        if self.x < self.r or self.x + self.r > width:
            self.angle = 180 - self.angle
        if self.y < self.r or self.y + self.r > height:
            self.angle *= -1

    def draw(self):
        pygame.draw.ellipse(display, self.color, (self.x - self.r, self.y - self.r, self.r*2, self.r*2))

    def collision(self, radius):
        pos = pygame.mouse.get_pos()

        dist = ((pos[0] - self.x)**2 + (pos[1] - self.y)**2)**0.5

        if dist <= self.r + radius:
            gameOver()

class Target:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 20
        self.h = self.w

    def generateNewCoord(self):
        self.x = random.randint(self.w, width - self.w)
        self.y = random.randint(self.h, height - self.h)

    def draw(self):
        color = random.choice(colors)

        pygame.draw.rect(display, color, (self.x, self.y, self.w, self.h))

class Button:
    def __init__(self, x, y, w, h, text, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, display):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(display, self.hover_color, self.rect)
            if mouse_click[0] == 1 and self.action is not None:
                self.action()
        else:
            pygame.draw.rect(display, self.color, self.rect)
        
        font = pygame.font.SysFont("Agency FB", 30)
        text_surf = font.render(self.text, True, (230, 230, 230))
        text_rect = text_surf.get_rect(center=self.rect.center)
        display.blit(text_surf, text_rect)


def readHighScore():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read().strip())
    except:
        return 0

def writeHighScore(high_score):
    with open("highscore.txt", "w") as file:
        file.write(str(high_score))


def gameOver():
    global high_score  # Reference the global high score variable
    if score > high_score:
        high_score = score  # Update high score if the current score is higher
        writeHighScore(high_score)  # Save the new high score to the file
    
    new_game_button = Button(width//2 - 50, height//2 + 50, 100, 50, "New Game", (100, 100, 100), (150, 150, 150), gameLoop)
    
    loop = True
    font = pygame.font.SysFont("Agency FB", 100)
    text = font.render("Game Over!", True, (230, 230, 230))
    
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    gameLoop()

        display.fill(background)
        display.blit(text, (20, height/2 - 100))
        displayScore()
        
        new_game_button.draw(display)
        
        pygame.display.update()
        clock.tick()


def checkCollision(target, d, objTarget):
    pos = pygame.mouse.get_pos()
    dist = ((pos[0] - target[0] - objTarget.w)**2 + (pos[1] - target[1]  - objTarget.h)**2)**0.5

    if dist <= d + objTarget.w:
        return True
    return False


def drawPlayerPointer(pos, r):
    pygame.draw.ellipse(display, playerColor, (pos[0] - r, pos[1] - r, 2*r, 2*r))


def close():
    pygame.quit()
    sys.exit()

def displayScore():
    font = pygame.font.SysFont("Forte", 30)
    scoreText = font.render("Score: " + str(score), True, (230, 230, 230))
    highScoreText = font.render("High Score: " + str(high_score), True, (230, 230, 230))
    display.blit(scoreText, (10, 10))
    display.blit(highScoreText, (10, 40))  # Display high score below the current score


def gameLoop():
    global score
    global high_score

    score = 0
    high_score = readHighScore()  # Initialize the high score from the file
    
    loop = True

    pRadius = 10

    balls = []

    for i in range(1):
        newBall = Ball(pRadius + 2, 5)
        newBall.createBall()
        balls.append(newBall)

    target = Target()
    target.generateNewCoord()
    
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    gameLoop()

        display.fill(background)

        for i in range(len(balls)):
            balls[i].move()
            
        for i in range(len(balls)):
            balls[i].draw()
            
        for i in range(len(balls)):
            balls[i].collision(pRadius)

        playerPos = pygame.mouse.get_pos()
        drawPlayerPointer((playerPos[0], playerPos[1]), pRadius)

        collide = checkCollision((target.x, target.y), pRadius, target)
        
        if collide:
            score += 1
            target.generateNewCoord()
        elif score == 2 and len(balls) == 1:
            newBall = Ball(pRadius + 2, 5)
            newBall.createBall()
            balls.append(newBall)
            target.generateNewCoord()
        elif score == 5 and len(balls) == 2:
            newBall = Ball(pRadius + 2, 6)
            newBall.createBall()
            balls.append(newBall)
            target.generateNewCoord()
        elif score == 10 and len(balls) == 3:
            newBall = Ball(pRadius + 2, 7)
            newBall.createBall()
            balls.append(newBall)
            target.generateNewCoord()
        elif score == 15 and len(balls) == 4:
            newBall = Ball(pRadius + 2, 8)
            newBall.createBall()
            balls.append(newBall)
            target.generateNewCoord()
        elif score == 20 and len(balls) == 5:
            newBall = Ball(pRadius + 2, 9)
            newBall.createBall()
            balls.append(newBall)
            target.generateNewCoord()

        target.draw()
        displayScore()
        
        pygame.display.update()
        clock.tick(60)

gameLoop()
