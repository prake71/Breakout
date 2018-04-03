# Brickout Game V 0.1
# 2018 by Peter Rake

# color constants
# a website for finding out color names
# https://www.w3schools.com/colors/colors_converter.asp
GREY = [105, 105, 105]
BLACK = [0, 0, 0]
PINK = [168, 76, 96]
BROWN = [133, 107, 17]
OTHERBROWN = [157, 90, 48]
GREEN = [28, 120, 29]
LIGHTGREEN = [56, 141, 47]
DARKGREEN = [46, 137, 95]
BLUE = [91, 92, 214]
BALL = [145, 100, 71]

# I - Import and Initialize
import pygame

pygame.mixer.pre_init(22050, -16, 1, 2048)
pygame.mixer.init()

pygame.init()

# D - Display
screen = pygame.display.set_mode([640, 500])
screen.fill(BLACK)


# E - Entitiess

# classes
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()


# A - Action
# A - Assign Values to key variables
blocks_container = pygame.sprite.Group()
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

paddle = Block(OTHERBROWN, 64, 8)
paddle.rect.x = (640 - 64) / 2
paddle.rect.y = 500 - 22
all_sprites.add(paddle)

# Create a ball sprite
ball = Block(BALL, 10, 10)
ball.rect.x = (640 - 10) / 2
ball.rect.y = paddle.rect.top - 20
all_sprites.add(ball)

# Score
font = pygame.font.Font("2600.ttf", 38)
text = font.render("000", False, GREY)

# Sounds
pygame.mixer.init()
snd_paddle_hit = pygame.mixer.Sound("hit_paddle.ogg")
snd_side_wall_hit = pygame.mixer.Sound("hit_side_wall.ogg")
snd_block_row1 = pygame.mixer.Sound("hit_block_row_1.ogg")
snd_block_row2 = pygame.mixer.Sound("hit_block_row_2.ogg")
snd_block_row3 = pygame.mixer.Sound("hit_block_row_3.ogg")
snd_block_row4 = pygame.mixer.Sound("hit_block_row_4.ogg")
snd_block_row5 = pygame.mixer.Sound("hit_block_row_5.ogg")
snd_block_row6 = pygame.mixer.Sound("hit_block_row_6.ogg")
"""
BxH = 48x20
165 Score 80   Paddles 96 Level
 D 16 D 16 D

"""

# Set the initial ball speed
ball_dx = 1
ball_dy = 1
ball_speed = 1
ball_speed_max = 1.1

# A couple of 'flags' (Boolean values)
ball_in_play = False
just_bounced = False

# 1 block = 32 pixel x 16 pixel
color_list = [GREEN, LIGHTGREEN, PINK, DARKGREEN, BROWN, BLUE]


def setup_blocks():
    # Create a horizontal row of blocks for each color
    for block_row, block_color in enumerate(color_list):
        for block_column in range(1, 19):
            # Create a block, leaving 1 pixels around the four edges
            block = Block(block_color, 32, 16)
            block.rect.x = block_column * 32 + 1
            block.rect.y = 145 + block_row * 16
            blocks.add(block)
            all_sprites.add(block)


# Create a horizontal row of blocks for each color
setup_blocks()
"""
for block_row, block_color in enumerate(color_list):
    for block_column in range(1,19):
        # Create a block, leaving 1 pixels around the four edges
        block = Block(block_color, 32, 16)
        block.rect.x = block_column * 32 + 1
        block.rect.y = 145 + block_row * 16
        blocks.add(block)
        all_sprites.add(block)
"""
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

clock = pygame.time.Clock()
game_over = False
score = 0
lives = 5

live_text = font.render("{}".format(lives), False, GREY)
mouse_x_old = paddle.rect.x
assert isinstance(paddle.rect.x, object)
mouse_x = paddle.rect.x
# L - Loop
while not game_over:
    # T - Timer
    clock.tick(240)
    # E- Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
    # b1, b2, b3 = pygame.mouse.get_pressed()
    if pygame.mouse.get_pressed()[0]:
        if lives > 0 and ball_in_play == False:
            ball_in_play = True
            ball.rect.x = paddle.rect.centerx
            ball.rect.y = paddle.rect.top - 20
            all_sprites.add(ball)
    if pygame.mouse.get_pressed()[2] and lives == 0:
        lives = 5
        score = 0
        setup_blocks()
        ball.rect.x = paddle.rect.centerx
        ball.rect.y = paddle.rect.top - 20
        ball_in_play = True
        all_sprites.add(ball)

    # print("Mouse Speed per frame:" , abs(mouse_x_old - mouse_x) )
    mouse_x_old = mouse_x
    mouse_x = pygame.mouse.get_pos()[0]
    mouse_pos_equal = True
    while mouse_pos_equal:
        mouse_pos_equal = mouse_x != paddle.rect.left
        # print(mouse_pos_equal)
        if mouse_x < paddle.rect.left:
            if paddle.rect.left > 32:
                paddle.rect.x = paddle.rect.x - 1
            else:
                mouse_pos_equal = False
        elif mouse_x > paddle.rect.left:
            if paddle.rect.right < 640 - 32:
                paddle.rect.x = paddle.rect.x + 1
            else:
                mouse_pos_equal = False

    if ball_in_play:
        # Move the ball
        ball.rect.x += ball_dx
        ball.rect.y += ball_dy
        # Check if it collidedd with the paddle
        if ball.rect.y < paddle.rect.top:
            just_bounced = False
        # Bounce off the screen edges
        if ball.rect.left <= 0 + 32:
            snd_side_wall_hit.play()
            ball.rect.x = 0 + 32
            ball_dx = -ball_dx
        if ball.rect.y <= 0 + 96:
            snd_side_wall_hit.play()
            ball.rect.y = 0 + 96
            ball_dy = -ball_dy
        if ball.rect.x > 640 - 32 - 10:
            snd_side_wall_hit.play()
            ball.rect.x = 640 - 32 - 10
            ball_dx = -ball_dx
        # Check if the ball bounced off the paddle
        # Collision detection between two sprites, using rects.
        if pygame.sprite.collide_rect(ball, paddle) and not just_bounced:
            snd_paddle_hit.play()
            ball_dy = -ball_dy
            just_bounced = True
        # While ball and paddle are in contact, don't bounce again
        # Ball didn't - game over
        elif ball.rect.y > paddle.rect.top + 10 / 2:
            ball_in_play = False
            all_sprites.remove(ball)
            lives = lives - 1
        # Check if the ball bounced off a block
        blocks_hit_list = pygame.sprite.spritecollide(ball, blocks, True)
        if blocks_hit_list:
            if ball_speed < ball_speed_max:
                ball_speed += 0.01

            print(ball_speed)
            for block in blocks_hit_list:
                score = score + 1
                print(block.rect.y)
                if block.rect.y == 145 + 6 * 16:
                    snd_block_row1.play()
                elif block.rect.y == 145 + 5 * 16:
                    snd_block_row2.play()
                elif block.rect.y == 145 + 4 * 16:
                    snd_block_row3.play()
                elif block.rect.y == 145 + 3 * 16:
                    snd_block_row4.play()
                elif block.rect.y == 145 + 2 * 16:
                    snd_block_row5.play()
                elif block.rect.y == 145 + 1 * 16:
                    snd_block_row6.play()
            # ball_dy = -ball_dy * ball_speeds

            blocks_container.add(blocks_hit_list)
            ball_dy = -ball_dy  # * ball_speed

    # scorestr = "{:0>3}".format(score)
    text = font.render("{:0>3}".format(score), False, GREY)
    live_text = font.render("{}".format(lives), False, GREY)
    all_sprites.update()
    screen.fill(BLACK)
    screen.blit(text, (165, 32))
    screen.blit(live_text, (165 + text.get_width() + 80, 32))
    # R - Refresh Display
    all_sprites.draw(screen)
    pygame.display.update()
pygame.quit()
