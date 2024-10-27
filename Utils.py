import pygame

class Button:
    def __init__(self, x, y, width, height, color, text='', border_radius=0):
        self.rect = pygame.Rect(x, y, width, height)  # Define button rectangle
        self.color = color  # Button color
        self.text = text  # Button text
        self.border_radius = border_radius  # Border radius for rounded corners
        self.clicked_time = None  # Time when button was clicked
        self.animation_duration = 200  # Animation duration in milliseconds

    def draw(self, screen):
        if self.clicked_time:
            elapsed_time = pygame.time.get_ticks() - self.clicked_time  # Calculate elapsed time since click
            if elapsed_time < self.animation_duration:
                scale = 1 - 0.2 * (elapsed_time / self.animation_duration)  # Scale down
                if elapsed_time > self.animation_duration / 2:
                    scale = 0.8 + 0.2 * ((elapsed_time - self.animation_duration / 2) / (self.animation_duration / 2))  # Scale up
                new_width = int(self.rect.width * scale)  # New width based on scale
                new_height = int(self.rect.height * scale)  # New height based on scale
                self.rect.width = new_width  # Update width
                self.rect.height = new_height  # Update height
                self.rect.center = self.rect.center  # Keep center position
            else:
                self.rect = self.rect.copy()  # Reset rectangle
                self.clicked_time = None  # Reset click time

        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)  # Draw button
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=self.border_radius)  # Draw button border
        if self.text:
            font_size = int(32 * (screen.get_width() / 800))  # Adjust font size based on screen width
            font = pygame.font.Font(None, font_size)  # Create font
            text = font.render(self.text, True, (255, 255, 255))  # Render text
            text_rect = text.get_rect(center=self.rect.center)  # Center text
            screen.blit(text, text_rect)  # Draw text

    def clicked(self, pos):
        if self.rect.collidepoint(pos):  # Check if click is within button
            self.clicked_time = pygame.time.get_ticks()  # Record click time
            return True  # Return True if clicked
        return False  # Return False if not clicked

class Slider:
    def __init__(self, x, y, width, height, bg_color, fg_color, min_val, max_val, initial_val, border_radius=0):
        self.rect = pygame.Rect(x, y, width, height)  # Define slider rectangle
        self.bg_color = bg_color  # Background color
        self.fg_color = fg_color  # Foreground color
        self.min_val = min_val  # Minimum value
        self.max_val = max_val  # Maximum value
        self.value = initial_val  # Current value
        self.target_value = initial_val  # Target value for smooth animation
        self.border_radius = border_radius  # Border radius for rounded corners
        self.handle_radius = height // 2 + 5  # Handle radius
        self.handle_rect = pygame.Rect(x, y - 5, self.handle_radius * 2, self.handle_radius * 2)  # Handle rectangle
        self.dragging = False  # Initialize dragging state
        self.animation_speed = 0.1  # Animation speed for smooth value change
        self.update_handle_position()  # Update handle position based on initial value

    def update_handle_position(self):
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)  # Calculate ratio of current value
        self.handle_rect.centerx = self.rect.x + int(ratio * (self.rect.width))  # Update handle x position
        self.handle_rect.centery = self.rect.centery  # Align handle with slider bar

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=self.border_radius)  # Draw slider background
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=self.border_radius)  # Draw slider border

        filled_rect = pygame.Rect(self.rect.x, self.rect.y, self.handle_rect.centerx - self.rect.x, self.rect.height)  # Filled portion
        pygame.draw.rect(screen, self.fg_color, filled_rect, border_radius=self.border_radius)  # Draw filled portion

        pygame.draw.circle(screen, (11, 214, 250), self.handle_rect.center, self.handle_radius)  # Draw handle
        pygame.draw.circle(screen, (255, 255, 255), self.handle_rect.center, self.handle_radius, 2)  # Draw handle border

        padding = 0.5
        available_width = self.rect.width - self.handle_radius * 2 - padding * 2  # Available width for text
        font_size = int(self.rect.height * 1.5)  # Initial font size
        font = pygame.font.Font(None, font_size)  # Create font
        percentage_text = font.render(f"{int((self.value - self.min_val) / (self.max_val - self.min_val) * 100)}%", True, (0, 0, 0))  # Render percentage text
        
        while percentage_text.get_width() > available_width and font_size > 1:
            font_size -= 1  # Decrease font size to fit
            font = pygame.font.Font(None, font_size)  # Update font
            percentage_text = font.render(f"{int((self.value - self.min_val) / (self.max_val - self.min_val) * 100)}%", True, (0, 0, 0))  # Re-render text
        
        screen.blit(percentage_text, (self.rect.right + padding, self.rect.y + (self.rect.height - percentage_text.get_height()) // 2))  # Draw percentage text

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):  # Check if handle is clicked
                self.dragging = True  # Start dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False  # Stop dragging
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.target_value = self.min_val + (event.pos[0] - self.rect.x) / self.rect.width * (self.max_val - self.min_val)  # Update target value
                self.target_value = max(self.min_val, min(self.target_value, self.max_val))  # Clamp target value
        elif event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):  # Check if mouse is over slider
                self.target_value += event.y * (self.max_val - self.min_val) / 100  # Adjust target value with mouse wheel
                self.target_value = max(self.min_val, min(self.target_value, self.max_val))  # Clamp target value

    def update(self):
        if self.value != self.target_value:
            self.value += (self.target_value - self.value) * self.animation_speed  # Smoothly update value
            if abs(self.target_value - self.value) < 0.01:
                self.value = self.target_value  # Snap to target value if close enough
            self.update_handle_position()  # Update handle position
