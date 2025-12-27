import pygame
from camera.camera_api import scroll, zoom
from common.state import scrolling
from graphics.draw import draw_info, clear_screen
from camera.camera_api import camera_ip

# Movement speed per command unit
MOVE_SPEED = 4

def compute_scroll_from_keys(keys_dict):
    """Compute dx, dy from current key states, allowing diagonal movement.

    Opposing keys cancel each other out (e.g., Left+Right => dx = 0).
    Returns a tuple (dx, dy).
    """
    dx = 0
    dy = 0

    # Horizontal
    if keys_dict.get(pygame.K_LEFT, False):
        dx -= MOVE_SPEED
    if keys_dict.get(pygame.K_RIGHT, False):
        dx += MOVE_SPEED

    # Vertical (negative dy is up in typical screen coords; adjust if needed)
    if keys_dict.get(pygame.K_UP, False):
        dy -= MOVE_SPEED
    if keys_dict.get(pygame.K_DOWN, False):
        dy += MOVE_SPEED

    return dx, dy

# pygame setup
clock = pygame.time.Clock()
running = True

MOVE_KEYS = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
keys = {
    pygame.K_UP: False,
    pygame.K_DOWN: False,
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False
}

# Track last scroll command to avoid sending duplicates
last_dx_dy = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key in MOVE_KEYS:
                # Update key state; actual scroll will be sent if state changes
                keys[event.key] = True

        elif event.type == pygame.KEYUP:
            if event.key in MOVE_KEYS:
                # Update key state; actual scroll will be sent if state changes
                keys[event.key] = False
            

    # fill the screen with a color to wipe away anything from last frame
    clear_screen()

    # LOGIC
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

    # Compute desired scroll from key states and send only on change
    current_dx_dy = compute_scroll_from_keys(keys)
    if current_dx_dy != last_dx_dy:
        dx, dy = current_dx_dy
        scroll(dx, dy)
        last_dx_dy = current_dx_dy

    draw_info(camera_ip)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)

pygame.quit()