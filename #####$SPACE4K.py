#!/usr/bin/env python3
# O3 ALPHA SPACE INVADERS – Procedural Vibes Only (No PNGs)

import pygame
import random
import numpy as np

# Game settings
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 6
BULLET_SPEED = 8
ENEMY_SPEED = 1.2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('O3 Alpha Space Invaders')
clock = pygame.time.Clock()

# Procedural sound (pew pew!)
def beep(frequency=440, duration=0.05):
    sr = 44100
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    wave = (32767 * 0.5 * np.sin(2 * np.pi * frequency * t)).astype(np.int16)
    wave_stereo = np.column_stack((wave, wave))
    sound = pygame.sndarray.make_sound(wave_stereo)
    sound.play()

# Game objects
player = pygame.Rect(WIDTH//2-25, HEIGHT-50, 50, 30)
bullets = []
enemies = [pygame.Rect(x, y, 40, 30) for x in range(50, WIDTH-50, 60) for y in range(50, 200, 45)]
dir_x = ENEMY_SPEED

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += PLAYER_SPEED
    if keys[pygame.K_SPACE] and len(bullets) < 3:
        bullets.append(pygame.Rect(player.centerx-2, player.y, 4, 10))
        beep(880)

    # Bullet movement
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED
        if bullet.y < 0:
            bullets.remove(bullet)

    # Enemy movement
    move_down = False
    for enemy in enemies:
        enemy.x += dir_x
        if enemy.right >= WIDTH or enemy.left <= 0:
            move_down = True

    if move_down:
        dir_x = -dir_x
        for enemy in enemies:
            enemy.y += 15

    # Collision detection
    for enemy in enemies[:]:
        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                beep(440)

    # Drawing
    screen.fill((16, 16, 16))
    pygame.draw.rect(screen, (255, 255, 255), player)
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 100, 100), bullet)
    for enemy in enemies:
        pygame.draw.rect(screen, (100, 200, 255), enemy)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()