import sys, pygame, random, time, os  # Import the libraries
pygame.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
size = width, height = 1280, 1024
black = 0, 0, 0
white = 255, 255, 255
font = pygame.font.Font(None,35)
score = [0, 0]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()



class Player1: # добавить края ракеткам, для хитбоксов + закруглить угла
    def __init__(self):
        self.image = pygame.image.load("paddle.png")
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 462

    def display(self):
        screen.blit(self.image, self.rect)

    def move(self, direction):
        if direction == "up":
            self.rect.y -= 1
        elif direction == "down":
            self.rect.y += 1
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height


class Player2: # добавить края ракеткам, для хитбоксов + закруглить угла
    def __init__(self):
        self.image = pygame.image.load("paddle.png")
        self.rect = self.image.get_rect()
        self.rect.x = width - 80
        self.rect.y = 462

    def display(self):
        screen.blit(self.image, self.rect)

    def move(self, direction):
        if direction == "up":
            self.rect.y -= 1
        elif direction == "down":
            self.rect.y += 1
        if self.rect.left < 0:
                    self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height

class ball:
    BASE_SPEED = 1      # horizontal speed at the start of each point
    MAX_SPEED = 1.5     # horizontal speed never goes above this
    SPEEDUP = 1.05      # speed multiplier per paddle hit
    MAX_VY = 1.2        # max vertical speed from the hit position
    RANDOMNESS = 0.3    # random extra vertical speed on each bounce

    def __init__(self):
        self.image = pygame.image.load("ball.png")
        self.rect = self.image.get_rect()
        self.alive = False
        self.reset()

    def reset(self):
        self.rect.x = 590
        self.rect.y = 462
        self.pos = [float(self.rect.x), float(self.rect.y)]   # float position
        self.speed = self.BASE_SPEED
        self.direction = [random.choice((-1, 1)) * self.speed,
                          random.uniform(-1, 1)]

    def display(self):
        screen.blit(self.image, self.rect)

    def move(self):
        self.pos[0] += self.direction[0]
        self.pos[1] += self.direction[1]
        self.rect.x = round(self.pos[0])
        self.rect.y = round(self.pos[1])

        if self.rect.left < 0:
            score[1] += 1
            pygame.time.set_timer(pygame.USEREVENT+1, 3000, loops=1) # сделать кд после поинта
            self.alive = False
            self.reset()
            return
        if self.rect.right > width:
            score[0] += 1
            pygame.time.set_timer(pygame.USEREVENT+1, 3000, loops=1)
            self.alive = False
            self.reset()
            return

        for paddle in (firstplayer.rect, secondplayer.rect):
            if self.rect.colliderect(paddle):
                from_left   = self.rect.right - paddle.left
                from_right  = paddle.right - self.rect.left
                from_top    = self.rect.bottom - paddle.top
                from_bottom = paddle.bottom - self.rect.top

                if min(from_left, from_right) < min(from_top, from_bottom):
                    # hit the front/back face: bounce back with a new angle
                    self.speed = min(self.speed * self.SPEEDUP, self.MAX_SPEED)

                    # -1 = top of paddle, 0 = middle, +1 = bottom
                    offset = (self.rect.centery - paddle.centery) / (paddle.height / 2)
                    offset = max(-1, min(1, offset))
                    new_vy = offset * self.MAX_VY + random.uniform(-self.RANDOMNESS, self.RANDOMNESS)

                    if from_left < from_right:
                        self.rect.right = paddle.left
                        self.direction[0] = -self.speed
                    else:
                        self.rect.left = paddle.right
                        self.direction[0] = self.speed
                    self.direction[1] = new_vy
                else:
                    # hit the top/bottom edge of the paddle
                    if from_top < from_bottom:
                        self.rect.bottom = paddle.top
                        self.direction[1] = -abs(self.direction[1])
                    else:
                        self.rect.top = paddle.bottom
                        self.direction[1] = abs(self.direction[1])

                # keep the float position in sync after pushing the ball out
                self.pos = [float(self.rect.x), float(self.rect.y)]

        if self.rect.top < 0:
            self.rect.top = 0
            self.direction[1] = abs(self.direction[1])
            self.pos[1] = float(self.rect.y)
        if self.rect.bottom > height:
            self.rect.bottom = height
            self.direction[1] = -abs(self.direction[1])
            self.pos[1] = float(self.rect.y)

firstplayer = Player1()
secondplayer = Player2()
sharik = ball()
pygame.time.set_timer(pygame.USEREVENT+1, 3000, loops=1)
while True:
    for event in pygame.event.get():                # Check if any system events have happened
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # elif event.type == pygame.USEREVENT+1:  # Used for timing - anything you put here will happen every four seconds.
        #     sharik.alive = True
    # clock.tick(500)
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_q]:
        pygame.quit()
        sys.exit()
    if keystate[pygame.K_w]:
        firstplayer.move("up")
    if keystate[pygame.K_s]:
        firstplayer.move("down")
    if keystate[pygame.K_UP]:
        secondplayer.move("up")
    if keystate[pygame.K_DOWN]:
        secondplayer.move("down")
    screen.fill(black)
    firstplayer.display()
    secondplayer.display()
    sharik.display()
    # while sharik.alive == True:
    #     sharik.move()
    sharik.move()
    score_image = font.render(f"{score[0]} | {score[1]}",1,(white))   # create an image which we can put on the "screen"
    score_rect = score_image.get_rect()                       # create a rect object for putting the message on the screen.
    score_rect.x = 590                                       # put the message somewhere sensible
    score_rect.y = 124
    screen.blit(score_image, score_rect)
    pygame.display.flip()