# -*- coding: utf-8 -*-

import pygame
import time
import cv2
import numpy as np
from qrcodes import qr
import flask_prog


WIDTH = 1280  # ширина
HEIGHT = 720  # высота
WHITE = (255, 255, 255)  # цвет
running = True  # флаг мониторящий закрытие экрана
pygame.init()  # запуск
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # задать ширину высоту экрана
# screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, pygame.NOFRAME)
# screen.fill(WHITE)  цвет экрана залить
# pygame.display.flip() перевернуть окно
pygame.display.set_caption("PhotoApp")  # название окна
pygame.display.set_icon(pygame.image.load('icon.png'))  # иконка приложения
number_of_screen = 1  # номер окна
camera = cv2.VideoCapture(0)  # иницилизация камеры
press_button = False
pygame.time.set_timer(pygame.USEREVENT, 1000)
start = True
transfer = True
number_img = [pygame.image.load('5_5.png'), pygame.image.load('4_5.png'), pygame.image.load('3_5.png'),
              pygame.image.load('2_5.png'), pygame.image.load('1_5.png'), pygame.image.load('0_5.png')]
surf_button = pygame.Surface((WIDTH, HEIGHT))


class Button:  # кнопка
    def __init__(self, width, height, action=False, new=True):
        self.width = width
        self.height = height
        self.inactive_color = (133, 133, 133)
        self.active_color = (0, 0, 0)
        self.action = action
        self.new = new

    def draw(self, x, y, message, font_size, font_color, radius=None, frame=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                surf_button.fill(WHITE)
                surf_button.set_colorkey(WHITE)
                pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height), frame, radius)
                pygame.display.update()
                if click[0] == 1:
                    self.action = True
        else:
            surf_button.fill(WHITE)
            surf_button.set_colorkey(WHITE)
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height), frame, radius)
            pygame.display.update()
        if self.new:
            print_text(message, x + 50, y + 30, font_size, font_color)
            self.new = False

    def click(self):
        return self.action


def print_text(message, x, y, font_size, font_color, font_type='YakumoPreschoolHand.ttf'):
    # печать текста
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def draw_number():
    global counter_photo, WIDTH, HEIGHT
    width = 512
    height = 512
    surf_img_number = pygame.Surface((WIDTH, HEIGHT))
    for i in range(20):
        scale = pygame.transform.scale(number_img[counter_photo], (width, height))
        surf_img_number.fill(WHITE)
        surf_img_number.set_colorkey(WHITE)
        surf_img_number.blit(scale, scale.get_rect(center=(650, 380)))
        screen.blit(surf_img_number, (0, 0))
        width -= 25
        height -= 25
        pygame.display.update()
        time.sleep(0.03)
        number_of_screen2()


def number_of_screen1():
    global start
    start = False
    print_text('Добро пожаловать в фото-будку!', 310, 250, 50, (0, 0, 0))
    print_text('Нажмите на любую часть экрана, чтобы продолжить!', 100, 320, 50, (0, 0, 0))
    pygame.display.update()
    while True:
        for event_number1 in pygame.event.get():
            if event_number1.type == pygame.MOUSEBUTTONDOWN:
                number_of_screen2(61)
                break


def number_of_screen2():
    screen.fill('white')
    ret, frame = camera.read()
    frame2 = np.rot90(frame)
    gray = cv2.cvtColor(frame2, cv2.COLORMAP_RAINBOW)
    frame2 = cv2.resize(gray, [420, 640])
    screen.blit(pygame.surfarray.make_surface(frame2), (320, 150))
    pygame.display.update()


def number_of_screen3():
    screen.fill(WHITE)
    screen.fill(pygame.Color('red'), pygame.Rect(350, 150, 600, 450))
    pygame.display.update()


while running:
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            number_of_screen = 2
            new = True
    if number_of_screen == 1:
        if transfer:
            screen.fill(WHITE)
            pygame.display.flip()
            transfer = False
        print_text('Добро пожаловать в фото-будку!', 310, 250, 50, (0, 0, 0))
        print_text('Нажмите на любую часть экрана, чтобы продолжить!', 100, 320, 50, (0, 0, 0))
        pygame.display.update()
    elif number_of_screen == 2:
        if new:
            counter = 1750
            counter_photo = -1
            new = False
            flag_mouse2 = False
            '''button = True
            button1 = Button(300, 100)
            button2 = Button(300, 100)'''
            screen.fill(WHITE)
            # pygame.draw.rect(screen, (133, 133, 133), (350, 150, 600, 450))
            pygame.display.update()
        '''if button:
            button1.draw(30, 350, 'Вернуться назад', 30, (0, 0, 0), 8, 3)
            button2.draw(965, 340, 'Сделать снимок', 30, (0, 0, 0), 8, 3)'''
        while True:
            for event1 in pygame.event.get():
                if event1.type == pygame.MOUSEBUTTONDOWN:
                    flag_mouse2 = True
                    break
            ret, frame = camera.read()
            frame2 = np.rot90(frame)
            gray = cv2.cvtColor(frame2, cv2.COLORMAP_RAINBOW)
            frame2 = cv2.resize(gray, [420, 640])
            screen.blit(pygame.surfarray.make_surface(frame2), (320, 150))
            pygame.display.update()
            if flag_mouse2:
                break
            elif counter > 0:
                counter -= 1
                # screen.fill('white')
                # print_text(str(counter), 100, 10, 50, 'black')
            elif counter == 0:
                transfer = True
                number_of_screen = 1
                break
        if flag_mouse2:
            counter_photo += 1
            draw_number()
        if counter_photo == 5:
            frame = cv2.resize(frame, [640, 420])
            frame = cv2.flip(frame, 1)
            cv2.imwrite('photos/image-1.png', frame)
            number_of_screen = 3
            qr_new = True
            flag_mouse2 = False
        '''if button1.click():
            transfer = True
            number_of_screen = 1'''
    elif number_of_screen == 3:
        screen.fill(WHITE)
        img = pygame.image.load('photos/image-1.png')
        if qr_new:
            qrc = pygame.image.load(qr())
            qr_new = False
        screen.blit(qrc, (870, 200))
        screen.blit(img, (150, 150))
        # screen.fill(pygame.Color('red'), pygame.Rect(350, 150, 600, 450))
        pygame.display.update()
        '''flask_prog.start()
        time.sleep(40)
        flask_prog.close()'''
