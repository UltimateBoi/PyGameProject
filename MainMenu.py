import pygame
from Utils import Button
from Settings import SettingsMenu

class MainMenu:
    def __init__(self, player_name, screen_width, screen_height):
        self.player_name = player_name
        self.background = pygame.image.load('assets/background.png')  # Load background image
        self.settings_icon = pygame.image.load('assets/settings_icon.png')  # Load settings icon image
        self.play_button = Button(0, 0, 0, 0, (0, 255, 0), "Play", border_radius=5)  # Initialize play button
        self.settings_menu = SettingsMenu(screen_width, screen_height)  # Initialize settings menu

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()  # Get current screen size
        background = pygame.transform.scale(self.background, (screen_width, screen_height))  # Scale background to fit screen
        screen.blit(background, (0, 0))  # Draw background
        
        font = pygame.font.SysFont(None, 36)
        name_text = font.render(self.player_name, True, (0, 0, 0))  # Render player's name
        text_rect = name_text.get_rect(topleft=(10, 10))  # Position for player's name
        
        # Draw border with border radius behind the player's username
        border_color = (255, 255, 255)  # White border
        border_radius = 10
        border_rect = text_rect.inflate(10, 10)  # Inflate to add padding around the text
        pygame.draw.rect(screen, border_color, border_rect, border_radius=border_radius)  # Draw white border
        
        # Draw black border around the white border
        black_border_rect = border_rect.inflate(4, 4)  # Slightly larger than the white border
        pygame.draw.rect(screen, (0, 0, 0), black_border_rect, 2, border_radius=border_radius)  # Draw black border
        
        screen.blit(name_text, text_rect.topleft)  # Draw player's name
        
        # Ensure the settings icon is always square
        icon_size = min(screen_width, screen_height) // 20  # Calculate icon size
        settings_icon = pygame.transform.scale(self.settings_icon, (icon_size, icon_size))  # Scale settings icon
        screen.blit(settings_icon, (10, 50))  # Draw settings icon
        
        # Draw main menu text "Tower Defence"
        title_font = pygame.font.SysFont(None, 72)
        title_text = title_font.render("Tower Defence", True, (0, 0, 0))  # Render title text
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))  # Position for title text
        screen.blit(title_text, title_rect.topleft)  # Draw title text
        
        play_button_width, play_button_height = screen_width // 5, screen_height // 10  # Calculate play button size
        self.play_button.rect = pygame.Rect((screen_width - play_button_width) // 2, screen_height - play_button_height - 50, play_button_width, play_button_height)  # Position play button
        self.play_button.draw(screen)  # Draw play button

        if self.settings_menu.visible:
            self.settings_menu.draw(screen)  # Draw settings menu if visible

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Check for left mouse button click
                if self.play_button and self.play_button.clicked(event.pos):  # Check if play button is clicked
                    return "map_selector"  # Return map selector screen
                settings_icon_rect = pygame.Rect(10, 50, self.settings_icon.get_width(), self.settings_icon.get_height())  # Get settings icon rect
                if settings_icon_rect.collidepoint(event.pos):  # Check if settings icon is clicked
                    self.settings_menu.toggle_visibility()  # Toggle settings menu visibility
        if self.settings_menu.visible:
            self.settings_menu.handle_events(event)  # Handle events for settings menu if visible
        return None  # Return None if no relevant events