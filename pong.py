# pong game useing pygame
import pygame # used for game dev
import time # used for loop timing
import math # for angles

NET = (211, 211, 211) # net colour (grey)
BALL = (255, 0, 0) # ball colour (red)
PLAYER = (255, 255, 255) # player colour (white)
BLACK = (0, 0, 0) # background colour
GREY = (50, 50, 50) # colour grey
BALL_RAD = 6 # ball radius
BALL_SPEED = 2.5 # ball speed (muliplier)
WIDTH = 1000 # width of screen
HEIGHT = 800 # height of screen including title
GAME_HEIGHT = 600 # game portion height
BLUE = (0, 0, 255) # goal explosion colour

leftPlayerX, leftPlayerY = 10, HEIGHT // 2 # left player paddle x,y (upper left of drawing)
rightPlayerX, rightPlayerY = WIDTH - 20, HEIGHT // 2 # right player paddle x,y (upper left of drawing)

ballX, ballY = WIDTH // 2, (HEIGHT // 2) + 35 # ball x,y (middle so +- 6px)
ballAngle = 0 # angle at which ball is moving (0 = East, 90 = South, 180 = West, 270 = North)

# used to increase speed if rallies are going for a long time as well as hold rally length
touchCount = 0

# player scores
leftPlayerScore = 0
rightPlayerScore = 0

# when ball contacts right paddle
def rightPaddle():
    global ballAngle, touchCount, BALL_SPEED
    touchCount += 1

    if touchCount % 8 == 0:
        BALL_SPEED += 0.5

    # we have established default angle now depending on location hit on paddle change
    if(ballY + 5 >= rightPlayerY and ballY - 5 <= rightPlayerY + 10):
        # top 3
        ballAngle = 225
    elif (ballY > rightPlayerY + 10 and ballY <= rightPlayerY + 20):
        # top 2
        ballAngle = 210
    elif (ballY > rightPlayerY + 20 and ballY <= rightPlayerY + 30):
        # top 1
        ballAngle = 195
    elif (ballY > rightPlayerY + 40 and ballY <= rightPlayerY + 50):
        # bottom 1
        ballAngle = 165
    elif (ballY > rightPlayerY + 50 and ballY <= rightPlayerY + 60):
       # bottom 2
        ballAngle = 150
    elif (ballY + 5 > rightPlayerY + 60 and ballY - 5 <= rightPlayerY + 70):
        # bottom 3
        ballAngle = 135
    else:
        # middle
        ballAngle = 180
    ballPosition()

# when ball contacts left paddle
def leftPaddle():
    global ballAngle, touchCount, BALL_SPEED
    touchCount += 1

    if touchCount % 8 == 0:
        BALL_SPEED += 0.5

    # we have established default angle now depending on location hit on paddle change
    if(ballY + 5 > leftPlayerY and ballY - 5 <= leftPlayerY - 10):
        # top 3
        ballAngle = 315
    elif (ballY > leftPlayerY + 10 and ballY <= leftPlayerY + 20):
        # top 2
        ballAngle = 330
    elif (ballY > leftPlayerY + 20 and ballY <= leftPlayerY + 30):
        # top 1
        ballAngle = 345
    elif (ballY > leftPlayerY + 40 and ballY <= leftPlayerY + 50):
        # bottom 1
        ballAngle = 15
    elif (ballY > leftPlayerY + 50 and ballY <= leftPlayerY + 60):
       # bottom 2
        ballAngle = 30
    elif (ballY + 5 > leftPlayerY + 60 and ballY - 5 <= leftPlayerY + 70):
        # bottom 3
        ballAngle = 45
    else:
        # middle
        ballAngle = 0
    ballPosition()

# check all collisions
def checkCollision():
    global ballAngle, leftPlayerScore, rightPlayerScore

    # ball hit left goal
    if ballX < 5:
        # ball hit left wall
        rightPlayerScore += 1
        goal()

    # ball hit right goal
    if ballX > 995:
        # ball hit right wall
        leftPlayerScore += 1
        goal()

    # ball bounce off top
    if ballY < 205:
        # checking direction
        if ballAngle < 90 and ballAngle > 270:
            # ball coming from left to right
            ballAngle = 90 + ballAngle
            ballAngle = 360 - ballAngle
        elif ballAngle > 90 and ballAngle < 270:
            # ball coming from right to left
            ballAngle = 270 - ballAngle
            ballAngle = 90 + ballAngle
        else:
            # ball is coming flat
            ballAngle += 20 # just in case so ball doest get stuck

    # ball bounce off bottom
    if ballY > HEIGHT - 5:
        # checking direction
        if ballAngle < 180:
            # ball coming from left to right
            ballAngle = 270 - ballAngle
            ballAngle = 90 + ballAngle
        elif ballAngle > 180:
            # ball coming from right top left
            ballAngle = 90 + ballAngle
            ballAngle = 360 - ballAngle
        else:
            # ball is coming flat
            ballAngle += 20 # just in case so ball doest get stuck

    # checking if ball hit paddles
    if ballX - 5 >= 10 and ballX - 5 <= 15:
        if ballY + 5 > leftPlayerY and ballY - 5 < leftPlayerY + 70:
            # hit left paddle
            leftPaddle()
    elif ballX + 5 >= WIDTH - 15 and ballX + 5 <= WIDTH - 5:
        if ballY + 5 > rightPlayerY and ballY - 5 < rightPlayerY + 70:
            # hit right paddle
            rightPaddle()
        
# Calculate new ball position
def ballPosition():
    global ballX
    global ballY
    ballAngleRad = math.radians(ballAngle)
    ballX += BALL_SPEED * math.cos(ballAngleRad)
    ballY += BALL_SPEED * math.sin(ballAngleRad)

# draw player paddles
def drawGame():
    # draw the ball
    pygame.draw.circle(screen, BALL, (int(ballX), int(ballY)), BALL_RAD) # drawn from centre co ord
    # draw players
    pygame.draw.rect(screen, PLAYER, (leftPlayerX, leftPlayerY, 5, 70)) # drawn from top left co ord
    pygame.draw.rect(screen, PLAYER, (rightPlayerX, rightPlayerY, 5, 70)) # drawn from top left co ord
    # draw the top of the game area
    pygame.draw.rect(screen, GREY, (0, 195, WIDTH, 5))

# drawing text on screen
def drawText():
    font = pygame.font.Font(None, 200)  # None uses the default font, and FONT_SIZE sets the font size
    text = font.render(str(leftPlayerScore), True, PLAYER)
    text_rect = text.get_rect()
    text_rect.center = (100, 100)

    text1 = font.render(str(rightPlayerScore), True, PLAYER)
    text_rect1 = text1.get_rect()
    text_rect1.center = (900, 100)

    font2 = pygame.font.Font(None, 200)  # None uses the default font, and FONT_SIZE sets the font size
    text2 = font2.render("PONG", True, PLAYER)
    text_rect2 = text2.get_rect()
    text_rect2.center = (WIDTH // 2, 100)

    font3 = pygame.font.Font(None, 30)  # None uses the default font, and FONT_SIZE sets the font size
    text3 = font3.render(f"current rally: {str(touchCount)}", True, PLAYER)
    text_rect3 = text3.get_rect()
    text_rect3.center = (WIDTH // 2, 175)

    screen.blit(text, text_rect)
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)
    screen.blit(text3, text_rect3)

# player scored a goal
def goal():
    global ballAngle, ballX, ballY, leftPlayerY, rightPlayerY, touchCount, BALL_SPEED
    countdown = 3 # countdown counter init
    touchCount = 0 # resetting touch count
    BALL_SPEED = 2.5 # resetting ball speed to default

    expX = ballX # explosion X co ord
    ballX = -10 # moving ball of screen

    # check for game over
    if leftPlayerScore > 6:
        # left player has won text
        screen.fill(BLACK)
        font = pygame.font.Font(None, 100)  # None uses the default font, and FONT_SIZE sets the font size
        text = font.render("Left Player Wins!", True, PLAYER)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        screen.blit(text, text_rect)

        pygame.display.update()

        running = True
        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
    elif rightPlayerScore > 6:
        # right player has won text
        screen.fill(BLACK)
        font = pygame.font.Font(None, 100)  # None uses the default font, and FONT_SIZE sets the font size
        text = font.render("Right Player Wins!", True, PLAYER)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        screen.blit(text, text_rect)

        pygame.display.update()

        running = True
        while running:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if keys[pygame.K_ESCAPE]:
                pygame.quit()

    # goal text
    screen.fill(BLACK)
    font = pygame.font.Font(None, 300)  # None uses the default font, and FONT_SIZE sets the font size
    text = font.render("GOAL!", True, PLAYER)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(text, text_rect)

    drawGame()
    drawText()
    pygame.display.update()

    # goal "explosion"
    explosionRadius = 1
    for i in range(0,100):
        pygame.draw.circle(screen, BLUE, (expX, ballY), explosionRadius)
        pygame.display.update()
        explosionRadius += 0.5
        time.sleep(0.02)

    # who scored
    if leftPlayerScore > rightPlayerScore:
        ballAngle = 0
    else:
        ballAngle = 180

    # countdown display!
    while countdown > 0:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 300)  # None uses the default font, and FONT_SIZE sets the font size
        text = font.render(str(countdown), True, PLAYER)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        screen.blit(text, text_rect)
        countdown -= 1

        drawGame()
        drawText()
        pygame.display.update()

        time.sleep(0.8)

    screen.fill(BLACK)
    font = pygame.font.Font(None, 300)  # None uses the default font, and FONT_SIZE sets the font size
    text = font.render("GO!", True, PLAYER)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(text, text_rect)
    countdown -= 1

    drawGame()
    drawText()
    pygame.display.update()

    time.sleep(0.8)

    # change ball location to middle of screen
    ballX, ballY = WIDTH // 2, HEIGHT // 2 + 35 # offset by 35 so that it will hit paddle if not moved
    leftPlayerY, rightPlayerY = HEIGHT // 2, HEIGHT // 2
    
# initialize pygame
pygame.init()

# set window width and caption
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# main game logic loop
running = True
while running:
    time.sleep(0.005)

    # listening for inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # input handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if rightPlayerY > 200:
            rightPlayerY -= 2.5
    if keys[pygame.K_DOWN]:
        if rightPlayerY + 70 < HEIGHT:
            rightPlayerY += 2.5
    if keys[pygame.K_w]:
        if leftPlayerY > 200:
            leftPlayerY -= 2.5
    if keys[pygame.K_s]:
        if leftPlayerY + 70 < HEIGHT:
            leftPlayerY += 2.5
    if keys[pygame.K_ESCAPE]:
        running = False

    # Clear the screen
    screen.fill(BLACK)
    checkCollision()
    ballPosition()
    drawGame()
    drawText()
    pygame.display.update() # finally update display

# quit pygame, game is over
pygame.quit()