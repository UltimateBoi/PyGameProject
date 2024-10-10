import pygame
import sys
import math
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Path Drawer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Path list
path = []

def draw_path(screen, path):
    if len(path) > 1:
        pygame.draw.lines(screen, RED, False, path, 2)
    for node in path:
        pygame.draw.circle(screen, RED, node, 5)

def get_angle_locked_position(start_pos, end_pos):
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    angle = math.atan2(dy, dx)
    angle = round(angle / (math.pi / 4)) * (math.pi / 4)
    distance = math.hypot(dx, dy)
    locked_x = start_pos[0] + distance * math.cos(angle)
    locked_y = start_pos[1] + distance * math.sin(angle)
    return (int(locked_x), int(locked_y))

def main():
    # Prompt user to select a PNG map
    Tk().withdraw()  # Hide the root window
    map_path = askopenfilename(filetypes=[("PNG files", "*.png")])
    if not map_path:
        print("No map selected. Exiting.")
        pygame.quit()
        sys.exit()

    # Load the selected PNG map
    map_image = pygame.image.load(map_path)
    map_rect = map_image.get_rect()

    running = True
    shift_held = False

    global screen
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()
                    if shift_held and path:
                        pos = get_angle_locked_position(path[-1], pos)
                    path.append(pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # Clear path with 'c' key
                    path.clear()
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    shift_held = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    shift_held = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        screen.fill(WHITE)
        screen.blit(map_image, map_rect)
        draw_path(screen, path)
        pygame.display.flip()

    pygame.quit()
    print("self.path =", path)

if __name__ == "__main__":
    main()