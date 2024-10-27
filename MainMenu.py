import pygame
from Utils import Button
from Settings import SettingsMenu

class MainMenu:
    def __init__(self, player_name, screen_width, screen_height):
        self.player_name = player_name
        self.background = pygame.image.load('assets/background.png')
        self.settings_icon = pygame.image.load('assets/settings_icon.png')
        self.play_button = Button(0, 0, 0, 0, (0, 255, 0), "Play", border_radius=5)
        self.settings_menu = SettingsMenu(screen_width, screen_height)

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        background = pygame.transform.scale(self.background, (screen_width, screen_height))
        screen.blit(background, (0, 0))
        
        font = pygame.font.SysFont(None, 36)
        name_text = font.render(self.player_name, True, (0, 0, 0))
        text_rect = name_text.get_rect(topleft=(10, 10))
        
        # Draw border with border radius behind the player's username
        border_color = (255, 255, 255)  # White border
        border_radius = 10
        border_rect = text_rect.inflate(10, 10)  # Inflate to add padding around the text
        pygame.draw.rect(screen, border_color, border_rect, border_radius=border_radius)
        
        # Draw black border around the white border
        black_border_rect = border_rect.inflate(4, 4)  # Slightly larger than the white border
        pygame.draw.rect(screen, (0, 0, 0), black_border_rect, 2, border_radius=border_radius)
        
        screen.blit(name_text, text_rect.topleft)
        
        # Ensure the settings icon is always square
        icon_size = min(screen_width, screen_height) // 20
        settings_icon = pygame.transform.scale(self.settings_icon, (icon_size, icon_size))
        screen.blit(settings_icon, (10, 50))
        
        # Draw main menu text "Tower Defence"
        title_font = pygame.font.SysFont(None, 72)
        title_text = title_font.render("Tower Defence", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(title_text, title_rect.topleft)
        
        play_button_width, play_button_height = screen_width // 5, screen_height // 10
        self.play_button.rect = pygame.Rect((screen_width - play_button_width) // 2, screen_height - play_button_height - 50, play_button_width, play_button_height)
        self.play_button.draw(screen)

        if self.settings_menu.visible:
            self.settings_menu.draw(screen)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.play_button and self.play_button.clicked(event.pos):
                    return "map_selector"
                settings_icon_rect = pygame.Rect(10, 50, self.settings_icon.get_width(), self.settings_icon.get_height())
                if settings_icon_rect.collidepoint(event.pos):
                    self.settings_menu.toggle_visibility()
        if self.settings_menu.visible:
            self.settings_menu.handle_events(event)
        return None