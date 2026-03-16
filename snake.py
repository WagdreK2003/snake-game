import pygame
from settings import *


class Snake:

    def __init__(self):
        self.reset()

    def reset(self):
        start_x = WIDTH // 2
        start_y = PLAY_HEIGHT // 2
        self.body = [
            (start_x, start_y),
            (start_x - CELL_SIZE, start_y),
            (start_x - CELL_SIZE * 2, start_y),
        ]
        self.direction = (CELL_SIZE, 0)

    def get_head(self):
        return self.body[0]

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)

    def set_direction(self, new_direction):
        if (new_direction[0] == -self.direction[0] and new_direction[1] == -self.direction[1]):
            return
        self.direction = new_direction

    def collides_with_self(self):
        head = self.get_head()
        return head in self.body[1:]

    def is_out_of_bounds(self):
        x, y = self.get_head()
        return x < 0 or y < 0 or x >= WIDTH or y >= PLAY_HEIGHT

    def draw(self, screen):
        for i, segment in enumerate(self.body):
            x, y = segment
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            if i == 0:
                pygame.draw.rect(screen, (0, 255, 0), rect)
                pygame.draw.rect(screen, (0, 180, 0), rect, 2)
                eye_offset = CELL_SIZE // 4
                pygame.draw.circle(screen, (0, 0, 0), (x + eye_offset + 2, y + eye_offset), 3)
                pygame.draw.circle(screen, (0, 0, 0), (x + CELL_SIZE - eye_offset - 2, y + eye_offset), 3)
            else:
                pygame.draw.rect(screen, GREEN, rect)
                pygame.draw.rect(screen, (17, 128, 17), rect, 1)

