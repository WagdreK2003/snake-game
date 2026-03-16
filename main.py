import os
import sys
import random
import pygame

from settings import *
from snake import Snake
from score import Score

pygame.init()
pygame.display.set_caption("Snake Fiesta - Fun UI Edition")
icon = pygame.Surface((32, 32), pygame.SRCALPHA)
pygame.draw.circle(icon, (0, 255, 100), (16, 16), 15)
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

FONT_TITLE = pygame.font.SysFont("Verdana", 42, bold=True)
FONT_BODY = pygame.font.SysFont("Verdana", 24, bold=True)
FONT_SM = pygame.font.SysFont("Verdana", 20)

GRID_COLS = WIDTH // CELL_SIZE
GRID_ROWS = PLAY_HEIGHT // CELL_SIZE


def draw_grid(surface):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(surface, (30, 30, 30), (x, 0), (x, PLAY_HEIGHT))
    for y in range(0, PLAY_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, (30, 30, 30), (0, y), (WIDTH, y))


def draw_background(surface):
    for y in range(PLAY_HEIGHT):
        color_val = int(20 + 120 * (y / PLAY_HEIGHT))
        pygame.draw.line(surface, (10, color_val, min(color_val + 80, 255)), (0, y), (WIDTH, y))


def place_food(snake):
    while True:
        col = random.randrange(GRID_COLS)
        row = random.randrange(GRID_ROWS)
        pos = (col * CELL_SIZE, row * CELL_SIZE)
        if pos not in snake.body:
            return pos


def draw_food(surface, location):
    fx, fy = location
    rect = pygame.Rect(fx, fy, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, RED, rect, border_radius=8)
    pygame.draw.circle(surface, (255, 150, 50), (fx + CELL_SIZE // 2, fy + CELL_SIZE // 2), CELL_SIZE // 3)


def show_overlay(surface, title, lines):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    title_surf = FONT_TITLE.render(title, True, (255, 250, 220))
    title_rect = title_surf.get_rect(center=(WIDTH // 2, PLAY_HEIGHT // 2 - 80))
    surface.blit(title_surf, title_rect)

    for i, line in enumerate(lines):
        text_surf = FONT_BODY.render(line, True, (220, 220, 255))
        text_rect = text_surf.get_rect(center=(WIDTH // 2, PLAY_HEIGHT // 2 - 20 + i * 32))
        surface.blit(text_surf, text_rect)


def run_game():
    snake = Snake()
    score = Score()
    food = place_food(snake)

    state = "menu"
    frame_timer = 0

    while True:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if state == "menu":
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        state = "playing"
                        snake.reset()
                        score.reset()
                        food = place_food(snake)

                elif state == "playing":
                    if event.key in (pygame.K_UP, pygame.K_w):
                        snake.set_direction((0, -CELL_SIZE))
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        snake.set_direction((0, CELL_SIZE))
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        snake.set_direction((-CELL_SIZE, 0))
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        snake.set_direction((CELL_SIZE, 0))
                    elif event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        state = "paused"

                elif state == "paused":
                    if event.key in (pygame.K_p, pygame.K_ESCAPE, pygame.K_RETURN):
                        state = "playing"

                elif state == "game_over":
                    if event.key in (pygame.K_r, pygame.K_RETURN):
                        state = "playing"
                        snake.reset()
                        score.reset()
                        food = place_food(snake)
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        if state == "playing":
            speed_ms = max(45, 140 - (score.level - 1) * 8)
            frame_timer += dt
            if frame_timer >= speed_ms:
                frame_timer = 0
                snake.move()

                if snake.get_head() == food:
                    snake.grow()
                    score.increase()
                    score.update_high_score()
                    food = place_food(snake)

                if snake.collides_with_self() or snake.is_out_of_bounds():
                    state = "game_over"

        draw_background(screen)
        draw_grid(screen)
        snake.draw(screen)
        draw_food(screen, food)

        pygame.draw.rect(screen, GRAY, (0, PLAY_HEIGHT, WIDTH, UI_HEIGHT))
        score.draw(screen)

        if state == "menu":
            show_overlay(screen, "Snake Fiesta", ["Press ENTER / SPACE to start", "Arrow/WASD to move", "P to pause"])

        elif state == "paused":
            show_overlay(screen, "Paused", ["Press P/Esc/Enter to resume", "Press R to restart"])

        elif state == "game_over":
            show_overlay(screen, "Game Over!", [f"Your score: {score.value}", f"Best: {score.high_score}", "Press R/Enter to retry or Esc to quit"])

        pygame.display.flip()


if __name__ == "__main__":
    run_game()
