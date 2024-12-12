import pygame
import random

# Параметры экрана
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Змейка')

# Цвета
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
dark_green = (2, 100, 62)
white = (255, 255, 255)

# Параметры змейки
snake_block = 10
snake_speed = 15

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
