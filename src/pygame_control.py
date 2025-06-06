import pygame
from camera.camera_api import scroll, zoom
from common.state import mouse_mode, scrolling
from graphics.draw import draw_info, clear_screen

def move_according_to_key(key, speed = 1):
    if key is None:
        scroll(0,0)
        return

    if key == pygame.K_UP:
        scroll(0, -speed)
    elif key == pygame.K_DOWN:
        scroll(0, speed)
    elif key == pygame.K_LEFT:
        scroll(-speed, 0)
    elif key == pygame.K_RIGHT:
        scroll(speed, 0)

# pygame setup
clock = pygame.time.Clock()
running = True

MOVE_KEYS = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
pressing_key = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key in MOVE_KEYS:
                move_according_to_key(event.key, 4)
            elif event.key == pygame.K_m and not mouse_mode:
                mouse_mode = True
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)
            elif event.key == pygame.K_t and mouse_mode:
                mouse_mode = False
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)

        elif event.type == pygame.KEYUP:
            if event.key in MOVE_KEYS:
                move_according_to_key(None, 4)
            

    # fill the screen with a color to wipe away anything from last frame
    clear_screen()

    # LOGIC
    if mouse_mode:
        delta_x, delta_y = pygame.mouse.get_rel()
        scroll(int(delta_x/5),int(delta_y/5))

    MODS = pygame.key.get_mods()

    if MODS & pygame.KMOD_LSHIFT and not scrolling:
        scrolling = True
        zoom(2)
    elif MODS & pygame.KMOD_LCTRL and not scrolling:
        scrolling = True
        zoom(-2)
    else:
        if not scrolling:
            zoom(0)
        scrolling = False

    draw_info()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)

pygame.quit()