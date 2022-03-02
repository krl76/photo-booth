import pygame
import cv2
import numpy as np
from PIL import Image

camera = cv2.VideoCapture(0)
pygame.init()
pygame.display.set_caption("Camera")
screen = pygame.display.set_mode([1280, 720])

while True:
    ret, frame = camera.read()
    # frame = Image.open()
    # frame = frame.resize(500, 500)
    screen.fill([0, 0, 0])
    pygame.display.flip()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0, 0))
    pygame.display.update()

sys.exit(0)
pygame.quit()
cv2.destroyAllWindows()
