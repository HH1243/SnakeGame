import pygame
import random
import time

import pygame.freetype

# defining window size
windowSize_x = 1280
windowSize_y = 720

# defining colours
green = pygame.Color(0, 100, 33)
yellow = pygame.Color(255, 255, 0)
red = pygame.Color(255, 0, 0)
white = pygame.Color(0, 0, 0)

pygame.init()

pygame.display.set_caption("Snake Game")

screen = pygame.display.set_mode((windowSize_x,windowSize_y)) 

clock = pygame.time.Clock()

# define snake speed
snakeSpeed = 15

# define starting snake position and first 4 blocks of body
snakePosition = [(windowSize_x//2), (windowSize_y//2)]
snakeBody = [[(windowSize_x//2), (windowSize_y//2)], 
             [((windowSize_x//2) - 20), (windowSize_y//2)], 
             [((windowSize_x//2) - 40), (windowSize_y//2)], 
             [((windowSize_x//2) - 60), (windowSize_y//2)]]


# define default snake direction
snakeDirection = 'RIGHT'

# variable for input direction from user
changedir = 'RIGHT'

# Dictionary to map opposite directions
oppositeDirection = {
    'UP': 'DOWN',
    'DOWN': 'UP',
    'RIGHT': 'LEFT',
    'LEFT': 'RIGHT'
}

# Dictionary to map position changes
positionChange = {

    'UP': (0, -20),
    'DOWN': (0, 20),
    'RIGHT': (20, 0),
    'LEFT': (-20, 0)
}

# Creates random x and y coordinates within dimensions of window
fruitPosition = ((random.randrange(1, windowSize_x // 20) * 20, (random.randrange(1, windowSize_y // 20) * 20)))
fruitSpawn = True

# Variable to store user score
score = 0

# function to display score
def scoreboard ():
    
    # font and size for scoreboard
    scoreFont = pygame.font.Font('Comic Sans MS.ttf', 30)

    # create display on surface object
    scoreSurface = scoreFont.render('Score: ' + str(score), True, white)
    screen.blit(scoreSurface, (10, 10))

def gameover ():

    # fills background
    screen.fill(green)

    # font and size for gameover
    gameoverFont = pygame.font.Font('Comic Sans MS.ttf', 50) 

    # Render the two lines separately
    gameoverText = gameoverFont.render('Game Over', True, white)
    scoreText = gameoverFont.render('Score: ' + str(score), True, white)

    # Get the positions to center the text on the screen
    gameoverRect = gameoverText.get_rect(center=(windowSize_x // 2, windowSize_y // 2 - 20))
    scoreRect = scoreText.get_rect(center=(windowSize_x // 2, windowSize_y // 2 + 40))

    # Blit the text to the screen
    screen.blit(gameoverText, gameoverRect)
    screen.blit(scoreText, scoreRect)


    pygame.display.flip()
    
    # quit after 3 seconds 
    time.sleep(3)

    pygame.quit()

    quit()


while True:

    # Process player inputs 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                changedir = 'UP'
            elif event.key == pygame.K_s:
                changedir = 'DOWN'
            elif event.key == pygame.K_d:
                changedir = 'RIGHT'
            elif event.key == pygame.K_a:
                changedir = 'LEFT'
    
    # Check if the changed direction is not the opposite of the current direction
    if changedir != oppositeDirection[snakeDirection]:
        snakeDirection = changedir
    
    # Use dictionary to change direction
    movement = positionChange[snakeDirection]
    snakePosition[0] += movement[0]
    snakePosition[1] += movement[1]

    # inserts new snake head position to the front of the snake body array
    snakeBody.insert(0, list(snakePosition))


    # Adds to score and snake size if fruit is eaten
    if (snakePosition[0] == fruitPosition[0]) and (snakePosition[1] == fruitPosition[1]):

        fruitSpawn = False

        score += 1

    else:

        # removes position of the back of the snake body array
        snakeBody.pop()
    

    if not fruitSpawn:

        fruitPosition = [random.randrange(2, (windowSize_x - 10) // 20) * 20, (random.randrange(2, (windowSize_y - 10) // 20) * 20)]


    fruitSpawn = True
    
    # fills background
    screen.fill(green)
    
    # creates green box for each position in snakeBody
    for pos in snakeBody:

        pygame.draw.rect(screen, yellow, pygame.Rect(pos[0], pos[1], 20, 20))
    
    # creates a red box for the fruit
    pygame.draw.rect(screen, red, pygame.Rect(fruitPosition[0], fruitPosition[1], 20, 20))

    # call scoreboard function to display current score
    scoreboard()

    # gameover conditions

    if (snakePosition[0]) < 0 or (snakePosition[0] > windowSize_x - 20): # if snake goes out of bounds in x plane

        gameover()

    if (snakePosition[1]) < 0 or (snakePosition[1] > windowSize_y - 20): # if snake goes out of bounds in y plane

        gameover()

    
    for pos in snakeBody[1:]: # if snake runs into own body

        if snakePosition[0] == pos[0]:

            if snakePosition[1] == pos[1]:

                gameover()

    # Refresh on-screen display
    pygame.display.flip() 

    clock.tick(snakeSpeed)


