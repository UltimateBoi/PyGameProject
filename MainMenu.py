import pygame
import sys

class MainMenu:
    def __init__(self, player_name):
        self.player_name = player_name
        self.background = pygame.image.load('assets/background.png')
        self.settings_icon = pygame.image.load('assets/settings_icon.png')
        self.play_button = pygame.Rect(350, 500, 100, 50)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        font = pygame.font.SysFont(None, 36)
        name_text = font.render(self.player_name, True, (0, 0, 0))
        screen.blit(name_text, (10, 10))
        screen.blit(self.settings_icon, (10, 50))
        pygame.draw.rect(screen, (0, 255, 0), self.play_button)
        play_text = font.render("Play", True, (0, 0, 0))
        screen.blit(play_text, (self.play_button.x + 10, self.play_button.y + 10))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(event.pos):
                return "map_selector"
        return None
