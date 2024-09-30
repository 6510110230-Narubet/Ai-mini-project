import pygame
from pygame.locals import *
from Bird import Bird
from Pipe import Pipe
import random
import setting
import os
import math
import sys
import neat

# เริ่มต้นการทำงานของ Pygame
pygame.init()

# ตั้งค่า clock สำหรับควบคุมเฟรมเรท
clock = pygame.time.Clock()

# สร้างหน้าต่างของเกม
screen = pygame.display.set_mode((setting.SCREEN_WIDTH, setting.SCREEN_HEIGHT))
pygame.display.set_caption('NEAT - Flappy Bird')

# กำหนดฟอนต์ที่ใช้ในเกม
font = pygame.font.SysFont('Bauhaus 93', 60)
font2 = pygame.font.Font('freesansbold.ttf', 20)
font3 = pygame.font.Font('freesansbold.ttf', 30)

# กำหนดสีต่างๆ ที่ใช้ในเกม
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# ฟังก์ชันสำหรับแสดงข้อความบนหน้าจอ
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# ฟังก์ชันคำนวณระยะห่างระหว่างสองจุด
def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx**2 + dy**2)

# ฟังก์ชันแสดงสถิติในเกม เช่น จำนวน bird ที่รอด จำนวน generation
def statistics():
    global birds, ge

    stats_text = []
    stats_text.append(font2.render(f'Bird Alive:  {str(len(birds))}', True, (0, 0, 0)))
    stats_text.append(font2.render(f'Generation:  {pop.generation+1}', True, (0, 0, 0)))
    stats_text.append(font2.render(f'Scroll Speed:  {str(setting.SCROLL_SPEED)}', True, (0, 0, 0)))
    stats_text.append(font2.render(f'Max Pipe:  {str(setting.MAX_PIPE)}', True, (0, 0, 0)))
    stats_text.append(font2.render(f'Max Fitness:  {str(setting.MAX_FITNESS)}', True, (0, 0, 0)))

    for i, text in enumerate(stats_text):
        screen.blit(text, (50, 500 + (i * 25)))

# ฟังก์ชันลบ bird ที่แพ้ออกจากกลุ่ม
def remove(idx):
    birds.pop(idx)
    ge.pop(idx)
    nets.pop(idx)

# ฟังก์ชันหลักที่ใช้ในการประเมิน bird ในแต่ละ genome
def eval_genomes(genomes, config):
    global pipe_group, birds, ge, nets, MAX_FITNESS, MAX_PIPE

    # สร้างกลุ่มของ pipe และ bird
    pipe_group = pygame.sprite.Group()
    birds = []
    ge = []
    nets = []

    # เริ่มต้น bird และ genome แต่ละตัว
    for genome_id, genome in genomes:
        flappy = Bird(100, int(setting.SCREEN_HEIGHT / 2))
        bird_group = pygame.sprite.Group()
        bird_group.add(flappy)
        birds.append((flappy, bird_group))

        genome.fitness = 0  # เริ่มค่า fitness ที่ 0
        ge.append(genome)

        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)

    LAST_PIPE = pygame.time.get_ticks() - setting.PIPE_FREQUENCY
    PASS_PIPE = False

    # เริ่มต้นเกม
    run = True
    while run:
        clock.tick(setting.FPS)  # จำกัดเฟรมเรท

        # วาดพื้นหลัง
        screen.blit(setting.BG, (0, 0))

        # วาด pipe และ bird
        pipe_group.draw(screen)
        for i, (flappy, bird_group) in enumerate(birds):
            bird_group.draw(screen)
            bird_group.update()
            pygame.draw.rect(screen, flappy.color, (flappy.rect.x, flappy.rect.y, flappy.rect.width, flappy.rect.height), 2)

            # วาดเส้นจาก bird ไปยัง pipe เพื่อใช้ในการคำนวณระยะ
            if len(pipe_group) > 0:
                pygame.draw.line(screen, flappy.color, (flappy.rect.x + 54, flappy.rect.y + 12), pipe_group.sprites()[0].rect.midtop, 2)
                pygame.draw.line(screen, flappy.color, (flappy.rect.x + 54, flappy.rect.y + 12), pipe_group.sprites()[1].rect.midbottom, 2)
            
            ge[i].fitness += 1  # เพิ่ม fitness ให้กับ bird ที่รอด

        # วาดและเลื่อนพื้น
        screen.blit(setting.GROUND_IMG, (setting.GROUND_SCROLL, 0.9 * setting.SCREEN_HEIGHT))

        # ตรวจสอบคะแนนและความสำเร็จของ bird
        for i, (flappy, bird_group) in enumerate(birds):
            if len(pipe_group) > 0:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and PASS_PIPE == False:
                    PASS_PIPE = True
                if PASS_PIPE == True:
                    if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                        flappy.pipe_passed += 1
                        ge[i].fitness += 100  # ให้คะแนนเพิ่มเมื่อผ่าน pipe
                        PASS_PIPE = False

        # อัปเดตค่า fitness สูงสุด
        mx_fitness = max([g.fitness for g in ge])
        text = font3.render(f'Gen. Fitness:  {str(mx_fitness)}', True, (0, 0, 0))
        screen.blit(text, (50, 30))
        setting.MAX_FITNESS = max([setting.MAX_FITNESS, mx_fitness])

        # อัปเดตค่า pipe สูงสุดที่ bird ผ่าน
        mx_pipe = max([flappy.pipe_passed for flappy, _ in birds])
        text = font3.render(f'Gen. Pipe:  {str(mx_pipe)}', True, (0, 0, 0))
        screen.blit(text, (50, 80))
        setting.MAX_PIPE = max([setting.MAX_PIPE, mx_pipe])

        # ตรวจสอบการชนและสถานะของ bird
        for i, (flappy, bird_group) in enumerate(birds):
            # ตรวจสอบการชนกับ pipe
            if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
                flappy.game_over = True

            # ถ้าบินออกนอกหน้าจอ
            if flappy.rect.top < 0 or flappy.rect.bottom >= setting.SCREEN_WIDTH:
                flappy.game_over = True
                flappy.flying = False

        # สร้าง pipe ใหม่
        time_now = pygame.time.get_ticks()
        if time_now - LAST_PIPE > setting.PIPE_FREQUENCY:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(setting.SCREEN_WIDTH, int(setting.SCREEN_HEIGHT / 2) + pipe_height, -1)
            top_pipe = Pipe(setting.SCREEN_WIDTH, int(setting.SCREEN_HEIGHT / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            LAST_PIPE = time_now

        pipe_group.update()

        # เลื่อนพื้น
        setting.GROUND_SCROLL -= setting.SCROLL_SPEED
        if abs(setting.GROUND_SCROLL) > 35:
            setting.GROUND_SCROLL = 0
        
        # ลบ bird ที่ game over ออกจากเกม
        for i, (flappy, bird_group) in enumerate(birds):
            if flappy.game_over:
                remove(i)

        # ตรวจสอบการกระทำของ neural network
        for i, (flappy, bird_group) in enumerate(birds):
            flappy_position = (bird_group.sprites()[0].rect.x, bird_group.sprites()[0].rect.y)
            output = nets[i].activate((bird_group.sprites()[0].rect.y, 
                                       distance(flappy_position, pipe_group.sprites()[0].rect.midtop),
                                       distance(flappy_position, pipe_group.sprites()[1].rect.midbottom)))
            if output[0] > 0.5:
                flappy.clicked = True

        # ตรวจสอบเหตุการณ์ในเกม
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

        # จบเกมเมื่อไม่มี bird เหลือ
        if len(birds) <= 0:
            break
        
        # แสดงสถิติบนหน้าจอ
        statistics()
        pygame.display.update()

# ตั้งค่า NEAT Neural Network และเริ่มเกม
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(eval_genomes, 50)

# เริ่มต้นโปรแกรม
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
