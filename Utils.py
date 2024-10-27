import pygame

class Button:
    def __init__(self, x, y, width, height, color, text='', border_radius=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.border_radius = border_radius
        self.clicked_time = None
        self.animation_duration = 200  # Animation duration in milliseconds

    def draw(self, screen):
        if self.clicked_time:
            elapsed_time = pygame.time.get_ticks() - self.clicked_time
            if elapsed_time < self.animation_duration:
                scale = 1 - 0.2 * (elapsed_time / self.animation_duration)
                if elapsed_time > self.animation_duration / 2:
                    scale = 0.8 + 0.2 * ((elapsed_time - self.animation_duration / 2) / (self.animation_duration / 2))
                new_width = int(self.rect.width * scale)
                new_height = int(self.rect.height * scale)
                self.rect.width = new_width
                self.rect.height = new_height
                self.rect.center = self.rect.center
            else:
                self.rect = self.rect.copy()
                self.clicked_time = None

        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=self.border_radius)
        if self.text:
            font_size = int(32 * (screen.get_width() / 800))
            font = pygame.font.Font(None, font_size)
            text = font.render(self.text, True, (255, 255, 255))
            text_rect = text.get_rect(center=self.rect.center)
            screen.blit(text, text_rect)

    def clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.clicked_time = pygame.time.get_ticks()
            return True
        return False

class Slider:
    def __init__(self, x, y, width, height, bg_color, fg_color, min_val, max_val, initial_val, border_radius=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.target_value = initial_val
        self.border_radius = border_radius
        self.handle_radius = height // 2 + 5  # Make the handle slightly larger than the slider height
        self.handle_rect = pygame.Rect(x, y - 5, self.handle_radius * 2, self.handle_radius * 2)
        self.dragging = False  # Initialize the dragging attribute
        self.animation_speed = 0.1  # Adjust this value for smoother or faster animation
        self.update_handle_position()

    def update_handle_position(self):
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.handle_rect.centerx = self.rect.x + int(ratio * (self.rect.width))
        self.handle_rect.centery = self.rect.centery  # Align the handle with the slider bar

    def draw(self, screen):
        # Draw the slider background with border radius
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=self.border_radius)

        # Draw the filled portion of the slider
        filled_rect = pygame.Rect(self.rect.x, self.rect.y, self.handle_rect.centerx - self.rect.x, self.rect.height)
        pygame.draw.rect(screen, self.fg_color, filled_rect, border_radius=self.border_radius)

        # Draw the handle as a circle with border
        pygame.draw.circle(screen, (11, 214, 250), self.handle_rect.center, self.handle_radius)  # Handle color
        pygame.draw.circle(screen, (255, 255, 255), self.handle_rect.center, self.handle_radius, 2)  # Handle border

        # Draw the percentage value
        padding = 0.5
        available_width = self.rect.width - self.handle_radius * 2 - padding * 2
        font_size = int(self.rect.height * 1.5)  # Increase the initial font size slightly
        font = pygame.font.Font(None, font_size)
        percentage_text = font.render(f"{int((self.value - self.min_val) / (self.max_val - self.min_val) * 100)}%", True, (0, 0, 0))
        
        # Adjust font size to fit within the available width
        while percentage_text.get_width() > available_width and font_size > 1:
            font_size -= 1
            font = pygame.font.Font(None, font_size)
            percentage_text = font.render(f"{int((self.value - self.min_val) / (self.max_val - self.min_val) * 100)}%", True, (0, 0, 0))
        
        screen.blit(percentage_text, (self.rect.right + padding, self.rect.y + (self.rect.height - percentage_text.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.target_value = self.min_val + (event.pos[0] - self.rect.x) / self.rect.width * (self.max_val - self.min_val)
                self.target_value = max(self.min_val, min(self.target_value, self.max_val))
        elif event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.target_value += event.y * (self.max_val - self.min_val) / 100  # Adjust precision as needed
                self.target_value = max(self.min_val, min(self.target_value, self.max_val))

    def update(self):
        if self.value != self.target_value:
            self.value += (self.target_value - self.value) * self.animation_speed
            if abs(self.target_value - self.value) < 0.01:
                self.value = self.target_value
            self.update_handle_position()