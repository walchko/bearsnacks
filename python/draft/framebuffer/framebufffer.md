
```
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev
```

```
pip install -U pygame
```

```python
import pygame
import os
import time

os.environ["SDL_FBDEV"] = "/dev/fb0"

pygame.init()

# screen rotated to portrait mode
screen = pygame.display.set_mode([480,800], pygame.FULLSCREEN)

def go(t):
    for i in range(t):
        screen.fill((200, 100, 155))
        pygame.draw.circle(screen, (0, 0, 255), (i%400, i%400), 75)
        pygame.display.flip()
        time.sleep(1/20)
        
go(1000)
print("success")
```

## Rotate Screen

```
sudo nano /boot/config.txt
```

Add one of these to the bottom:

```
display_rotate=0 Normal
display_rotate=1 90 degrees
display_rotate=2 180 degrees
NOTE: You can rotate both the image and touch interface 180º by entering lcd_rotate=2 instead
display_rotate=3 270 degrees
display_rotate=0x10000 horizontal flip
display_rotate=0x20000 vertical flip
```

## Reference

- [SDL/Pygame to framebuffer in SSH session](https://www.raspberrypi.org/forums/viewtopic.php?t=262907)
- [Rotating screen](https://www.raspberrypi.org/forums/viewtopic.php?f=108&t=120793)
