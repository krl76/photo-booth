# -*- coding: utf-8 -*-

import pygame
import cv2
import numpy as np
from PIL import Image

'''pygame.init()
pygame.display.set_caption("Camera")
screen = pygame.display.set_mode((1280, 720))
screen.fill([128, 128, 128])
pygame.display.flip()'''


def cam():
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        frame2 = np.rot90(frame)
        gray = cv2.cvtColor(frame2, cv2.COLORMAP_RAINBOW)
        frame2 = cv2.resize(gray, [420, 640])
        return frame2
        # screen.blit(pygame.surfarray.make_surface(frame2), (320, 150))
