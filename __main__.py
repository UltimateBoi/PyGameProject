import pygame
import math
from MainMenu import MainMenu
from MapSelector import MapSelector
from towers import Tower, Dart
from ui import TowerSidebar

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Tower Defense Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Load images
background_img = pygame.image.load('assets/map_1.png')
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Bloon Class (Enemy)
class Bloon:
    def __init__(self, path):
        self.image = pygame.image.load('assets/bloon.png')
        self.rect = self.image.get_rect()
        self.rect.center = path[0]
        self.path = path
        self.speed = 2
        self.path_pos = 0
        self.health = 100
    
    def move(self):
        if self.path_pos < len(self.path) - 1:
            target_x, target_y = self.path[self.path_pos + 1]
            dx, dy = target_x - self.rect.centerx, target_y - self.rect.centery
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 0:
                dx, dy = dx / dist, dy / dist
                self.rect.centerx += dx * self.speed
                self.rect.centery += dy * self.speed

            if dist < 5:
                self.path_pos += 1

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

# Game Class
class Game:
    def __init__(self):
        self.bloons = []
        self.towers = []
        self.darts = []
        self.round = 1
        self.lives = 100
        self.money = 500
        self.path = [(4, 400), (171, 400), (171, 184), (362, 184), (362, 608), 
                     (97, 608), (97, 771), (757, 771), (757, 526), (537, 526), 
                     (537, 326), (755, 326), (755, 91), (471, 91), (471, 4)]
        self.original_path = self.path.copy()
        self.sidebar = TowerSidebar(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.selected_tower = None
        self.dragging_tower = None
        
        # Wave spawning variables
        self.bloons_per_wave = 5
        self.bloons_spawned = 0
        self.spawn_delay = 120  # 2 seconds at 60 FPS
        self.spawn_timer = 0
        self.wave_in_progress = False
        self.wave_complete = False
        self.wave_start_delay = 180  # 3 seconds between waves

    def start_wave(self):
        if not self.wave_in_progress and not self.wave_complete:
            self.wave_in_progress = True
            self.bloons_spawned = 0
            self.spawn_timer = 0
        elif self.wave_complete:
            self.round += 1
            self.bloons_per_wave = 5 + (self.round - 1) * 2  # Increase bloons per wave
            self.wave_in_progress = True
            self.wave_complete = False
            self.bloons_spawned = 0
            self.spawn_timer = 0

    def spawn_bloon(self):
        if self.wave_in_progress:
            if self.bloons_spawned < self.bloons_per_wave:
                if self.spawn_timer >= self.spawn_delay:
                    self.bloons.append(Bloon(self.path))
                    self.bloons_spawned += 1
                    self.spawn_timer = 0
                else:
                    self.spawn_timer += 1
            elif len(self.bloons) == 0:  # All bloons from wave are gone
                self.wave_in_progress = False
                self.wave_complete = True
                self.spawn_timer = 0

    def update_bloons(self):
        for bloon in self.bloons[:]:
            bloon.move()
            if bloon.path_pos >= len(bloon.path) - 1:
                self.bloons.remove(bloon)
                self.lives -= 1
            if bloon.health <= 0:
                self.bloons.remove(bloon)
                self.money += 1

    def update_towers(self):
        for tower in self.towers:
            tower.shoot(self.bloons, self.darts)

    def update_darts(self):
        for dart in self.darts[:]:
            dart.move()
            if not dart.active:
                self.darts.remove(dart)
                continue
                
            for bloon in self.bloons:
                if dart.rect.colliderect(bloon.rect):
                    bloon.health -= 50
                    self.darts.remove(dart)
                    break

    def draw(self):
        screen.blit(background_img, (0, 0))

        # Draw path
        for i in range(len(self.path) - 1):
            pygame.draw.line(screen, BLUE, self.path[i], self.path[i + 1], 5)

        # Draw game objects
        for bloon in self.bloons:
            bloon.draw()

        for tower in self.towers:
            tower.draw(screen)

        for dart in self.darts:
            dart.draw(screen)

        # Draw sidebar
        self.sidebar.draw(screen)

        # Draw UI elements
        font = pygame.font.SysFont(None, 36)
        money_text = font.render(f"Money: ${self.money}", True, BLACK)
        lives_text = font.render(f"Lives: {self.lives}", True, BLACK)
        round_text = font.render(f"Round: {self.round}", True, BLACK)
        screen.blit(money_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(round_text, (10, 90))

        # Draw wave status
        if self.wave_complete:
            wave_text = font.render("Press SPACE for next wave", True, (0, 255, 0))
            screen.blit(wave_text, (SCREEN_WIDTH // 2 - 150, 10))
        elif not self.wave_in_progress:
            wave_text = font.render("Press SPACE to start wave", True, (255, 255, 0))
            screen.blit(wave_text, (SCREEN_WIDTH // 2 - 150, 10))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                pos = pygame.mouse.get_pos()
                
                # Check if clicking in sidebar
                if self.sidebar.rect.collidepoint(pos):
                    tower = self.sidebar.handle_mouse_down(pos)
                    if tower and self.money >= tower.cost:
                        self.dragging_tower = tower
                else:
                    # Check if clicking on existing tower
                    for tower in self.towers:
                        if tower.rect.collidepoint(pos):
                            # Deselect other towers
                            for t in self.towers:
                                t.is_selected = False
                            tower.is_selected = True
                            self.selected_tower = tower
                            break
                    else:
                        # Deselect all towers if clicking empty space
                        for tower in self.towers:
                            tower.is_selected = False
                        self.selected_tower = None

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging_tower:
                pos = pygame.mouse.get_pos()
                if not self.sidebar.rect.collidepoint(pos):
                    # Place tower if we have enough money
                    if self.money >= self.dragging_tower.cost:
                        self.money -= self.dragging_tower.cost
                        self.towers.append(self.dragging_tower)
                self.dragging_tower = None

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_tower:
                self.dragging_tower.rect.center = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right click
            if self.selected_tower:
                action = self.selected_tower.handle_click(event.pos)
                if action == "upgrade":
                    if self.money >= self.selected_tower.upgrade_cost:
                        if self.selected_tower.upgrade():
                            self.money -= self.selected_tower.upgrade_cost
                elif action == "sell":
                    self.money += self.selected_tower.sell()
                    self.towers.remove(self.selected_tower)
                    self.selected_tower = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.start_wave()

    def resize(self, new_width, new_height):
        global SCREEN_WIDTH, SCREEN_HEIGHT
        SCREEN_WIDTH, SCREEN_HEIGHT = new_width, new_height
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        self.path = [(int(x * new_width / 800), int(y * new_height / 600)) 
                    for x, y in self.original_path]
        self.sidebar = TowerSidebar(SCREEN_WIDTH, SCREEN_HEIGHT)

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
            game.spawn_bloon()
            game.update_bloons()
            game.update_towers()
            game.update_darts()
            game.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                game.resize(event.w, event.h)
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
            else:
                game.handle_events(event)

        if current_screen == "main_menu":
            main_menu.settings_menu.update()
        elif current_screen == "map_selector":
            pass

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()