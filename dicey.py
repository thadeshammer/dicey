import random
import sys
from dataclasses import dataclass

import pygame

screen_width, screen_height = 800, 600


def roll_dice(dice_count: int):
    return [random.randint(1, 6) for _ in range(dice_count)]


@dataclass
class DiceDrawDeets:
    size_percentage: float = 0.1  # 10% of screen height
    margin_percentage: float = 0.02  # 2% of screen height
    dice_count: int = 5

    @property
    def size(self):
        return int(screen_height * self.size_percentage)

    @property
    def margin(self):
        return int(screen_height * self.margin_percentage)

    @property
    def dice_per_row(self):
        return (screen_width - self.margin) // (self.size + self.margin)

    @property
    def total_width(self):
        max_dice_per_row = self.dice_per_row
        return max_dice_per_row * self.size + (max_dice_per_row - 1) * self.margin

    @property
    def x_start(self):
        return (screen_width - self.total_width) // 2

    @property
    def y_start(self):
        total_height = ((self.dice_count - 1) // self.dice_per_row + 1) * (
            self.size + self.margin
        )
        return screen_height - total_height


def draw_dice(screen, dice_values, dice_data):
    dice_per_row = dice_data.dice_per_row
    for i, value in enumerate(dice_values):
        row = i // dice_per_row
        col = i % dice_per_row
        dice_x = dice_data.x_start + col * (dice_data.size + dice_data.margin)
        dice_y = screen_height - (row + 1) * (dice_data.size + dice_data.margin)
        pygame.draw.rect(
            screen, (255, 255, 255), (dice_x, dice_y, dice_data.size, dice_data.size)
        )
        font = pygame.font.Font(
            None, int(dice_data.size * 0.6)
        )  # Adjust font size based on dice size
        text = font.render(str(value), True, (0, 0, 0))
        text_rect = text.get_rect(
            center=(dice_x + dice_data.size // 2, dice_y + dice_data.size // 2)
        )
        screen.blit(text, text_rect)


def main():
    global screen_width, screen_height
    pygame.init()

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Dice Rolling Game")
    clock = pygame.time.Clock()
    fps = 30

    dice_count = 5

    # Dice properties
    dice_data = DiceDrawDeets(dice_count=dice_count)

    # Initialize dice values
    dice_values = roll_dice(dice_count)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                dice_count = min(dice_count + 2, 30)
                dice_values = roll_dice(dice_count)
                dice_data = DiceDrawDeets(dice_count=dice_count)
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode(
                    (screen_width, screen_height), pygame.RESIZABLE
                )
                dice_data = DiceDrawDeets(dice_count=dice_count)

        screen.fill((0, 0, 0))
        draw_dice(screen, dice_values, dice_data)
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
