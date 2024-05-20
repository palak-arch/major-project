import random
from time import sleep
import pygame
import sys
import time

class CarRacing:
    def __init__(self):
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None

        self.initialize()

    def initialize(self):
        self.crashed = False

        self.carImg = pygame.image.load('\\car.png')
        self.car_x_coordinate = (self.display_width * 0.45)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49

        # enemy_car
        self.enemy_car = pygame.image.load('\\enemy_car_1.png')
        self.enemy_car_startx = random.randrange(310, 450)
        self.enemy_car_starty = -600
        self.enemy_car_speed = 5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        # Background
        self.bgImg = pygame.image.load("\\back_ground.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.score = 0

        # High score
        self.high_score = self.read_high_score()

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Dodge')
        self.run_car()

    def run_car(self):
        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.car_x_coordinate -= 50
                    if event.key == pygame.K_RIGHT:
                        self.car_x_coordinate += 50

            self.gameDisplay.fill(self.black)
            self.back_ground_road()

            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.randrange(310, 450)

            self.car(self.car_x_coordinate, self.car_y_coordinate)
            self.update_score()
            self.display_score()

            # Increase speed based on score
            if self.score % 100 == 0 and self.score != 0:
                self.enemy_car_speed += 0.5
                self.bg_speed += 0.5

            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if (self.car_x_coordinate > self.enemy_car_startx and 
                    self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width or 
                    self.car_x_coordinate + self.car_width > self.enemy_car_startx and 
                    self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width):
                    self.crashed = True
                    self.display_message("Game Over !!!")

            if self.car_x_coordinate < 310 or self.car_x_coordinate > 460:
                self.crashed = True
                self.display_message("Game Over !!!")

            pygame.display.update()
            self.clock.tick(60)

    def display_message(self, msg):
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        self.update_high_score()
        self.display_high_score()
        pygame.display.update()
        sleep(1)
        self.new_game_button()

    def new_game_button(self):
        button_font = pygame.font.SysFont("comicsansms", 36)
        text = button_font.render("New Game", True, (255, 255, 255))
        button_rect = pygame.Rect(300, 400, 200, 50)
        pygame.draw.rect(self.gameDisplay, (0, 128, 0), button_rect)
        self.gameDisplay.blit(text, (button_rect.x + 20, button_rect.y + 10))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        self.initialize()
                        self.racing_window()

    def back_ground_road(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def update_score(self):
        self.score += 1

    def display_score(self):
        font = pygame.font.SysFont("lucidaconsole", 20)
        text = font.render("Score : " + str(self.score), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

    def read_high_score(self):
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read().strip())
        except:
            return 0

    def write_high_score(self, high_score):
        with open("highscore.txt", "w") as file:
            file.write(str(high_score))

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.write_high_score(self.high_score)

    def display_high_score(self):
        font = pygame.font.SysFont("lucidaconsole", 20)
        text = font.render("High Score : " + str(self.high_score), True, self.white)
        self.gameDisplay.blit(text, (0, 30))

if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()
