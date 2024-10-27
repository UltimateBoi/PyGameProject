import pygame
from Utils import Slider

class SettingsMenu:
    def __init__(self, screen_width, screen_height):
        self.visible = False
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect = pygame.Rect(0, 0, 320, 260)  # Increased height to add more space
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.animation_start_time = None
        self.animation_duration = 300

        # Initialize sliders with relative positions
        self.master_volume_slider = Slider(self.rect.x + 20, self.rect.y + 60, 240, 20, (56, 32, 15), (129, 254, 7), 0, 100, 50, 5)
        self.music_volume_slider = Slider(self.rect.x + 20, self.rect.y + 130, 240, 20, (56, 32, 15), (129, 254, 7), 0, 100, 50, 5)
        self.fx_volume_slider = Slider(self.rect.x + 20, self.rect.y + 200, 240, 20, (56, 32, 15), (129, 254, 7), 0, 100, 50, 5)

    def toggle_visibility(self):
        self.visible = not self.visible
        if self.visible:
            self.animation_start_time = pygame.time.get_ticks()

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        if self.animation_start_time:
            elapsed_time = pygame.time.get_ticks() - self.animation_start_time
            if elapsed_time < self.animation_duration:
                scale = elapsed_time / self.animation_duration
                new_rect = self.rect.inflate(self.rect.width * (scale - 1), self.rect.height * (scale - 1))
                new_rect.center = (screen_width // 2, screen_height // 2)  # Center relative to the current window size
                self._draw_elements(screen, new_rect, scale)
            else:
                self.animation_start_time = None
                self.rect.center = (screen_width // 2, screen_height // 2)  # Center relative to the current window size
                self._draw_elements(screen, self.rect, 1)
        else:
            self.rect.center = (screen_width // 2, screen_height // 2)  # Center relative to the current window size
            self._draw_elements(screen, self.rect, 1)

    def _draw_elements(self, screen, rect, scale):
        pygame.draw.rect(screen, (0, 0, 0), rect, border_radius=10)
        pygame.draw.rect(screen, (188, 147, 90), rect.inflate(-4, -4), border_radius=10)

        font = pygame.font.SysFont(None, int(36 * scale))
        master_text = font.render("Master Volume", True, (0, 0, 0))
        music_text = font.render("Music Volume", True, (0, 0, 0))
        fx_text = font.render("FX Volume", True, (0, 0, 0))

        # Calculate positions based on the current scale
        master_text_pos = (rect.x + 20 * scale, rect.y + 20 * scale)
        music_text_pos = (rect.x + 20 * scale, rect.y + 90 * scale)
        fx_text_pos = (rect.x + 20 * scale, rect.y + 160 * scale)

        screen.blit(master_text, master_text_pos)
        screen.blit(music_text, music_text_pos)
        screen.blit(fx_text, fx_text_pos)

        # Draw slider backgrounds
        slider_bg_rect = pygame.Rect(rect.x + 10 * scale, rect.y + 50 * scale, rect.width - 20 * scale, 40 * scale)
        pygame.draw.rect(screen, (132, 101, 52), slider_bg_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), slider_bg_rect, 2, border_radius=10)

        slider_bg_rect.y += 70 * scale
        pygame.draw.rect(screen, (132, 101, 52), slider_bg_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), slider_bg_rect, 2, border_radius=10)

        slider_bg_rect.y += 70 * scale
        pygame.draw.rect(screen, (132, 101, 52), slider_bg_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), slider_bg_rect, 2, border_radius=10)

        # Update slider positions based on the current scale
        self.master_volume_slider.rect.topleft = (rect.x + 20 * scale, rect.y + 60 * scale)
        self.music_volume_slider.rect.topleft = (rect.x + 20 * scale, rect.y + 130 * scale)
        self.fx_volume_slider.rect.topleft = (rect.x + 20 * scale, rect.y + 200 * scale)

        # Update slider sizes based on the current scale
        self.master_volume_slider.rect.width = 240 * scale
        self.music_volume_slider.rect.width = 240 * scale
        self.fx_volume_slider.rect.width = 240 * scale

        # Update slider handle sizes based on the current scale
        self.master_volume_slider.handle_radius = int((20 // 2 + 5) * scale)
        self.music_volume_slider.handle_radius = int((20 // 2 + 5) * scale)
        self.fx_volume_slider.handle_radius = int((20 // 2 + 5) * scale)

        self.master_volume_slider.update_handle_position()
        self.music_volume_slider.update_handle_position()
        self.fx_volume_slider.update_handle_position()

        self.master_volume_slider.draw(screen)
        self.music_volume_slider.draw(screen)
        self.fx_volume_slider.draw(screen)

    def handle_events(self, event):
        self.master_volume_slider.handle_event(event)
        self.music_volume_slider.handle_event(event)
        self.fx_volume_slider.handle_event(event)

    def update(self):
        self.master_volume_slider.update()
        self.music_volume_slider.update()
        self.fx_volume_slider.update()