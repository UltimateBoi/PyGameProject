import pygame

class MapSelector:
    def __init__(self):
        self.background = pygame.image.load('assets/map_selector_background.png')
        self.map_thumbnails = [pygame.image.load(f'assets/map_{i}.png') for i in range(1, 4)]
        self.thumbnail_rects = [pygame.Rect(100 + i * 200, 200, 150, 150) for i in range(len(self.map_thumbnails))]
        self.next_button = pygame.Rect(700, 500, 100, 50)
        self.prev_button = pygame.Rect(50, 500, 100, 50)
        self.current_page = 0

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for i, thumbnail in enumerate(self.map_thumbnails):
            screen.blit(thumbnail, self.thumbnail_rects[i])
        pygame.draw.rect(screen, (0, 255, 0), self.next_button)
        pygame.draw.rect(screen, (0, 255, 0), self.prev_button)
        font = pygame.font.SysFont(None, 36)
        next_text = font.render("Next", True, (0, 0, 0))
        prev_text = font.render("Prev", True, (0, 0, 0))
        screen.blit(next_text, (self.next_button.x + 10, self.next_button.y + 10))
        screen.blit(prev_text, (self.prev_button.x + 10, self.prev_button.y + 10))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.next_button.collidepoint(event.pos):
                self.current_page += 1
            elif self.prev_button.collidepoint(event.pos):
                self.current_page -= 1
            else:
                for i, rect in enumerate(self.thumbnail_rects):
                    if rect.collidepoint(event.pos):
                        return f"map_{i + 1}"
        elif event.type == pygame.MOUSEWHEEL:
            self.current_page += event.y
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  # Left mouse button is held down
                self.current_page += event.rel[1] // 10  # Adjust the divisor for sensitivity
        return None
