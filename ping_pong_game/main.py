import pygame
import random

pygame.init()
WIDTH, HEIGHT = 800 , 600
BALL_SPEED = 7 # سرعت توپ
PADDLE_SPEED = 7 # سرعت دسته ها
# رنگ ها
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
# امتیاز بازیکن اول و دوم
score1 = 0
score2 = 0
# نام بازیکن های اول و دوم
player1_name = "A"
player2_name = "B"
# موقعیت توپ و دسته ها
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
paddle1 = pygame.Rect(50, HEIGHT // 2 - 60, 10, 120)
paddle2 = pygame.Rect(WIDTH - 60, HEIGHT // 2 -60, 10, 120)
# موقعیت توپ هنگام شروع بازی بطور شانسی به چپ بره یا راست بره
ball_dx = BALL_SPEED * random.choice((1, -1))
ball_dy = BALL_SPEED * random.choice((1, -1))
# دسته یک و دو
paddle1_dy = 0
paddle2_dy = 0
# حرکت توپ
ball_in_motion = True
# صفحه نمایش و تایتل
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# موقعیت نمایش امتیاز ها
def draw_scores():
    font = pygame.font.Font(None, 36)
    score1_text = font.render(f"{player1_name}: {score1}", True, GREEN)
    score2_text = font.render(f"{player2_name}: {score2}", True, GREEN)
    screen.blit(score1_text, (10, 10))
    screen.blit(score2_text, (WIDTH - score2_text.get_width() -10 , 10))

# برسی برخورد توپ با دسته ها
def check_collision(ball, paddle):
    if ball.colliderect(paddle):
        return True
    return False

# موقعیت توپ بعداز شکست یک بازیکن
def reset_ball_position():
    side = random.choice(('left', 'right'))
    if side == 'left':
        ball.x = 10 + 50 + 10
        ball_dx = BALL_SPEED
    else:
        ball.x = WIDTH - 50 -10 - 30 - 10
        ball_dx = -BALL_SPEED
    ball.y = HEIGHT // 2 - 15
    return ball_dx


running = True
while running:
    for event in pygame.event.get():
        # اگر ضرب در رو بزنه بازی بسته میشه
        if event.type == pygame.QUIT:
            running = False
        # دکمه های بالا و پایین رو بزنه حرکت میکنه
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                paddle2_dy = -PADDLE_SPEED
            elif event.key == pygame.K_DOWN:
                paddle2_dy = PADDLE_SPEED
            # اگه اسپیس بزنه بازی شروع میشه
            elif event.key == pygame.K_SPACE:
                ball_in_motion = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                paddle2_dy = 0
    # همون دکمه ها برای بازیکن اول
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1_dy = -PADDLE_SPEED
    elif keys[pygame.K_s]:
        paddle1_dy = PADDLE_SPEED
    else:
        paddle1_dy = 0
    # حرکت توپ
    if ball_in_motion:
        ball.x += ball_dx
        ball.y += ball_dy
    # اگه توپ به بالا و پایین بخوره در خلاف جهت برگرده
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1
    # اگه توپ به دسته ها بخوره در خلاف جهت برگرده
    if check_collision(ball, paddle1) or check_collision(ball, paddle2):
        ball_dx *= -1
    # اگه توپ از چپ و راست رد شه امتیاز ثبت شه
    if ball.left <= 0:
        score2 += 1
        if score2 == 5:
            running = False
        else:
            ball_dx = reset_ball_position()
            ball_in_motion = False
    elif ball.right >= WIDTH:
        score1 += 1
        if score1 == 5:
            running = False
        else:
            ball_dx = reset_ball_position()
            ball_in_motion = False

    paddle1.y += paddle1_dy
    paddle2.y += paddle2_dy

    # دسته ها از بالا و پایین خارج نشن
    if paddle1.top <= 0:
        paddle1.top = 0
    if paddle1.bottom >= HEIGHT:
        paddle1.bottom = HEIGHT
    if paddle2.top <= 0:
        paddle2.top = 0
    if paddle2.bottom >= HEIGHT:
        paddle2.bottom = HEIGHT
    # رنگ بکگراند
    screen.fill(BLACK)
    # رسم همه المان های بازی
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, RED, ball)

    draw_scores()

    pygame.display.flip()

    pygame.time.delay(30)


pygame.quit()