import keyboard
from camera_api import scroll

keyboard.add_hotkey('ctrl+shift+a', print, args=('triggered', 'hotkey'))

keyboard.add_hotkey('up', scroll, args=(0, -1))
keyboard.add_hotkey('down', scroll, args=(0, 1))
keyboard.add_hotkey('left', scroll, args=(-1, 0))
keyboard.add_hotkey('right', scroll, args=(1, 0))

keyboard.wait('ctrl+shift+esc')
