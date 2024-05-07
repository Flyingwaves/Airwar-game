import pygame
import sys
import traceback
from pygame.locals import *
import myplane
import enemy
import bullet
import supply
from random import *

pygame.init()
pygame.mixer.init()

bg_size = [480, 800]
screen = pygame.display.set_mode((480, 800), 0, 32)
pygame.display.set_caption("飞机大战--v1.0")
image_file_path = './pictures/background.png'
background = pygame.image.load(image_file_path).convert()

# RGB颜色显示，用于血条
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_large_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.LargeEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def inc_speed(target, inc):
    for each in target:
        each.speed += inc

def main():
    running = True

    # 生成我方飞机
    us = myplane.MyPlane([480, 800])

    # 生成敌方飞机
    enemies = pygame.sprite.Group()
    # 生成小飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)
    # 生成中飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 5)
    # 生成大飞机
    large_enemies = pygame.sprite.Group()
    add_large_enemies(large_enemies, enemies, 2)


    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 5
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(us.rect.midtop))  # 默认在顶部了

    # 生成超级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 10
    for i in range(BULLET2_NUM // 2):
        bullet2.append(bullet.Bullet2((us.rect.centerx - 33, us.rect.centery)))     # 后一个变量限制在飞机肚子处发射
        bullet2.append(bullet.Bullet2((us.rect.centerx + 30, us.rect.centery)))

    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    us_destroy_index = 0

    # 统计得分
    score = 0
    score_font = pygame.font.Font("./font/MoShangHuaKaiTi-2-1.ttf", 36)

    # 标志是否暂停游戏
    paused = False
    pause_nor_image = pygame.image.load("./pictures/game_pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("./pictures/game_pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("./pictures/game_resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("./pictures/game_resume_pressed.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = 480 - paused_rect.width - 10, 10
    paused_image = pause_nor_image

    # 设置难度级别
    level = 1

    # 全屏炸弹
    bomb_image = pygame.image.load("./pictures/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("./font/MoShangHuaKaiTi-2-1.ttf", 48)
    bomb_num = 5

    # 每30秒发放一个补给包
    bullet_supply = supply.Bullet_supply(bg_size)
    bomb_supply = supply.Bomb_supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)

    # 补给子弹计时
    DOUBLE_BULLET_TIME = USEREVENT + 1
    # 标志是否使用超级子弹
    is_double_bullet = False

    # 解除无敌状态计时器
    INVINCIBLE_TIME = USEREVENT + 2

    # 游戏结束画面
    gameover_font = pygame.font.Font("./font/MoShangHuaKaiTi-2-1.ttf", 48)
    again_image = pygame.image.load("./gameover_UI/game_again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("./gameover_UI/game_over.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()


    # 生命数量
    life_image = pygame.image.load("./pictures/life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    # 用于阻止重复打开记录文件
    recorded = False

    # 切换飞机图片，造成闪烁效果
    switch_image = True

    # 用于延迟
    delay = 100

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    # 解决暂停期间发放补给包的问题
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        # 暂停背景音乐及音效
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        # 恢复背景音乐及音效

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.alive = False
            elif event.type == SUPPLY_TIME:
                # 播放声音
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            elif event.type == INVINCIBLE_TIME:
                us.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)  # 计时器一直触发，相当于取消计时

        screen.blit(background, (0, 0))

        # 根据用户得分增加难度
        if level == 1 and score > 20000:
            level = 2
            # 增加3架小飞机，2架中飞机，1架大飞机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_large_enemies(large_enemies, enemies, 1)
            # 提升小型飞机的速度
            inc_speed(small_enemies, 1)

        elif level == 2 and score > 50000:
            level = 3
            # 增加5架小飞机，3架中飞机，2架大飞机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_large_enemies(large_enemies, enemies, 2)
            # 提升小型飞机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 150000:
            level = 4
            # 增加5架小飞机，3架中飞机，2架大飞机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_large_enemies(large_enemies, enemies, 2)
            # 提升小型飞机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 4 and score > 300000:
            level = 5
            # 增加5架小飞机，3架中飞机，2架大飞机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_large_enemies(large_enemies, enemies, 2)
            # 提升小型飞机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)

        if life_num and not paused:

            # 检测键盘操作
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_w] or key_pressed[K_UP]:
                us.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                us.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                us.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                us.moveRight()

            # 绘制全屏炸弹补给并检测是否获得
            if bomb_supply.alive:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, us):
                    # 捡到补给音效
                    if bomb_num < 5:
                        bomb_num += 1
                    bomb_supply.alive = False

            # 绘制子弹补给并检测是否获得
            if bullet_supply.alive:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, us):
                    # 捡到补给音效
                    # 发射双蛋
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)    # 捡到才开始计时，不是一开始就计时
                    bullet_supply.alive = False     # 供给包消失不是子弹消失

            global bullets
            # 生成子弹
            if not(delay % 10):

                # 播放子弹声音
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((us.rect.centerx - 33, us.rect.centery))
                    bullets[bullet2_index + 1].reset((us.rect.centerx + 30, us.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(us.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM


            # 检测子弹是否击中敌机
            for b in bullets:
                if b.alive:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.alive = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in large_enemies:
                                e.energy -= 1
                                e.hit = True
                                if e.energy == 0:
                                    e.alive = False
                            else:
                                e.alive = False

            # 绘制敌机
            # 绘制大型机
            for each in large_enemies:
                if each.alive:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 绘制血条
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5), 2)
                    # 当生命大于20% 显示绿色， 否则显示红色
                    energy_remain = each.energy / enemy.LargeEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5),
                            (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5),
                                     2)

                else:
                    # 毁灭
                    if not(delay % 3):
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            score += 10000
                            each.reset()    # 更改状态，就不会循环爆炸了


            # 绘制中型号机
            for each in mid_enemies:
                if each.alive:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # 绘制血条
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5), 2)
                    # 当生命大于20% 显示绿色， 否则显示红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5),
                                     2)
                else:
                    # 毁灭
                    if not(delay % 3):
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            each.reset()    # 更改状态，就不会循环爆炸了
            # 绘制小型机
            for each in small_enemies:
                if each.alive:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    if not (delay % 3):
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()  # 更改状态，就不会循环爆炸了

            # 检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(us, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not us.invincible:
                us.alive = False
                for e in enemies_down:
                    e.alive = False

            # 绘制我方飞机
            if us.alive:
                if switch_image:
                    screen.blit(us.image1, us.rect)
                else:
                    screen.blit(us.image2, us.rect)
            else:
                # 毁灭
                if not (delay % 3):
                    screen.blit(us.destroy_images[e1_destroy_index], us.rect)
                    us_destroy_index = (us_destroy_index + 1) % 4
                    if us_destroy_index == 0:
                        life_num -= 1
                        us.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)

            # 绘制炸弹数量
            bomb_text = bomb_font.render("x %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, bg_size[1] - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, bg_size[1] - 10 - text_rect.height))

            # 绘制剩余生命数量
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, (bg_size[0] - 10 - (i + 1) * life_rect.width,
                                bg_size[1] - 10 - life_rect.height))

            # 绘制得分
            score_text = score_font.render("Score : %s" % str(score), True, WHITE)
            screen.blit(score_text, (10, 5))

        # 绘制游戏结束画面
        elif life_num == 0:
            # 背景音乐停止
            # 停止全部音效
            # 停止发放补给
            pygame.time.set_timer(SUPPLY_TIME, 0)

            if not recorded:
                recorded = True
                # 读取历史记录
                with open("record.txt", "r") as f:      # with open用法会在使用文件后自动关闭
                    record_score = int(f.read())
                # 如果得分可以更新，进行存档
                if score > record_score:
                    with open("record.txt", "w") as f:
                        f.write(str(score))

            # 绘制结束界面
            record_score_text = score_font.render("Best : %d" % record_score, True, WHITE)
            screen.blit(record_score_text, (50, 50))

            gameover_text1 = gameover_font.render("Your Score", True, WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                (bg_size[0] - gameover_text1_rect.width) // 2, 300
            # 这里高度向的位置（后一个参数300），视频没给，自己估了个大概，有时间可以想一想，用一个公式定好位置
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, WHITE)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                (bg_size[0] - gameover_text2_rect.width) // 2, gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                (bg_size[0] - again_rect.width) // 2, gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                (bg_size[0] - gameover_rect.width) // 2, again_rect.bottom + 50
            screen.blit(gameover_image, gameover_rect)

            # 检测用户的鼠标操作
            # 如果按下左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                if again_rect.left < pos[0] < again_rect.right and \
                        again_rect.top < pos[1] < again_rect.bottom:
                    main()
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                        gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()

            # running = False



        # 绘制暂停按钮
        screen.blit(paused_image, paused_rect)

        # 切换图片
        if not(delay % 5):
            switch_image = not switch_image     # 实现每5帧切换一次

        delay -= 1      # 一帧减1
        if not delay:
            delay = 100

        pygame.display.flip()

        clock.tick(60)      # 1秒60帧

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()

# def start():
#     # 创建窗口，显示内容
#     screen = pygame.display.set_mode((480, 800), 0, 32)
#     # 根据窗口创建一个图片背景
#     image_file_path = './pictures/background.png'
#     background = pygame.image.load(image_file_path).convert()
#     # 背景图片显示
#     while(True):
#         screen.blit(background, (0, 0))
#         pygame.display.update()
# if __name__ == '__main__':
#     start()
# from pygame.locals import *
# for event in pygame.event.get():
#     if event.type == QUIT:
#         print("exit")
#         exit()
#     elif event.type == KEYDOWN:
#         if event.key == K_a or event.key == K_LEFT:
#             print('left')
#         elif event.key == K_d or event.key == K_RIGHT:
#             print('right')
#         elif event.key == K_SPACE:
#             print('space')