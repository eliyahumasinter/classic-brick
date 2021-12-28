import pygame
import random

pygame.init()

WIDTH = 500
HEIGHT = 500
BG_COLOR = (125, 125, 125)
RED = (255, 0, 0)
ORANGE = (255, 125, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COLORS = [RED, ORANGE]
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()

score = 0
level = 0

score_time = None
run = True


class Brick(pygame.sprite.Sprite):
        def __init__(self, x, y, level):
                pygame.sprite.Sprite.__init__(self)
                self.x = x
                self.y = y
                self.color = COLORS[level]
                self.image = pygame.Surface((50, 20))
                self.image.fill(self.color)
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.x, self.y)
                all_sprites.add(self)
                bricks.add(self)

        def update(self):
                global score
                if self.rect.colliderect(ball.rect):
                        ball.speedy *= -1
                        self.kill()
                        score += 1


class Ball(pygame.sprite.Sprite):
        def __init__(self):
                global score_time
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load("ball.png")
                self.image = pygame.transform.scale(self.image, (30, 30))
                self.rect = self.image.get_rect()
                self.rect.center = (WIDTH / 2, HEIGHT / 2)
                all_sprites.add(self)
                self.speedx = 8
                self.speedy = -8

        def update(self):
                global run
                self.rect.x += self.speedx
                self.rect.y += self.speedy
                if self.rect.right >= WIDTH or self.rect.left <= 0:
                        self.speedx *= -1

                if self.rect.top <= 0:
                        self.speedy *= -1

                if self.rect.y > HEIGHT + 50:
                        print("YOU LOSE!")
                        run = False

        def wait(self):
                pygame.time.wait(3000)


class Paddle(pygame.sprite.Sprite):
        def __init__(self):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.Surface((80, 20))
                self.image.fill((255, 255, 0))
                self.rect = self.image.get_rect()
                self.rect.center = (WIDTH / 2, HEIGHT - 50)
                self.speed = 0
                all_sprites.add(self)

        def update(self):

                self.rect.x += self.speed
                if self.rect.right >= WIDTH:
                        self.rect.right = WIDTH - 1
                if self.rect.left <= 0:
                        self.rect.left = 1

                if self.rect.top <= (ball.rect.bottom + 5) and ball.rect.left <= self.rect.right - 2 and ball.rect.right >= self.rect.left + 2:
                        ball.rect.y -= 10
                        ball.speedy *= -1


paddle = Paddle()
ball = Ball()
for column in range(7):
        brick = Brick(70 * column + 10, 30, level)


def wait():
        global score_time
        ball.rect.y = WIDTH / 3
        ball.rect.x = WIDTH / 2
        current_time = pygame.time.get_ticks()
        if current_time - score_time < 2100:
                ball.speedx = 0
                ball.speedy = 0
        else:
                ball.speedx = random.choice([-8, 8])
                ball.speedy = random.choice([-8, 8])
                score_time = None


while run:
        paddle.speed = 0
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
                paddle.speed = 12
        elif keys[pygame.K_LEFT]:
                paddle.speed = -12

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
        if len(bricks) == 0:

                level += 1
                score_time = pygame.time.get_ticks()
                wait()
                if level == len(COLORS):
                        run = False
                        print("YOU WIN!")
                        break

                else:
                        for row in range(level + 1):
                                for column in range(7):
                                        brick = Brick(70 * column + 10,
                                                      30 + (row * 30), row)

        if score_time:
                wait()

        screen.fill(BG_COLOR)
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.set_caption('Score: ' + str(score))
        pygame.display.flip()

pygame.quit()
