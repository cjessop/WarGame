import numpy as np
import pandas as pd
import pygame

import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up display
MAP_WIDTH, MAP_HEIGHT = 8192, 4096
#WIDTH, HEIGHT = 819.2, 409.6
WIDTH, HEIGHT = 2000, 1200

raid_size = 10
PRE_LAUNCH_DELAY = 15  # 15 seconds before launch

font = pygame.font.Font(None, 36)

##screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Rocket Trajectory")


# Load map image
map_image = pygame.image.load("8k_earth_daymap.jpg")  # Replace with your image path
map_image = pygame.transform.scale(map_image, (WIDTH, int(WIDTH / MAP_WIDTH * MAP_HEIGHT)))

# Define launch and target positions (x, y)
#launch_position = [(400, 250), (450, 250)]
target_position = (1100, 500)

# Draw grid lines and labels
def draw_grid(screen, width, height, spacing):
    for x in range(0, width, spacing):
        pygame.draw.line(screen, (100, 100, 100), (x, 0), (x, height))
        font = pygame.font.Font(None, 24)
        text = font.render(str(x), True, (255, 255, 255))
        screen.blit(text, (x + 5, 5))
    for y in range(0, height, spacing):
        pygame.draw.line(screen, (100, 100, 100), (0, y), (width, y))
        font = pygame.font.Font(None, 24)
        text = font.render(str(y), True, (255, 255, 255))
        screen.blit(text, (5, y + 5))

def draw_grid_minor(screen, width, height, major_spacing, minor_spacing):
    for x in range(0, width, major_spacing):
        pygame.draw.line(screen, (100, 100, 100), (x, 0), (x, height))
        font = pygame.font.Font(None, 24)
        text = font.render(str(x), True, (255, 255, 255))
        screen.blit(text, (x + 5, 5))
        for minor_x in range(x + minor_spacing, x + major_spacing, minor_spacing):
            pygame.draw.line(screen, (50, 50, 50, 100), (minor_x, 0), (minor_x, height), 1)
    for y in range(0, height, major_spacing):
        pygame.draw.line(screen, (100, 100, 100), (0, y), (width, y))
        font = pygame.font.Font(None, 24)
        text = font.render(str(y), True, (255, 255, 255))
        screen.blit(text, (5, y + 5))
        for minor_y in range(y + minor_spacing, y + major_spacing, minor_spacing):
            pygame.draw.line(screen, (50, 50, 50, 100), (0, minor_y), (width, minor_y), 1)

# Rocket class
class Rocket(pygame.sprite.Sprite):
    def __init__(self, launch_position):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.launch_position = launch_position
        # self.image = pygame.Surface((40, 40), pygame.SRCALPHA)  # Transparent surface
        # self.image.fill((0, 0, 0, 0))  # Make the surface transparent
        # pygame.draw.circle(self.image, (255, 0, 0), (20, 20), 20)  # Draw a red filled circle
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.launch_position
        self.speed = self.calculate_speed()  # Calculate speed based on travel time
        self.start_time = time.time()
        self.travel_time = 35 * 60  # 35 minutes in seconds

    def update(self):
        elapsed_time = time.time() - self.start_time
        progress = elapsed_time / self.travel_time
        if progress >= 1:
            self.rect.center = target_position
        else:
            # Calculate current position based on linear interpolation
            current_x =self.launch_position[0] + (target_position[0] -self.launch_position[0]) * progress
            current_y =self.launch_position[1] + (target_position[1] -self.launch_position[1]) * progress
            self.rect.center = (current_x, current_y)

    def calculate_speed(self):
        # Calculate speed based on travel time and the distance between launch and target positions
        distance = ((target_position[0] -self.launch_position[0]) ** 2 + (target_position[1] -self.launch_position[1]) ** 2) ** 0.5
        speed = distance / (35 * 60)
        return speed
    

    def draw_trajectory(self, screen):
        pygame.draw.line(screen, (255, 255, 255),self.launch_position, self.rect.center, 2)

# Create rocket sprite



rocket_list = []
for i in range(0, raid_size):
    rand_num1 = np.random.randint(400, 500)
    rand_num2 = np.random.randint(200, 250)
    rocket = Rocket((rand_num1, rand_num2))
    rocket_list.append(rocket)

print(rocket_list)


rocket1 = Rocket((400, 250))
rocket2 = Rocket((450, 250))
all_sprites = pygame.sprite.Group()
for i in range(0, len(rocket_list)):
    all_sprites.add(rocket_list[i])
#all_sprites.add(rocket1, rocket2)

# Main loop
running = True
event_spotted = False
pre_launch_start_time = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if event_spotted:


    # Update rocket
        all_sprites.update()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw map
    screen.blit(map_image, (0, 0))

    # Draw launch position
    if not event_spotted:
        pygame.draw.circle(screen, (255, 0, 0), (400, 250), 2)

    # Draw grid lines
    draw_grid_minor(screen, WIDTH, HEIGHT, 100, 50)  # Adjust spacing as needed

    if event_spotted:
    # Draw rocket trajectory
        for rocket in rocket_list:
            rocket.draw_trajectory(screen)
    #rocket_list[2].draw_trajectory(screen)

    # Draw sprites
    if event_spotted:
        all_sprites.draw(screen)

    # Display "IR EVENT SPOTTED" text at the top
    if not event_spotted:
        font = pygame.font.Font(None, 36)
        text = font.render("IR EVENT SPOTTED", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, 50))
        screen.blit(text, text_rect)

    if not event_spotted and time.time() - pre_launch_start_time >= PRE_LAUNCH_DELAY:
        event_spotted = True
        rocket.start_time = time.time()    

    # Update time to landing
    time_to_landing = max(0, rocket1.travel_time - (time.time() - rocket1.start_time))
    time_to_landing_str = "Time to Impact: {:02}:{:02}".format(int(time_to_landing // 60), int(time_to_landing % 60))
    timer_text = font.render(time_to_landing_str, True, (255, 0, 0))
    screen.blit(timer_text, (WIDTH - 350, 20))  # Adjust the position as needed

    # Update display
    pygame.display.flip()

    # Cap frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
