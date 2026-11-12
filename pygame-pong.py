import sys, pygame, random, time, os  # Import the libraries
pygame.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
size = width, height = 1280, 1024
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
font = pygame.font.Font(None,35)
score = [0, 0]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("explosive pong")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

def restart():
    score[0] = 0
    score[1] = 0
    firstplayer.rect.y = 462
    secondplayer.rect.y = 462
    sharik.reset(random.choice([True, False]))
    sharik.paused = True   # press P to serve, like at the start

class Player1:
    def __init__(self):
        self.image = pygame.image.load("paddle.png")
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 462
        self.outline = self.rect

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


class Player2:
    def __init__(self):
        self.image = pygame.image.load("paddle.png")
        self.rect = self.image.get_rect()
        self.rect.x = width - 80
        self.rect.y = 462
        self.outline = self.rect

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
        self.outline = self.rect
        self.paused = True
        left = True
        self.reset(left)

    def reset(self, side):
        self.rect.x = 590
        self.rect.y = 462
        self.pos = [float(self.rect.x), float(self.rect.y)]   # float position
        self.speed = self.BASE_SPEED
        if side: self.direction = [1 * self.speed, random.uniform(-1, 1)]
        else: self.direction = [-1 * self.speed, random.uniform(-1, 1)]

    def display(self):
        screen.blit(self.image, self.rect)

    def move(self):
        if not self.paused:
            self.pos[0] += self.direction[0]
            self.pos[1] += self.direction[1]
            self.rect.x = round(self.pos[0])
            self.rect.y = round(self.pos[1])

            if self.rect.left < 0:
                score[1] += 1
                # pygame.time.set_timer(pygame.USEREVENT+1, 3000, loops=1) # сделать кд после поинта / ИСПОЛЬЗОВАТЬ ФУНКЦИЮ ПАУЗЫ !!!
                self.paused = True
                left = True
                self.reset(left)
                return
            if self.rect.right > width:
                score[0] += 1
                # pygame.time.set_timer(pygame.USEREVENT+1, 3000, loops=1)
                self.paused = True
                left = False
                self.reset(left)
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
paused = False
pygame.time.set_timer(pygame.USEREVENT+1, 3000, loops=1)
while True:
    game_over = score[0] >= 5 or score[1] >= 5

    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    restart()
        winner = "Player 1" if score[0] >= 5 else "Player 2"
        screen.fill(white)
        text = font.render(f"{winner} wins! Press SPACE to play again, Q to quit", 1, black)
        screen.blit(text, text.get_rect(center=(width // 2, 124)))
        pygame.display.flip()

    elif not paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and sharik.paused:
                    sharik.paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    paused = True
        keystate = pygame.key.get_pressed()
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
        sharik.move()
        pygame.draw.rect(screen, white, firstplayer.outline, 2, 20)
        pygame.draw.rect(screen, white, secondplayer.outline, 2, 20)
        pygame.draw.rect(screen, red, sharik.outline, 2, 20)
        score_text = font.render(f"{score[0]} | {score[1]}", 1, white)
        screen.blit(score_text, (590, 124))
        pygame.display.flip()

    else:  # paused
        sharik.paused = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        screen.fill(white)
        pause_text = font.render("GAME IS PAUSED", 1, black)
        screen.blit(pause_text, (500, 124))
        pygame.display.flip()
