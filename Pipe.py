import pygame
from pygame.locals import *
import setting

# คลาส Pipe ใช้สำหรับสร้างท่อ (pipe) ที่ bird จะต้องบินผ่าน
class Pipe(pygame.sprite.Sprite):

    # ฟังก์ชันเริ่มต้นของคลาส Pipe
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        
        # โหลดภาพท่อจากไฟล์
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()  # กำหนดพื้นที่ (rect) ของท่อจากขนาดของภาพ

        # ตัวแปร position กำหนดว่าท่อจะมาจากด้านบนหรือล่าง
        # position = 1 ท่อจะมาจากด้านบน, -1 ท่อจะมาจากด้านล่าง
        if position == 1:
            # ถ้า position เป็น 1, หมุนภาพท่อให้อยู่ด้านบน
            self.image = pygame.transform.flip(self.image, False, True)
            # กำหนดตำแหน่งของท่อจากด้านล่างซ้าย
            self.rect.bottomleft = [x, y - int(setting.PIPE_GAP / 2)]
        elif position == -1:
            # ถ้า position เป็น -1, กำหนดตำแหน่งของท่อจากด้านบนซ้าย
            self.rect.topleft = [x, y + int(setting.PIPE_GAP / 2)]

    # ฟังก์ชันอัปเดตการเคลื่อนไหวของท่อในเกม
    def update(self):
        # เลื่อนตำแหน่งของท่อไปทางซ้ายด้วยความเร็วที่กำหนด (SCROLL_SPEED)
        self.rect.x -= setting.SCROLL_SPEED
        
        # ถ้าท่อเลื่อนออกจากหน้าจอ (ด้านขวาของท่ออยู่ต่ำกว่าขอบซ้ายของหน้าจอ)
        # ให้ลบวัตถุท่อนี้ออกจากเกม
        if self.rect.right < 0:
            self.kill()
