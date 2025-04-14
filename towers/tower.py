import pygame
import math
from typing import List, Tuple
from .dart import Dart

class Tower:
    def __init__(self, x: int, y: int):
        self.image = pygame.image.load('assets/tower.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.range = 100
        self.damage = 50
        self.cooldown = 30
        self.last_shot = 0
        self.level = 1
        self.cost = 50
        self.sell_value = int(self.cost * 0.7)  # 70% refund when selling
        self.upgrade_cost = int(self.cost * 1.5)  # 150% of base cost for upgrade
        self.is_selected = False
        self.dragging = False
        self.original_pos = (x, y)

    def upgrade(self) -> bool:
        if self.level < 3:  # Max level 3
            self.level += 1
            self.damage *= 1.5
            self.range *= 1.2
            self.cooldown = max(10, self.cooldown - 5)  # Minimum cooldown of 10
            self.upgrade_cost = int(self.upgrade_cost * 1.5)
            return True
        return False

    def sell(self) -> int:
        return self.sell_value

    def shoot(self, bloons: List['Bloon'], darts: List[Dart]) -> None:
        for bloon in bloons:
            dist = math.sqrt((bloon.rect.centerx - self.rect.centerx)**2 + 
                           (bloon.rect.centery - self.rect.centery)**2)
            if dist < self.range and self.last_shot >= self.cooldown:
                darts.append(Dart(self.rect.centerx, self.rect.centery, bloon))
                self.last_shot = 0
                break
        self.last_shot += 1

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect.topleft)
        if self.is_selected:
            # Draw range circle
            pygame.draw.circle(screen, (255, 255, 255, 128), self.rect.center, self.range, 1)
            # Draw upgrade/sell buttons
            self._draw_buttons(screen)

    def _draw_buttons(self, screen: pygame.Surface) -> None:
        font = pygame.font.SysFont(None, 24)
        if self.level < 3:
            upgrade_text = font.render(f"Upgrade (${self.upgrade_cost})", True, (0, 255, 0))
            screen.blit(upgrade_text, (self.rect.x, self.rect.y - 30))
        sell_text = font.render(f"Sell (${self.sell_value})", True, (255, 0, 0))
        screen.blit(sell_text, (self.rect.x, self.rect.y - 60))

    def handle_click(self, pos: Tuple[int, int]) -> str:
        if self.is_selected:
            # Check if upgrade button was clicked
            if self.level < 3:
                upgrade_rect = pygame.Rect(self.rect.x, self.rect.y - 30, 100, 20)
                if upgrade_rect.collidepoint(pos):
                    return "upgrade"
            # Check if sell button was clicked
            sell_rect = pygame.Rect(self.rect.x, self.rect.y - 60, 100, 20)
            if sell_rect.collidepoint(pos):
                return "sell"
        return ""

    def start_drag(self, pos: Tuple[int, int]) -> None:
        if self.rect.collidepoint(pos):
            self.dragging = True
            self.original_pos = self.rect.center

    def update_drag(self, pos: Tuple[int, int]) -> None:
        if self.dragging:
            self.rect.center = pos

    def end_drag(self) -> None:
        self.dragging = False 