import pygame
from typing import List, Tuple, Optional
from towers.tower import Tower

class TowerSidebar:
    def __init__(self, screen_width: int, screen_height: int):
        self.width = 200
        self.height = screen_height
        self.rect = pygame.Rect(screen_width - self.width, 0, self.width, self.height)
        self.tower_slots = []
        self.selected_tower: Optional[Tower] = None
        self.dragging_tower: Optional[Tower] = None
        self._initialize_tower_slots()

    def _initialize_tower_slots(self) -> None:
        slot_width = 80
        slot_height = 80
        padding = 10
        columns = 2
        rows = 8

        for row in range(rows):
            for col in range(columns):
                x = self.rect.x + padding + col * (slot_width + padding)
                y = self.rect.y + padding + row * (slot_height + padding)
                slot_rect = pygame.Rect(x, y, slot_width, slot_height)
                self.tower_slots.append(slot_rect)

    def draw(self, screen: pygame.Surface) -> None:
        # Draw sidebar background
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)

        # Draw tower slots
        for slot in self.tower_slots:
            pygame.draw.rect(screen, (150, 150, 150), slot)
            pygame.draw.rect(screen, (100, 100, 100), slot, 1)

        # Draw tower previews in slots
        for i, slot in enumerate(self.tower_slots):
            tower = Tower(slot.centerx, slot.centery)
            tower.image = pygame.transform.scale(tower.image, (60, 60))
            screen.blit(tower.image, tower.image.get_rect(center=slot.center))

        # Draw dragging tower if exists
        if self.dragging_tower:
            screen.blit(self.dragging_tower.image, self.dragging_tower.rect.topleft)

    def handle_mouse_down(self, pos: Tuple[int, int]) -> Optional[Tower]:
        # Check if clicking in a tower slot
        for i, slot in enumerate(self.tower_slots):
            if slot.collidepoint(pos):
                tower = Tower(slot.centerx, slot.centery)
                self.dragging_tower = tower
                return tower
        return None

    def handle_mouse_up(self, pos: Tuple[int, int]) -> Optional[Tower]:
        if self.dragging_tower:
            tower = self.dragging_tower
            self.dragging_tower = None
            return tower
        return None

    def update_drag(self, pos: Tuple[int, int]) -> None:
        if self.dragging_tower:
            self.dragging_tower.rect.center = pos 