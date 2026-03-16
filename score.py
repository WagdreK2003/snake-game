import pygame


class Score:

    def __init__(self):
        self.value = 0
        self.level = 1
        self.high_score = 0
        self.font = pygame.font.SysFont("Arial", 24, bold=True)

    def reset(self):
        self.high_score = max(self.high_score, self.value)
        self.value = 0
        self.level = 1

    def increase(self):
        self.value += 1
        if self.value % 5 == 0:
            self.level += 1

    def update_high_score(self):
        if self.value > self.high_score:
            self.high_score = self.value

    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.value}", True, (255, 255, 255))
        level_text = self.font.render(f"Level: {self.level}", True, (240, 240, 20))
        hi_text = self.font.render(f"High Score: {self.high_score}", True, (120, 255, 220))
        screen.blit(score_text, (12, 8))
        screen.blit(level_text, (220, 8))
        screen.blit(hi_text, (420, 8))
