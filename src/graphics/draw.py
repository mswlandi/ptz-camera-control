import os, sys
import pygame

def resource_path(rel_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    return os.path.join(base_path, rel_path)

SCREEN_SIZE = (480, 480)
IMG = {
    'icon': pygame.image.load(resource_path(os.path.join('img', 'icon.png')))
}

pygame.init()
pygame.display.set_caption('Controle de Câmera PTZ do Marcos')
pygame.display.set_icon(IMG['icon'])
pygame.font.init()
font = pygame.font.SysFont('Consolas', 30)
screen = pygame.display.set_mode(SCREEN_SIZE)

def clear_screen():
    screen.fill("black")

def draw_info(camera_ip='192.168.0.100'):
    text_surface = font.render(
        f'IP da Câmera: {camera_ip}', False, (255, 255, 255))

    screen.blit(text_surface, (SCREEN_SIZE[0]/2 - text_surface.get_width() / 2, 10))
