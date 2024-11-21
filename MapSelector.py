import pygame
from Utils import Button

class MapSelector:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = pygame.image.load('assets/map_selector_background.png')
        self.map_thumbnails = [pygame.image.load(f'assets/map_{i}.png') for i in range(1, 5)]
        self.update_layout()
        self.current_page = 0

    def update_layout(self):
        self.thumbnail_size = self.calculate_thumbnail_size()
        self.thumbnail_rects = self.calculate_thumbnail_positions()
        self.next_button = pygame.Rect(self.screen_width - 150, self.screen_height - 100, 100, 50)
        self.prev_button = pygame.Rect(50, self.screen_height - 100, 100, 50)
        self.back_button = pygame.Rect(50, 50, 100, 50)

    def calculate_thumbnail_size(self):
        grid_width = self.screen_width * 0.8
        grid_height = self.screen_height * 0.6
        thumbnail_width = grid_width // 4
        thumbnail_height = grid_height // 2
        return (thumbnail_width, thumbnail_height)

    def calculate_thumbnail_positions(self):
        positions = []
        start_x = (self.screen_width - (self.thumbnail_size[0] * 4)) // 2
        start_y = (self.screen_height - (self.thumbnail_size[1] * 2)) // 2
        for row in range(2):
            for col in range(4):
                x = start_x + col * self.thumbnail_size[0]
                y = start_y + row * self.thumbnail_size[1]
                positions.append(pygame.Rect(x, y, self.thumbnail_size[0], self.thumbnail_size[1]))
        return positions

    def draw(self, screen):
        self.screen_width, self.screen_height = screen.get_size()
        self.update_layout()
        background_resized = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        screen.blit(background_resized, (0, 0))
        
        for i, thumbnail in enumerate(self.map_thumbnails):
            resized_thumbnail = pygame.transform.scale(thumbnail, self.thumbnail_size)
            screen.blit(resized_thumbnail, self.thumbnail_rects[i])
        
        self.next_button = Button(self.screen_width - 150, self.screen_height - 100, 100, 50, (0, 255, 0), "Next", border_radius=5)
        self.prev_button = Button(50, self.screen_height - 100, 100, 50, (0, 255, 0), "Prev", border_radius=5)
        self.back_button = Button(50, 50, 100, 50, (255, 0, 0), "Back", border_radius=5)
        
        self.next_button.draw(screen)
        self.prev_button.draw(screen)
        self.back_button.draw(screen)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.next_button.clicked(event.pos):
                self.current_page += 1
            elif self.prev_button.clicked(event.pos):
                self.current_page -= 1
            elif self.back_button.clicked(event.pos):
                return "main_menu"
            else:
                for i, rect in enumerate(self.thumbnail_rects):
                    if rect.collidepoint(event.pos):
                        return f"map_{i + 1}"
        elif event.type == pygame.MOUSEWHEEL:
            self.current_page += event.y
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                self.current_page += event.rel[1] // 10
        elif event.type == pygame.VIDEORESIZE:
            self.screen_width, self.screen_height = event.size
            self.update_layout()
        return None