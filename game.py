import pygame
from snake import Snake
from pygame.locals import *
import random

pygame.init()
width = 500
height = 500
screen = pygame.display.set_mode((width, height))

draw_apple = True
apple_eaten = False

NUM_SNAKES = 1
CELL_SIZE = 10

FRAMES_PER_TURN = 50

BACKGROUND_COL = (0, 0, 255)
SNAKE_COL = (0, 255, 0)
APPLE_COL = (255, 0, 0)

score = 0

Q ={}
snake = Snake(width, height)



play_game = True
frames_passed = 0
dir_updated = False
while play_game:
    screen.fill(BACKGROUND_COL)

    #gets the key events and sets the direction of the snake
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play_game = False
        if event.type == pygame.KEYDOWN and not dir_updated:
            if event.key == pygame.K_UP:
                snake.updateDirection("UP")
            if event.key == pygame.K_RIGHT:
                snake.updateDirection("RIGHT")
            if event.key == pygame.K_DOWN:
                snake.updateDirection("DOWN")
            if event.key == pygame.K_LEFT:
                snake.updateDirection("LEFT")
            dir_updated = True

    #sets the apple location
    if draw_apple:
        draw_apple = False
        snake.setNewAppleLocation()
    #draws apple location
    pygame.draw.rect(screen, APPLE_COL, (snake.apple[0], snake.apple[1], CELL_SIZE, CELL_SIZE))

    #checks to see if the snake head is on the apple aka eats the appel
    if snake.getHeadLocation() == snake.apple:
        draw_apple = True
        apple_eaten = True
        score += 1

    #dictates the speed of the game
    if frames_passed > FRAMES_PER_TURN:
        dir_updated = False
        if not snake.isAlive(): play_game = False
        frames_passed = 0
        snake.updateBody(apple_eaten)
        apple_eaten = False

    #draws the snake at every time step
    for snek in snake.body:
        pygame.draw.rect(screen, SNAKE_COL, (snek[0], snek[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, SNAKE_COL, (snek[0] + 1, snek[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2))

    pygame.display.update()
    frames_passed += 1

print(f"You got {score} points!")
pygame.quit()

