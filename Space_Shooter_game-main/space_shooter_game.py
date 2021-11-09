import pygame
import random
#import module
import os, sys
# lấy ra đường dẫn đến thư mục modules ở trong projetc hiện hành
lib_path = os.path.abspath(os.path.join('modules'))
# thêm thư mục cần load vào trong hệ thống
sys.path.append(lib_path)
# import module
from modules.LASER import *
from modules.SHIP import *
from modules.ACTOR import *
from modules.PLAYER import *
from modules.ENEMY import *
pygame.font.init()
WIDTH, HEIGHT = 600, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Game")
def main():
    #khoi tao ct
    run = True
    FPS = 60
    level = 0
    lives = 5
    enemies = []
    wave_length = 5
    enemy_vel = 1
    player_vel = 5
    laser_vel = 6
    global score
    score = 0
     # khởi tạo player
    player = Player(275, 375)
    #khoi tao font
    main_font = pygame.font.SysFont("comicsans", 25)
    lost_font = pygame.font.SysFont("comicsans", 40)
    smallText = pygame.font.SysFont("comicsansms",20)
    clock = pygame.time.Clock()
    lost = False
    lost_count = 0

    #giao dien khi choi game
    def redraw_window():
        WIN.blit(BG_ingame, (0,0))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        player.draw(WIN)
        WIN.blit(lives_label, (10, 10))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        total = main_font.render(f"Score: {score}", 1, (255,255,255))
        text_pause = main_font.render("press 'esc' to pause", 1, (255,255,255))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 15, 10))
        WIN.blit(total, (WIDTH - level_label.get_width() - 15, 35))
        WIN.blit(text_pause, (10, 470))


        for enemy in enemies:
            enemy.draw(WIN)
        #thong bao khi thua
        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            total = smallText.render(f"Score:{score}", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 250))
            WIN.blit(total, (WIDTH/2 - total.get_width()/2, 380))

        pygame.display.update()



    while run:                                                                #Playing program
        clock.tick(FPS)
        redraw_window()
                                                                                    # player->
        ## thua
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        ## tau di chuyen va ban
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        #pause game
        if keys[pygame.K_ESCAPE]:
            paused()
        if lost:
            if lost_count > FPS * 5:
                run = False
            else:
                continue
        #  tuong tac cua anemy
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            #enemy ban
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
            #va cham giua player voi enemy, va khi tau di het map
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
                score += 1
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        # tau ban
        player.cooldown()
        for laser in player.lasers:
            laser.move(-laser_vel)
            if laser.off_screen(HEIGHT):
                player.lasers.remove(laser)
            else:
                for enemy in enemies:
                    if laser.collision(enemy):
                        enemies.remove(enemy)
                        score += 1
                        if laser in player.lasers:
                            player.lasers.remove(laser)


        # sinh tau enemy moi khi het dot tan cong
        if len(enemies) == 0:                                                   #Common run for both
            level += 1  ## tang lv choi
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-80), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def main_menu():
    # giao dien luc bat dau vo game
    title_font = pygame.font.SysFont("comicsans", 25)

    run = True
    while run:
        WIN.blit(BG_ingame, (0,0))

        title_label = title_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 250))
        title_label2 = title_font.render("Press esc to exit...", 1, (255,255,255))
        WIN.blit(title_label2, (10, 470))

        player = Player(275, 375)
        player.draw(WIN)
        #tuong tac truoc khi vao game
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # sukien bam nut X
                pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]: #bam nut esc de thoat ve menu
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN: # nhan chuot
                main()


# pause game
def paused():
    largeText = pygame.font.SysFont("comicsansms",75)
    smallText = pygame.font.SysFont("comicsansms",20)
    text = largeText.render("Paused",1,(255,255,255))
    text2= smallText.render("Press 'o' to continue or 'Backspace' to re turn menu",1,(255,255,255))
    WIN.blit(text, (WIDTH/2 - text.get_width()/2, 190))
    WIN.blit(text2, (WIDTH/2 - text2.get_width()/2, 290))
    pygame.display.update()
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # skien an nut X
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_o]: #an o de tiep tuc
            pause = False
        if keys[pygame.K_BACKSPACE]: #backspace de ve menu
            intro()

#tạo button ở đầu menu
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    smallText = pygame.font.SysFont("comicsansms",20)
    text = smallText.render(msg,1,(255,255,255))

    if x+w > mouse[0] > x and y+h > mouse[1] > y: #di chuot vao button thi doi mau
        pygame.draw.rect(WIN, ac,(x,y,w,h))

        if click[0] == 1 and action == "start": #neu click vao button start
            main_menu()
            WIN.blit(BG, (0,0))
        if click[0] == 1 and action == "exit": #neu click vao button exit
            pygame.quit()

    else:
        pygame.draw.rect(WIN, ic,(x,y,w,h))

    WIN.blit(text, (WIDTH/2 - text.get_width()/2, ((y+(h/2))-17)) )
    pygame.display.update()

#giao dien menu chinh
def intro():

    WIN.blit(BG, (0,0))

    main_font = pygame.font.SysFont("comicsans", 28)
    text = main_font.render("SPACE SHOOTER", 1, (0,0,0))
    WIN.blit(text, (225, 100))
    text1 = main_font.render("made by N1 PTIT", 1, (0,0,0))
    WIN.blit(text1, (225, 400))
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #nhan x de tat
                run = False


        button("Play",215,200,170,50,(0,0,0),(90,90,90),"start")
        button("Exit",250,335,100,50,(0,0,0),(90,90,90),"exit")

    pygame.quit()

intro()                                                                     #run