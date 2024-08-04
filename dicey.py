import random
import sys
from dataclasses import dataclass

import pygame

screen_width, screen_height = 800, 600


@dataclass
class PlayerState:
    energy: int = 0
    fury_points: int = 0


def roll_dice(dice_count: int, player_state: PlayerState):
    dice_values = []
    temporary_dice = []
    for _ in range(dice_count):
        value = random.randint(1, 6)
        dice_values.append(value)
        if value == 1:
            player_state.fury_points += 1
        elif value in {2, 3}:
            player_state.energy += 1
        elif value in {4, 5}:
            player_state.energy += 1
            temporary_dice.extend(handle_blow_up(player_state))
        elif value == 6:
            player_state.energy += 1
            temporary_dice.extend(handle_blow_up(player_state))
    return dice_values, temporary_dice


def handle_blow_up(player_state: PlayerState):
    temp_dice = []
    value = random.randint(1, 6)
    temp_dice.append(value)
    if value in {2, 3}:
        player_state.energy += 1
    elif value in {4, 5}:
        player_state.energy += 1
        temp_dice.extend(handle_blow_up(player_state))
    elif value == 1:
        player_state.fury_points += 1
    elif value == 6:
        player_state.energy += 1
        temp_dice.extend(handle_blow_up(player_state))
    return temp_dice


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


def draw_dice(screen, dice_values, dice_data, temp_dice_values):
    draw_individual_dice(
        screen, dice_values, dice_data, (255, 255, 255)
    )  # White for regular dice
    draw_individual_dice(
        screen, temp_dice_values, dice_data, (173, 216, 230)
    )  # Light blue for temporary dice


def draw_individual_dice(screen, dice_values, dice_data, color):
    dice_per_row = dice_data.dice_per_row
    for i, value in enumerate(dice_values):
        row = i // dice_per_row
        col = i % dice_per_row
        dice_x = dice_data.x_start + col * (dice_data.size + dice_data.margin)
        dice_y = screen_height - (row + 1) * (dice_data.size + dice_data.margin)
        pygame.draw.rect(
            screen, color, (dice_x, dice_y, dice_data.size, dice_data.size)
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
    player_state = PlayerState()

    # Dice properties
    dice_data = DiceDrawDeets(dice_count=dice_count)

    # Initialize dice values
    dice_values, temp_dice_values = roll_dice(dice_count, player_state)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                dice_count = min(dice_count + 2, 30)
                dice_values, temp_dice_values = roll_dice(dice_count, player_state)
                dice_data = DiceDrawDeets(dice_count=dice_count)
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode(
                    (screen_width, screen_height), pygame.RESIZABLE
                )
                dice_data = DiceDrawDeets(dice_count=dice_count)

        screen.fill((0, 0, 0))
        draw_dice(screen, dice_values, dice_data, temp_dice_values)
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
