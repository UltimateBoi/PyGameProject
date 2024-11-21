import pygame
import math
from MainMenu import MainMenu
from MapSelector import MapSelector

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)  # Create a resizable screen
pygame.display.set_caption("Tower Defense Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Load images (add images in your assets folder, replace "bloon.png" and "tower.png")
bloon_img = pygame.image.load('assets/bloon.png')
tower_img = pygame.image.load('assets/tower.png')
background_img = pygame.image.load('assets/background.png')

# Resize tower image
tower_img = pygame.transform.scale(tower_img, (80, 80))  # Resize tower image

# FPS and clock
FPS = 60
clock = pygame.time.Clock()  # Create a clock object to manage FPS

# Bloon Class (Enemy)
class Bloon:
    def __init__(self, path):
        self.image = bloon_img
        self.rect = self.image.get_rect()
        self.rect.center = path[0]
        self.path = path
        self.speed = 2
        self.path_pos = 0
        self.health = 100
    
    def move(self):
        # Move the bloon along the path
        if self.path_pos < len(self.path) - 1:
            target_x, target_y = self.path[self.path_pos + 1]
            dx, dy = target_x - self.rect.centerx, target_y - self.rect.centery
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 0:
                dx, dy = dx / dist, dy / dist
                self.rect.centerx += dx * self.speed
                self.rect.centery += dy * self.speed

            # Check if close to next point
            if dist < 5:
                self.path_pos += 1

    def draw(self):
        screen.blit(self.image, self.rect.topleft)  # Draw the bloon on the screen

# Dart Class (Projectile)
dart_img = pygame.image.load('assets/dart.png')
dart_img = pygame.transform.scale(dart_img, (20, 35))  # Resize dart image

class Dart:
    def __init__(self, x, y, target):
        self.image = dart_img
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.target = target
        self.dx, self.dy = self.calculate_velocity()  # Calculate initial velocity

    def calculate_velocity(self):
        dx, dy = self.target.rect.centerx - self.rect.centerx, self.target.rect.centery - self.rect.centery
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            return dx / dist * self.speed, dy / dist * self.speed
        return 0, 0

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self):
        screen.blit(self.image, self.rect.topleft)  # Draw the dart on the screen

# Tower Class
class Tower:
    def __init__(self, x, y):
        self.image = tower_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.range = 100
        self.damage = 50
        self.cooldown = 30  # 0.5 seconds at 60 FPS
        self.last_shot = 0

    def shoot(self, bloons, darts):
        # Shoot at the first bloon in range
        for bloon in bloons:
            dist = math.sqrt((bloon.rect.centerx - self.rect.centerx)**2 + (bloon.rect.centery - self.rect.centery)**2)
            if dist < self.range and self.last_shot >= self.cooldown:
                darts.append(Dart(self.rect.centerx, self.rect.centery, bloon))  # Create a new dart
                self.last_shot = 0
                break
        self.last_shot += 1

    def draw(self):
        screen.blit(self.image, self.rect.topleft)  # Draw the tower on the screen

# Game Class
class Game:
    def __init__(self):
        self.bloons = []
        self.towers = []
        self.darts = []
        self.round = 1
        self.lives = 100
        self.money = 500
        # Example path starting from the bottom left TODO: change paths for different maps. Will be stored as json files
        self.path = [(4, 400), (171, 400), (171, 184), (362, 184), (362, 608), (97, 608), (97, 771), (757, 771), (757, 526), (537, 526), (537, 326), (755, 326), (755, 91), (471, 91), (471, 4)]
        self.original_path = self.path.copy()

    def spawn_bloon(self):
        # Spawn a bloon every few seconds
        if len(self.bloons) < self.round * 5:
            self.bloons.append(Bloon(self.path))  # Add a new bloon to the list

    def update_bloons(self):
        for bloon in self.bloons[:]:
            bloon.move()
            if bloon.path_pos >= len(bloon.path) - 1:
                self.bloons.remove(bloon)
                self.lives -= 1  # Decrease lives if bloon reaches the end
            if bloon.health <= 0:
                self.bloons.remove(bloon)
                self.money += 1  # Increase money if bloon is destroyed

    def update_towers(self):
        for tower in self.towers:
            tower.shoot(self.bloons, self.darts)  # Towers shoot at bloons

    def update_darts(self):
        for dart in self.darts[:]:
            dart.move()
            for bloon in self.bloons:
                if dart.rect.colliderect(bloon.rect):
                    bloon.health -= 50  # Decrease bloon health if hit by dart
                    self.darts.remove(dart)
                    break

    def draw(self):
        screen.blit(background_img, (0, 0))  # Draw the background

        for bloon in self.bloons:
            bloon.draw()

        for tower in self.towers:
            tower.draw()

        for dart in self.darts:
            dart.draw()

        # Draw path (for demonstration)
        for i in range(len(self.path) - 1):
            pygame.draw.line(screen, BLUE, self.path[i], self.path[i + 1], 5)

        # Draw money and health counters
        font = pygame.font.SysFont(None, 36)
        money_text = font.render(f"Money: {self.money}", True, BLACK)
        lives_text = font.render(f"Lives: {self.lives}", True, BLACK)
        screen.blit(money_text, (10, 10))
        screen.blit(lives_text, (10, 50))

    def resize(self, new_width, new_height):
        global SCREEN_WIDTH, SCREEN_HEIGHT
        SCREEN_WIDTH, SCREEN_HEIGHT = new_width, new_height
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)  # Adjust screen size
        self.path = [(int(x * new_width / 800), int(y * new_height / 600)) for x, y in self.original_path]  # Adjust path

# Main Game Loop
def main():
    game = Game()
    main_menu = MainMenu("Player1", SCREEN_WIDTH, SCREEN_HEIGHT)
    map_selector = MapSelector(SCREEN_WIDTH, SCREEN_HEIGHT)
    current_screen = "main_menu"

    running = True
    while running:
        screen.fill(WHITE)
        
        if current_screen == "main_menu":
            main_menu.draw(screen)
        elif current_screen == "map_selector":
            map_selector.draw(screen)
        else:
            game.spawn_bloon()  # Spawn new bloons
            game.update_bloons()  # Update bloon positions and states
            game.update_towers()  # Update tower actions
            game.update_darts()  # Update dart positions and collisions
            game.draw()  # Draw all game elements

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the game loop
            elif event.type == pygame.VIDEORESIZE:
                game.resize(event.w, event.h)  # Handle screen resize
            elif current_screen == "main_menu":
                result = main_menu.handle_events(event)
                if result == "map_selector":
                    current_screen = "map_selector"
            elif current_screen == "map_selector":
                result = map_selector.handle_events(event)
                if result == "main_menu":
                    current_screen = "main_menu"
                elif result and result.startswith("map_"):
                    current_screen = "game"
                    # Load the selected map here
            else:
                # Mouse click to place a tower
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        game.towers.append(Tower(x, y))  # Place a new tower

        # Update sliders for smooth animation
        if current_screen == "main_menu":
            main_menu.settings_menu.update()
        elif current_screen == "map_selector":
            # Update any sliders in the map selector if needed
            pass

        pygame.display.update()
        clock.tick(FPS)  # Maintain the frame rate

    pygame.quit()

if __name__ == "__main__":
    main()  # Start the game