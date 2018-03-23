# Brickout Game V 0.1
# 2018 by Peter Rake

# color constants
# a website for finding out color names
# https://www.w3schools.com/colors/colors_converter.asp
GREY =  [105,105,105]
BLACK = [0,  0,  0]
PINK = [168, 76, 96]
BROWN = [133,107, 17]
OTHERBROWN = [157, 90, 48]
GREEN = [28,120, 29]
LIGHTGREEN = [56,141, 47]
DARKGREEN = [46,137, 95]
BLUE = [91, 92,214]
BALL = [145, 100, 71]

# I - Import and Initialize
import pygame

pygame.init()

# D - Display
screen = pygame.display.set_mode([640, 500])
screen.fill(BLACK)

# E - Entities

# classes
class Block(pygame.sprite.Sprite):
    def __init__(self,color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

# A - Action
# A - Assign Values to key variables
blocks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()

wall_left = Block(GREY, 32, 430)
wall_right = Block(GREY, 32, 430)
wall_horiz = Block(GREY, 640, 32)
wall_left.rect.x = 0
wall_left.rect.y = 64
wall_right.rect.x = 640 - 32
wall_right.rect.y = 64
wall_horiz.rect.x = 0
wall_horiz.rect.y = 64
all_sprites.add(wall_left, wall_right, wall_horiz)
walls.add(wall_left, wall_right, wall_horiz)


paddle = Block(OTHERBROWN, 64, 8 )
paddle.rect.x = (640 - 64) / 2
paddle.rect.y = 500 - 22
all_sprites.add(paddle)

# Create a ball sprite
ball = Block(BALL, 10, 10)
ball.rect.x = (640 - 10) / 2
ball.rect.y = paddle.rect.top - 20
all_sprites.add(ball)

# Score
font = pygame.font.SysFont("PressStart2P.ttf", 40)
text = font.render("000", False, GREY)

"""
BxH = 48x20
165 Score 80   Paddles 96 Level
 D 16 D 16 D
Digits:
       .byte $E7 ; |XXX  XXX| $F000
       .byte $A5 ; |X X  X X| $F001
       .byte $A5 ; |X X  X X| $F002
       .byte $A5 ; |X X  X X| $F003
       .byte $E7 ; |XXX  XXX| $F004

       .byte $42 ; | X    X | $F005
       .byte $42 ; | X    X | $F006
       .byte $42 ; | X    X | $F007
       .byte $42 ; | X    X | $F008
       .byte $42 ; | X    X | $F009

       .byte $E7 ; |XXX  XXX| $F00A
       .byte $24 ; |  X  X  | $F00B
       .byte $E7 ; |XXX  XXX| $F00C
       .byte $81 ; |X      X| $F00D
       .byte $E7 ; |XXX  XXX| $F00E

       .byte $E7 ; |XXX  XXX| $F00F
       .byte $81 ; |X      X| $F010
       .byte $C3 ; |XX    XX| $F011
       .byte $81 ; |X      X| $F012
       .byte $E7 ; |XXX  XXX| $F013

       .byte $81 ; |X      X| $F014
       .byte $81 ; |X      X| $F015
       .byte $E7 ; |XXX  XXX| $F016
       .byte $A5 ; |X X  X X| $F017
       .byte $A5 ; |X X  X X| $F018

       .byte $E7 ; |XXX  XXX| $F019
       .byte $81 ; |X      X| $F01A
       .byte $E7 ; |XXX  XXX| $F01B
       .byte $24 ; |  X  X  | $F01C
       .byte $E7 ; |XXX  XXX| $F01D

       .byte $E7 ; |XXX  XXX| $F01E
       .byte $A5 ; |X X  X X| $F01F
       .byte $E7 ; |XXX  XXX| $F020
       .byte $24 ; |  X  X  | $F021
       .byte $24 ; |  X  X  | $F022

       .byte $81 ; |X      X| $F023
       .byte $81 ; |X      X| $F024
       .byte $81 ; |X      X| $F025
       .byte $81 ; |X      X| $F026
       .byte $E7 ; |XXX  XXX| $F027

       .byte $E7 ; |XXX  XXX| $F028
       .byte $A5 ; |X X  X X| $F029
       .byte $E7 ; |XXX  XXX| $F02A
       .byte $A5 ; |X X  X X| $F02B
       .byte $E7 ; |XXX  XXX| $F02C

       .byte $81 ; |X      X| $F02D
       .byte $81 ; |X      X| $F02E
       .byte $E7 ; |XXX  XXX| $F02F
       .byte $A5 ; |X X  X X| $F030
       .byte $E7 ; |XXX  XXX| $F031

       .byte $00 ; |        | $F032
       .byte $00 ; |        | $F033
       .byte $00 ; |        | $F034
       .byte $00 ; |        | $F035
       .byte $00 ; |        | $F036

"""

# Set the initial ball speed
ball_dx = 1.5
ball_dy = 1.8

# A couple of 'flags' (Boolean values)
ball_in_play = False
just_bounced = False

# 1 block = 32 pixel x 16 pixel
color_list = [GREEN, LIGHTGREEN, PINK, DARKGREEN, BROWN, BLUE]
# Create a horizontal row of blocks for each color
for block_row, block_color in enumerate(color_list):
    for block_column in range(1,19):
        # Create a block, leaving 1 pixels around the four edges
        block = Block(block_color, 32, 16)
        block.rect.x = block_column * 32 + 1
        block.rect.y = 145 + block_row * 16
        blocks.add(block)
        all_sprites.add(block)




pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

clock = pygame.time.Clock()
game_over = False
score = 0
lives = 5

live_text = font.render("{}".format(lives), False, GREY)

# L - Loop
while not game_over:
    # T - Timer
    clock.tick(120)
    # E- Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
    mouse_x = pygame.mouse.get_pos()[0]
    #b1, b2, b3 = pygame.mouse.get_pressed()
    if pygame.mouse.get_pressed()[0]:
        if lives > 0:
            ball_in_play = True
            ball.rect.x = paddle.rect.centerx
            ball.rect.y = paddle.rect.top - 20
            all_sprites.add(ball)
    if pygame.mouse.get_pressed()[2] and lives == 0:
        lives = 5
        score = 0
        ball.rect.x = paddle.rect.centerx
        ball.rect.y = paddle.rect.top - 20
        ball_in_play = True
        all_sprites.add(ball)

    mouse_pos_equal = True
    while mouse_pos_equal:
        mouse_pos_equal = mouse_x != paddle.rect.left
        print(mouse_pos_equal)
        if mouse_x <  paddle.rect.left:
            paddle.rect.x = paddle.rect.x - 1
        elif mouse_x > paddle.rect.left:
            if paddle.rect.right < 640 - 32:
                paddle.rect.x = paddle.rect.x + 1
            else:
                mouse_pos_equal = False
    if ball_in_play:
        # Move the ball
        ball.rect.x += ball_dx
        ball.rect.y += ball_dy
        # Check if it collided with the paddle
        if ball.rect.y < paddle.rect.top:
            just_bounced = False
        # Bounce off the screen edges
        if (ball.rect.x <= 0 + 32):
            ball.rect.x = 0 + 32
            ball_dx = -ball_dx
        if (ball.rect.y <= 0 + 96):
            ball.rect.y = 0 + 96
            ball_dy = -ball_dy
        if (ball.rect.x > 640 - 10 - 32):
            ball.rect.x = 640 - 10 - 32
            ball_dx = -ball_dx
        # Check if the ball bounced off the paddle
        if (pygame.sprite.collide_rect(ball, paddle) and not just_bounced):
            ball_dy = -ball_dy
            just_bounced = True
        # While ball and paddle are in contact, don't bounce again
        # Ball didn't - game over
        elif (ball.rect.y > paddle.rect.top + 10 / 2):
            ball_in_play = False
            all_sprites.remove(ball)
            lives = lives - 1
        # Check if the ball bounced off a block
        blocks_hit_list = pygame.sprite.spritecollide(ball, blocks, True)
        if blocks_hit_list:
            ball_dy = -ball_dy
            score = score + 1
    #scorestr = "{:0>3}".format(score)
    text = font.render("{:0>3}".format(score), False, GREY)
    live_text = font.render("{}".format(lives), False, GREY)
    all_sprites.update()
    screen.fill(BLACK)
    screen.blit(text, (144,36) )
    screen.blit(live_text, (250, 36))
    # R - Refresh Display
    all_sprites.draw(screen)
    pygame.display.update()
pygame.quit()


