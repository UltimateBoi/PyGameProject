import pygame
import math
from typing import Tuple

class Dart:
    def __init__(self, x: float, y: float, target: 'Bloon'):
        self.image = pygame.image.load('assets/dart.png')
        self.image = pygame.transform.scale(self.image, (20, 35))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.target = target
        self.dx, self.dy = self.calculate_velocity()
        self.rotation = math.degrees(math.atan2(-self.dy, self.dx))
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect(center=(x, y))
        self.active = True

    def calculate_velocity(self) -> Tuple[float, float]:
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            return dx / dist * self.speed, dy / dist * self.speed
        return 0, 0

    def move(self) -> None:
        if not self.active:
            return
            
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Check if dart is off screen
        screen = pygame.display.get_surface()
        if (self.rect.right < 0 or self.rect.left > screen.get_width() or
            self.rect.bottom < 0 or self.rect.top > screen.get_height()):
            self.active = False

    def draw(self, screen: pygame.Surface) -> None:
        if self.active:
            screen.blit(self.image, self.rect.topleft) 