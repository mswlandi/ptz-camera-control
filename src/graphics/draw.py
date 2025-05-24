import pygame
from common.state import mouse_mode

SCREEN_SIZE = (480, 480)

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Consolas', 30)
screen = pygame.display.set_mode(SCREEN_SIZE)

def clear_screen():
    screen.fill("black")

def draw_info():
    text_surface = font.render(
        f'MODO: {"mouse" if mouse_mode else "teclado"}', False, (255, 255, 255))

    screen.blit(text_surface, (SCREEN_SIZE[0]/2 - text_surface.get_width() / 2, 10))
