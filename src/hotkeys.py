import keyboard
from camera.camera_api import scroll, enable_tracking, disable_tracking, call_1

keyboard.add_hotkey('ctrl+alt+shift+e', enable_tracking)
keyboard.add_hotkey('ctrl+alt+shift+d', disable_tracking)
keyboard.add_hotkey('ctrl+alt+shift+1', call_1)

keyboard.add_hotkey('ctrl+right', scroll, args=(1,0))
keyboard.add_hotkey('ctrl+left', scroll, args=(-1,0))

keyboard.wait('ctrl+shift+esc')
