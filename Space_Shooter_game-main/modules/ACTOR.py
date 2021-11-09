import pygame
from LASER import *
from SHIP import *
RED_SPACE_SHIP = pygame.transform.scale(pygame.image.load("image/enemy3.png"),(60,28))
GREEN_SPACE_SHIP = pygame.transform.scale(pygame.image.load("image/enemy1.png"),(64,44))
BLUE_SPACE_SHIP = pygame.transform.scale(pygame.image.load("image/enemy2.png"),(61,33))

# Player player
SPACE_SHIP = pygame.transform.scale(pygame.image.load("image/spaceship1.png"),(50,50))

# Lasers
RED_LASER = pygame.transform.scale(pygame.image.load("image/pixel_laser_red.png"),(65,75))
GREEN_LASER = pygame.transform.scale(pygame.image.load("image/pixel_laser_green.png"),(65,75))
BLUE_LASER = pygame.transform.scale(pygame.image.load("image/pixel_laser_blue.png"),(65,75))
YELLOW_LASER = pygame.transform.scale(pygame.image.load("image/pixel_laser_yellow.png"),(65,75))

# Background
BG_ingame = pygame.transform.scale(pygame.image.load("image/background-black.png"), (WIDTH, HEIGHT))
BG = pygame.transform.scale(pygame.image.load("image/background.png"), (WIDTH, HEIGHT))
score = 0