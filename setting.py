import pygame
from pygame.locals import *

# กำหนดตัวแปรทั้งหมดให้เป็น global เพื่อให้สามารถเข้าถึงได้จากทุกฟังก์ชัน
global FPS, SCREEN_RATIO, SCREEN_WIDTH, SCREEN_HEIGHT, font, white
global PIPE_GAP, PIPE_FREQUENCY, BG, GROUND_IMG, SCROLL_SPEED, GROUND_SCROLL, POP_SIZE
global MAX_PIPE, MAX_FITNESS

# ตั้งค่าเฟรมเรทของเกมให้เป็น 60 FPS (เฟรมต่อวินาที)
FPS = 60

# กำหนดอัตราส่วนของหน้าจอเกม
SCREEN_RATIO = 0.7
# กำหนดความกว้างและความสูงของหน้าจอเกม
SCREEN_WIDTH = SCREEN_RATIO * 864
SCREEN_HEIGHT = SCREEN_RATIO * 936

# กำหนดค่าตัวแปรต่าง ๆ ที่เกี่ยวข้องกับเกม
PIPE_GAP = 200  # ระยะห่างระหว่างท่อด้านบนและล่าง
PIPE_FREQUENCY = 1600  # ความถี่ในการสร้างท่อใหม่ (หน่วยเป็นมิลลิวินาที)

# โหลดภาพพื้นหลังและพื้นดินสำหรับเกม
BG = pygame.image.load('img/bg.png')
GROUND_IMG = pygame.image.load('img/ground.png')

# กำหนดความเร็วในการเลื่อนพื้นดิน (หน่วยพิกเซล)
SCROLL_SPEED = 4
GROUND_SCROLL = 0  # ตำแหน่งของการเลื่อนพื้นดิน

# (Population) นกที่ใช้ ใน NEAT ซึ่งใช้กำหนดจำนวน Bird ในแต่ละ generation
POP_SIZE = 5

# ตัวแปรสำหรับเก็บค่าท่อสูงสุดและค่า Fitness สูงสุดในแต่ละ generation
MAX_PIPE = 0
MAX_FITNESS = 0
