import pygame
import random

# defining window size
windowSize_x = 1280
windowSize_y = 720

# defining colours
green = pygame.Color(0, 255, 0)


pygame.init()

pygame.display.set_caption("Snake Game")
screen = pygame.display.set_mode((windowSize_x,windowSize_y))

clock = pygame.time.Clock()

# define snake speed
snakeSpeed = 15

# define starting snake position and first 4 blocks of body
snakePosition = [(windowSize_x//2), (windowSize_y//2)]
snakeBody = [[(windowSize_x//2), (windowSize_y//2)], 
             [((windowSize_x//2) - 10), (windowSize_y//2)], 
             [((windowSize_x//2) - 20), (windowSize_y//2)], 
             [((windowSize_x//2) - 30), (windowSize_y//2)]]


# define defualt snake direction
snakeDirection = 'RIGHT'

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snakeDirection = 'UP'
            elif event.key == pygame.K_s:
                snakeDirection = 'DOWN'
            elif event.key == pygame.K_d:
                snakeDirection = 'RIGHT'
            elif event.key == pygame.K_a:
                snakeDirection = 'LEFT'
    

    if snakeDirection == 'UP':
        snakePosition[1] -= 10
    elif snakeDirection == 'DOWN':
        snakePosition[1] += 10
    elif snakeDirection == 'LEFT':
        snakePosition[0] -= 10
    elif snakeDirection == 'RIGHT':
        snakePosition[0] += 10
    
    snakeBody.insert(0, list(snakePosition))
    snakeBody.pop()

    screen.fill(pygame.Color(0, 0, 0))

    for pos in snakeBody:

        pygame.draw.rect(screen, green, pygame.Rect(pos[0], pos[1], 20, 20))


    pygame.display.flip()  # Refresh on-screen display

    clock.tick(snakeSpeed)         # wait until next frame (at 60 FPS)

