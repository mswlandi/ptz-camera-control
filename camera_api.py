import requests

# http://[Camera IP]/cgi-bin/ptzctrl.cgi?ptzcmd&[Action]&[Pan Speed]&[Tilt Speed]
# [Action]: up, down, left, right, leftup, rightup, leftdown, rightdown, ptzstop
# [Pan Speed]: 1 (Slowest) – 24 (Fastest)
# [Tilt Speed]: 1 (Slowest) – 20 (Fastest)

# camera_ip = '192.168.0.2'
camera_ip = 'localhost:5000'


def _get_action(x: int, y: int) -> str:
    '''
    Get the action to be taken based on the direction of the movement
    '''
    directions = {
        (1, 1): 'rightdown',
        (1, -1): 'rightup',
        (-1, 1): 'leftdown',
        (-1, -1): 'leftup',
        (1, 0): 'right',
        (-1, 0): 'left',
        (0, 1): 'down',
        (0, -1): 'up'
    }
    return directions.get((int(x > 0) - int(x < 0), int(y > 0) - int(y < 0)), 'ptzstop')

def scroll(x: int, y: int):
    '''
    Scroll (Pan and/or Tilt) the camera in the given directions
    '''

    action = _get_action(x, y)
    x = abs(x)
    y = abs(y)

    print(f'Action: {action}, x: {x}, y: {y}')

    requests.get(f'http://{camera_ip}/cgi-bin/ptzctrl.cgi?ptzcmd&{action}&{x}&{y}')
