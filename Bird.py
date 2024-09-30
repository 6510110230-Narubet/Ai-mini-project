import pygame
from pygame.locals import *
import random

class Bird(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # สร้างลิสต์สำหรับเก็บภาพของนก
        self.images = []
        self.index = 0  # เก็บค่าดัชนีของภาพที่จะใช้
        self.counter = 0  # ตัวนับสำหรับควบคุมความเร็วการกระพือปีก

        # โหลดภาพนก 3 รูปเข้ามาในลิสต์
        for num in range(1, 4):
            img = pygame.image.load(f"img/bird{num}.png")
            self.images.append(img)
        
        # ตั้งค่าเริ่มต้นให้กับภาพแรก
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()  # สร้างกรอบสี่เหลี่ยมที่ครอบภาพนก
        self.rect.center = [x, y]  # ตำแหน่งเริ่มต้นของนก
        self.vel = 0  # ความเร็วในการเคลื่อนที่ (ใช้กับแรงโน้มถ่วง)
        self.clicked = False  # ตรวจสอบว่านกถูกคลิก
        self.flying = True  # ตรวจสอบสถานะของนกว่ายังบินอยู่หรือไม่
        self.game_over = False  # สถานะเกมจบ
        self.pipe_passed = 0  # นับจำนวนท่อที่นกผ่าน
        # สุ่มสีของนก
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self):
        # ตรวจสอบว่านกยังบินอยู่หรือไม่
        if self.flying:
            # ใช้แรงโน้มถ่วงดึงนกลง
            self.vel += 0.5
            if self.vel > 8:  # จำกัดความเร็วสูงสุดที่นกตก
                self.vel = 8
            if self.rect.bottom < 768:  # ตรวจสอบไม่ให้นกตกถึงพื้น
                self.rect.y += int(self.vel)

        if not self.game_over:  # ถ้าเกมยังไม่จบ
            # กระโดด (เคลื่อนที่ขึ้น)
            if self.clicked:
                self.clicked = False
                self.vel = -10  # ความเร็วในการกระโดด (เคลื่อนที่ขึ้น)
            
            # จัดการอนิเมชันกระพือปีก
            flap_cooldown = 5  # ควบคุมความเร็วในการกระพือปีก
            self.counter += 1

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1  # เปลี่ยนภาพของนกเป็นภาพถัดไป
                if self.index >= len(self.images):  # ถ้าถึงภาพสุดท้ายให้กลับไปเริ่มใหม่
                    self.index = 0
                self.image = self.images[self.index]

            # หมุนนกตามความเร็วในการตก
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            # ถ้าเกมจบ ให้นกหมุนลงชี้พื้น
            self.image = pygame.transform.rotate(self.images[self.index], -90)
