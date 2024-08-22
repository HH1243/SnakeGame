import pygame
import random
import time


# defining window size
windowSize_x = 720
windowSize_y = 560

# defining block size
blockSize = 40

# defining colours
green = pygame.Color(0, 100, 33)
yellow = pygame.Color(255, 255, 0)
red = pygame.Color(255, 0, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

pygame.init()

pygame.display.set_caption("Snake Game")

screen = pygame.display.set_mode((windowSize_x,windowSize_y)) 

# load background image
background = pygame.image.load('assets/images/snakeBackground.png')
# load fruit image
grape = pygame.image.load('assets/images/grape.png')
# load snake head image
snakeHead = pygame.image.load('assets/images/snakehead.png')
# load snake body image
snakeMiddle = pygame.image.load('assets/images/snakeMiddle.png')

resizedBackground = pygame.transform.scale(background, (windowSize_x, windowSize_y))
resizedGrape = pygame.transform.scale(grape, (blockSize, blockSize))
resizedHead = pygame.transform.scale(snakeHead, (blockSize, blockSize))
resizedMiddle = pygame.transform.scale(snakeMiddle, (blockSize, blockSize))
# copy image content onto screen
screen.blit(resizedBackground, (0, 0))

clock = pygame.time.Clock()

# define snake speed
snakeSpeed = 12

# define starting snake position and first 4 blocks of body
snakePosition = [(windowSize_x//2), (windowSize_y//2)]
snakeBody = [[(windowSize_x//2), (windowSize_y//2)], 
             [((windowSize_x//2) - blockSize), (windowSize_y//2)], 
             [((windowSize_x//2) - (2 * blockSize)), (windowSize_y//2)], 
             [((windowSize_x//2) - (3 * blockSize)), (windowSize_y//2)]]


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

    'UP': (0, -blockSize, 180),
    'DOWN': (0, blockSize, 0),
    'RIGHT': (blockSize, 0, 90),
    'LEFT': (-blockSize, 0, 270)
}

# Creates random x and y coordinates within dimensions of window
fruitPosition = ((random.randrange(1, windowSize_x // blockSize) * blockSize, (random.randrange(1, windowSize_y // blockSize) * blockSize)))
fruitSpawn = True

# Variable to store user score
score = 0

# Variable to store high score
highScore = 0


# function to display score
def scoreboard ():
    
    # font and size for scoreboard
    scoreFont = pygame.font.Font('assets/data/Comic Sans MS.ttf', 30)
    highscoreFont = pygame.font.Font('assets/data/Comic Sans MS.ttf', 19)

    # create display on surface object
    scoreSurface = scoreFont.render('Score: ' + str(score), True, white, black)
    highscoreSurface = highscoreFont.render('Highscore: ' + str(highScore), True, red, black)

    screen.blit(scoreSurface, (10, 10))
    screen.blit(highscoreSurface, (10, 52))


# function for gameover screen
def gameover ():

    screen.blit(resizedBackground, (0, 0))

    # font and size for gameover
    gameoverFont = pygame.font.Font('assets/data/Comic Sans MS.ttf', 50) 

    # Render the two lines separately
    gameoverText = gameoverFont.render('Game Over', True, white, black)
    scoreText = gameoverFont.render('Score: ' + str(score), True, white, black)
    highscoreText = gameoverFont.render('Highscore: ' + str(highScore), True, red, black)

    # Get the positions to center the text on the screen
    gameoverRect = gameoverText.get_rect(center=(windowSize_x // 2, windowSize_y // 2 - 80))
    scoreRect = scoreText.get_rect(center=(windowSize_x // 2, windowSize_y // 2 -20))
    highscoreRect = highscoreText.get_rect(center=(windowSize_x // 2, windowSize_y // 2 + 50))

    # Blit the text to the screen
    screen.blit(gameoverText, gameoverRect)
    screen.blit(scoreText, scoreRect)
    screen.blit(highscoreText, highscoreRect)


    pygame.display.flip()
    
    # quit after 3 seconds 
    time.sleep(3)

    pygame.quit()

    quit()

# function to update or grab highscore
def updateHighscore ():

    # open file in read mode
    f = open('assets/data/score.txt', 'r')
    # read all lines into a list
    firstLine = f.readline().strip()
    # save first line into variable 
    highScore = int(firstLine)

    f.close()

    # update if the current score is higher than highscore
    if score > highScore:

        # open file in write mode
        file = open('assets/data/score.txt', 'w')
        # write current score in file
        file.write(str(score))
        # close file
        file.close()

    return highScore


# funtion to spawn fruit
def spawnFruit():

    # create a set out of snake body positions
    snakebodySet = set(tuple(pos) for pos in snakeBody)

    # loops if fruit spawns in the same position as the snake
    while True:

        fruitPosition = [random.randrange(2, (windowSize_x - 10) // blockSize) * blockSize, (random.randrange(2, (windowSize_y - 10) // blockSize) * blockSize)]

        if (tuple(fruitPosition) not in snakebodySet):

            return fruitPosition


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
    rotatedHead = pygame.transform.rotate(resizedHead, movement[2])

    # inserts new snake head position to the front of the snake body array
    snakeBody.insert(0, list(snakePosition))


    # Adds to score and snake size if fruit is eaten
    if (snakePosition[0] == fruitPosition[0]) and (snakePosition[1] == fruitPosition[1]):

        fruitSpawn = False

        score += 1

    else:

        
        snakeBody.pop() # removes position of the back of the snake body array
    

    if not fruitSpawn:

        fruitPosition = spawnFruit()

    screen.blit(resizedBackground, (0, 0))


    fruitSpawn = True
    
    # applies snakehead image to first block of snake
    screen.blit(rotatedHead, snakePosition)
    
    # creates body
    for pos in snakeBody[1:]:

        # creates a red box for the fruit
        screen.blit(resizedMiddle, pos)
    
    # creates a red box for the fruit
    screen.blit(resizedGrape, fruitPosition)

    # call update highscore function
    highScore = updateHighscore()

    # call scoreboard function to display current score
    scoreboard()


    # gameover conditions
    if (snakePosition[0]) < 0 or (snakePosition[0] > windowSize_x - blockSize): # if snake goes out of bounds in x plane

        gameover()

    if (snakePosition[1]) < 0 or (snakePosition[1] > windowSize_y - blockSize): # if snake goes out of bounds in y plane

        gameover()

    
    for pos in snakeBody[1:]: # if snake runs into own body
        
        if snakePosition[0] == pos[0]:

            if snakePosition[1] == pos[1]:

                gameover()

    # Refresh on-screen display
    pygame.display.flip() 

    clock.tick(snakeSpeed)


