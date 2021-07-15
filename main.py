import pygame
import random
import os, sys
import time
import math
from pygame.math import Vector2

# --------- Configurations --------- #

pygame.init()
pygame.display.set_caption("Jake's Reimagined Google Snake Game")
cellSize,cellNumber = 40,20
WIN = pygame.display.set_mode((cellNumber*cellSize,cellNumber*cellSize))

apple = pygame.image.load('Graphics/apple.png')

head_left = pygame.image.load('Graphics/head_left.png')
head_right = pygame.image.load('Graphics/head_right.png')
head_up = pygame.image.load('Graphics/head_up.png')
head_down = pygame.image.load('Graphics/head_down.png')

tail_left = pygame.image.load('Graphics/tail_left.png')
tail_right = pygame.image.load('Graphics/tail_right.png')
tail_up = pygame.image.load('Graphics/tail_up.png')
tail_down = pygame.image.load('Graphics/tail_down.png')

body_tl = pygame.image.load('Graphics/body_topleft.png')
body_tr = pygame.image.load('Graphics/body_topright.png')
body_bl = pygame.image.load('Graphics/body_bottomleft.png')
body_br = pygame.image.load('Graphics/body_bottomright.png')

body_horz = pygame.image.load('Graphics/body_horizontal.png')
body_vert = pygame.image.load('Graphics/body_vertical.png')





programIcon = pygame.image.load('snakeIcon.png')
pygame.display.set_icon(programIcon)

class Snake():
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False
        self.head = head_right
        self.tail = tail_right
        self.body1 = body_horz



    def chooseHead(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = head_left
        if head_relation == Vector2(0, 1):
            self.head = head_up
        if head_relation == Vector2(-1, 0):
            self.head = head_right
        if head_relation == Vector2(0, -1):
            self.head = head_down

    def chooseTail(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0):
            self.tail = tail_left
        if tail_relation == Vector2(0, 1):
            self.tail = tail_up
        if tail_relation == Vector2(-1, 0):
            self.tail = tail_right
        if tail_relation == Vector2(0, -1):
            self.tail = tail_down


    def drawSnake(self):
        self.chooseHead()
        self.chooseTail()
        for index, block in enumerate(self.body):
            xPos = block.x * cellSize
            yPos = block.y * cellSize
            blockRect = pygame.Rect(xPos, yPos, cellSize, cellSize)

            if index == 0:
                WIN.blit(self.head, blockRect)
            elif index == len(self.body)-1:
                WIN.blit(self.tail, blockRect)
            else:
                previous_block_relation = self.body[index+1] - block
                next_block_relation = self.body[index-1] - block
                if previous_block_relation.x == next_block_relation.x:
                    WIN.blit(body_vert, blockRect)
                elif previous_block_relation.y == next_block_relation.y:
                    WIN.blit(body_horz,blockRect)
                else:
                    if previous_block_relation.x == -1 and next_block_relation.y == -1 or previous_block_relation.y == -1 and next_block_relation.x == -1:
                        WIN.blit(body_tl, blockRect)
                    if previous_block_relation.x == -1 and next_block_relation.y == 1 or previous_block_relation.y == 1 and next_block_relation.x == -1:
                        WIN.blit(body_bl, blockRect)
                    if previous_block_relation.x == 1 and next_block_relation.y == -1 or previous_block_relation.y == -1 and next_block_relation.x == 1:
                        WIN.blit(body_tr, blockRect)
                    if previous_block_relation.x == 1 and next_block_relation.y == 1 or previous_block_relation.y == 1 and next_block_relation.x == 1:
                        WIN.blit(body_br, blockRect)


    def moveSnake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def check_fail(self):
        if not 0 <= snake.body[0].x  < cellNumber or not 0 <= snake.body[0].y < cellNumber:
            pygame.quit()
            sys.exit()
        for block in snake.body[1:]:
            if block == snake.body[0]:
                pygame.quit()
                sys.exit()



class Fruit():
    def __init__(self):
        self.x = random.randint(0,cellNumber-1)
        self.y = random.randint(0,cellNumber-1)
        self.pos = pygame.math.Vector2(self.x , self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cellSize , self.pos.y * cellSize , cellSize, cellSize)
        WIN.blit(apple,fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cellNumber - 1)
        self.y = random.randint(0, cellNumber - 1)
        self.pos = pygame.math.Vector2(self.x, self.y)

fruit = Fruit()
snake = Snake()


def draw_grass():
    grass_color = (167,209,61)
    for row in range(cellNumber):
        if row % 2 == 0:
            for col in range(cellNumber):
                if col % 2 == 0:
                    grass_rect = pygame.Rect(col * cellSize, row * cellSize, cellSize,cellSize)
                    pygame.draw.rect(WIN, grass_color, grass_rect)
        else:
            for col in range(cellNumber):
                if col % 2 != 0:
                    grass_rect = pygame.Rect(col * cellSize, row * cellSize, cellSize, cellSize)
                    pygame.draw.rect(WIN, grass_color, grass_rect)



def checkCollision():
    if fruit.pos == snake.body[0]: # If head == fruit
        fruit.randomize()
        snake.add_block()


def main():
    run = True
    clock = pygame.time.Clock()
    FPS = 60


    def redraw():
        WIN.fill((175,215,70))
        draw_grass()
        fruit.draw_fruit()
        snake.drawSnake()
        pygame.display.update()


    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE , 150)

    while run:
        clock.tick(FPS)
        snake.check_fail()
        redraw()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == SCREEN_UPDATE:
                snake.moveSnake()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.direction.x != 1:
                    snake.direction = Vector2(-1,0)
                if event.key == pygame.K_DOWN and snake.direction.y != -1:
                    snake.direction = Vector2(0,1)
                if event.key == pygame.K_UP and snake.direction.y != 1:
                    snake.direction = Vector2(0,-1)
                if event.key == pygame.K_RIGHT and snake.direction.x != -1:
                    snake.direction = Vector2(1,0)
                if event.key == pygame.K_a and snake.direction.x != 1:
                    snake.direction = Vector2(-1,0)
                if event.key == pygame.K_s and snake.direction.y != -1:
                    snake.direction = Vector2(0,1)
                if event.key == pygame.K_w and snake.direction.y != 1:
                    snake.direction = Vector2(0,-1)
                if event.key == pygame.K_d and snake.direction.x != -1:
                    snake.direction = Vector2(1,0)
        checkCollision()



main()