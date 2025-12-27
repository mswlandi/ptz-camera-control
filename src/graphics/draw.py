import pygame

SCREEN_SIZE = (480, 480)

pygame.init()
pygame.display.set_caption('Controle de Câmera PTZ do Marcos')
pygame.display.set_icon(pygame.image.load('icon.png'))
pygame.font.init()
font = pygame.font.SysFont('Consolas', 30)
screen = pygame.display.set_mode(SCREEN_SIZE)

def clear_screen():
    screen.fill("black")

def draw_info(camera_ip='192.168.0.100'):
    text_surface = font.render(
        f'IP da Câmera: {camera_ip}', False, (255, 255, 255))

    screen.blit(text_surface, (SCREEN_SIZE[0]/2 - text_surface.get_width() / 2, 10))
