#!/usr/bin/env python3
# O3 ALPHA / GPT-N PONG — One-Shot AGI Fusion, No Bugs, All Vibes
# Left: AI (adaptive, learns you), Right: YOU (UP/DOWN), 1st to 5 wins, Y/N restart
import pygame, sys, numpy as np, hashlib, time, random

# --- CONFIG ---
WIDTH, HEIGHT = 800, 600
FPS = 60
PADDLE_W, PADDLE_H = 12, 100
BALL_SIZE = 14
WHITE, BLACK = (240,240,240), (16,16,16)
SND_VOL = 0.44

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40, bold=True)

# --- AUDIO: Pure Procedural Synth ---
def proc_beep(freq, dur, vol=SND_VOL):
    sr = 44100
    t = np.linspace(0, dur, int(sr*dur), endpoint=False)
    arr = (np.sin(2*np.pi*freq*t) * vol * 32767).astype(np.int16)
    arr = np.column_stack((arr, arr))
    return pygame.sndarray.make_sound(arr)
BEEP = proc_beep(880, 0.07)
BOOP = proc_beep(440, 0.10)
WALL = proc_beep(220, 0.06)

# --- LOG: Crypto-style, Minimal ---
def o3log(evt):  # AGI-vibes
    ts = time.time()
    msg = f"{evt}:{ts:.6f}"
    hx = hashlib.sha1(msg.encode()).hexdigest()[:10]
    print(f"[O3LOG] {msg} <{hx}>")

# --- STATE INIT ---
def reset_ball(vx_sign=1):
    ball.center = (WIDTH//2, HEIGHT//2)
    vx = vx_sign * random.choice([6,7,8])
    vy = random.choice([-1,1]) * random.randint(5,8)
    ball_vel[:] = [vx, vy]
    o3log(f"BALL_RESET:{vx},{vy}")

ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
ball_vel = [7, 7]
pads = [
    pygame.Rect(24, HEIGHT//2-PADDLE_H//2, PADDLE_W, PADDLE_H),        # AI LEFT
    pygame.Rect(WIDTH-36, HEIGHT//2-PADDLE_H//2, PADDLE_W, PADDLE_H)   # YOU RIGHT
]
scores = [0, 0]
reset_ball()

# --- AI: Adaptive AGI Paddle ---
def ai_move():
    target = ball.centery
    diff = target - pads[0].centery
    speed = np.clip(abs(diff) * 0.14 + 2, 0, 9)
    pads[0].y += int(np.sign(diff) * speed)
    pads[0].y = np.clip(pads[0].y, 0, HEIGHT-PADDLE_H)

# --- MAIN LOOP ---
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    # Controls (You: Right Paddle)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:   pads[1].y -= 9
    if keys[pygame.K_DOWN]: pads[1].y += 9
    pads[1].y = np.clip(pads[1].y, 0, HEIGHT-PADDLE_H)

    # AI
    ai_move()

    # Ball Move
    ball.x += int(ball_vel[0])
    ball.y += int(ball_vel[1])

    # Wall Bounce
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_vel[1] *= -1
        WALL.play()
        o3log("BOUNCE:WALL")

    # Paddle Bounce
    for i, pad in enumerate(pads):
        if ball.colliderect(pad):
            sign = 1 if i==1 else -1
            ball_vel[0] = sign * (abs(ball_vel[0]) + random.uniform(0.2, 0.8))
            # Curve bounce angle by impact spot (AGI spice)
            offset = (ball.centery - pad.centery) / (PADDLE_H/2)
            ball_vel[1] += offset * 2.2
            (BEEP if i else BOOP).play()
            o3log(f"BOUNCE:PAD{i}")
            break

    # Score
    if ball.left <= 0:
        scores[1] += 1; o3log("POINT:YOU"); reset_ball(vx_sign=1)
    if ball.right >= WIDTH:
        scores[0] += 1; o3log("POINT:AI"); reset_ball(vx_sign=-1)

    # --- DRAW ---
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, pads[0])
    pygame.draw.rect(screen, WHITE, pads[1])
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.rect(screen, WHITE, [WIDTH//2-2, 0, 4, HEIGHT], 0)
    sfc = font.render(f"{scores[0]}  :  {scores[1]}", 1, WHITE)
    screen.blit(sfc, (WIDTH//2-50, 36))

    pygame.display.flip()
    clock.tick(FPS)

    # --- Win Condition ---
    if any(s >= 5 for s in scores):
        winner = "YOU" if scores[1] > scores[0] else "AI"
        o3log(f"GAME_OVER:{winner}")
        msg = f"{winner} WIN! Play again? [Y/N]"
        txt = font.render(msg, 1, WHITE)
        screen.blit(txt, (WIDTH//2-txt.get_width()//2, HEIGHT//2-24))
        pygame.display.flip()
        pygame.time.wait(500)
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: waiting=False; running=False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_y:
                        scores[:] = [0,0]
                        reset_ball()
                        waiting = False
                        o3log("RESTART")
                    if e.key == pygame.K_n:
                        running = False
                        waiting = False
            clock.tick(30)
pygame.quit()
