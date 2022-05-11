# -*- coding: utf-8 -*-

import pygame
import time
import cv2
import numpy as np
from qrcodes import generate_qr
# import flask_prog


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


def draw_number(counter_photo, WIDTH, HEIGHT):
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
        output_camera()


def clear_screen():
    screen.fill(WHITE)
    pygame.display.flip()


def output_camera():
    screen.fill(WHITE)
    ret, frame = camera.read()
    frame2 = np.rot90(frame)
    gray = cv2.cvtColor(frame2, cv2.COLORMAP_RAINBOW)
    frame2 = cv2.resize(gray, (420, 640))
    screen.blit(pygame.surfarray.make_surface(frame2), (320, 150))
    pygame.display.update()


def main_screen():
    global transfer
    if transfer:
        clear_screen()
        transfer = False
    print_text('Добро пожаловать в фото-будку!', 310, 250, 50, (0, 0, 0))
    print_text('Нажмите на любую часть экрана, чтобы продолжить!', 100, 320, 50, (0, 0, 0))
    pygame.display.update()


def vebcam_screen():
    global new, transfer, number_of_screen, qr_new, new3, flag_mouse2, counter_photo
    if new:
        counter = 1750
        counter_photo = -1
        new = False
        flag_mouse2 = False
        '''button = True
        button1 = Button(300, 100)
        button2 = Button(300, 100)'''
        clear_screen()
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
        frame2 = cv2.resize(gray, (420, 640))
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
        draw_number(counter_photo, WIDTH, HEIGHT)
    if counter_photo == 5:
        frame = cv2.resize(frame, (640, 420))
        frame = cv2.flip(frame, 1)
        cv2.imwrite('photos/image-1.png', frame)
        number_of_screen = 3
        qr_new = True
        flag_mouse2 = False
        new3 = True
    '''if button1.click():
        transfer = True
        number_of_screen = 1'''


def photo_output_screen():
    global new3, qr_new, number_of_screen, transfer, qrc
    if new3:
        counter = 1750
    counter -= 1
    screen.fill(WHITE)
    img = pygame.image.load('photos/image-1.png')
    if qr_new:
        qrc = pygame.image.load(generate_qr())
        qr_new = False
    screen.blit(qrc, (870, 200))
    screen.blit(img, (150, 150))
    # screen.fill(pygame.Color('red'), pygame.Rect(350, 150, 600, 450))
    pygame.display.update()
    if counter == 0:
        number_of_screen = 1
        transfer = True


while running:
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if number_of_screen == 1:
                number_of_screen = 2
                new = True
            if number_of_screen == 3:
                number_of_screen = 1
                transfer = True
    if number_of_screen == 1:
        main_screen()
    elif number_of_screen == 2:
        vebcam_screen()
    elif number_of_screen == 3:
        photo_output_screen()
        '''flask_prog.start()
        time.sleep(40)
        flask_prog.close()'''
