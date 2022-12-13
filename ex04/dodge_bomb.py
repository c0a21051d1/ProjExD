from itertools import count
import pygame as pg
import random
import sys
import time

def Clock():
    time_sta = time.time()
    time.sleep()
    time_end = time.perf_counter()
    tim = time_end-time_sta

def check_bound(obj_rct, scr_rct):
    # 第1引数：こうかとんrectまたは爆弾rect
    # 第2引数：スクリーンrect
    # 範囲内：+1／範囲外：-1
    yoko, tate = +1, +1
    global count
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:    #[追加]爆弾段々速くなる
        if count <8:
            yoko = -1.2
            tate = 1.2
            count +=1
        else:
            yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        if count <8:
            yoko = 1.2
            tate = -1.2
            count +=1
        else:
            tate = -1
    return yoko, tate


def main():
    
    pg.init()
    font = pg.font.Font(None,300)



    clock =pg.time.Clock()
    # 練習１
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600, 900))
    scrn_rct = scrn_sfc.get_rect()
    pgbg_sfc = pg.image.load("fig/pg_bg.jpg")
    pgbg_rct = pgbg_sfc.get_rect()

    # 練習３
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400
    # scrn_sfcにtori_rctに従って，tori_sfcを貼り付ける
    scrn_sfc.blit(tori_sfc, tori_rct) 

    # 練習５
    bomb_sfc = pg.Surface((40, 40)) # 正方形の空のSurface
    bomb_sfc.set_colorkey((0, 0, 0))
    pg.draw.circle(bomb_sfc, (0, 0, 255), (10, 10), 10)
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.centerx = random.randint(0, scrn_rct.width)
    bomb_rct.centery = random.randint(0, scrn_rct.height)
    scrn_sfc.blit(bomb_sfc, bomb_rct) 
    vx, vy = +1, +1

    
    # 練習２
    while True:
        scrn_sfc.blit(pgbg_sfc, pgbg_rct) 

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        # 練習4
        key_dct = pg.key.get_pressed() # 辞書型
        if key_dct[pg.K_UP]:
            tori_rct.centery -= 1
        if key_dct[pg.K_DOWN]:
            tori_rct.centery += 1
        if key_dct[pg.K_LEFT]:
            tori_rct.centerx -= 1
        if key_dct[pg.K_RIGHT]:
            tori_rct.centerx += 1
        if check_bound(tori_rct, scrn_rct) != (+1, +1):
             # どこかしらはみ出ていたら
            if key_dct[pg.K_UP]:
                tori_rct.centery += 1
            if key_dct[pg.K_DOWN]:
                tori_rct.centery -= 1
            if key_dct[pg.K_LEFT]:
                tori_rct.centerx += 1
            if key_dct[pg.K_RIGHT]:
                tori_rct.centerx -= 1       

        if key_dct[pg.K_b]:                             #[追加]bが押されている間、速さが二倍になる
            if key_dct[pg.K_UP]:
                tori_rct.centery -= 2
            if key_dct[pg.K_DOWN]:
                tori_rct.centery += 2
            if key_dct[pg.K_LEFT]:
                tori_rct.centerx -= 2
            if key_dct[pg.K_RIGHT]:
                tori_rct.centerx += 2
            if check_bound(tori_rct, scrn_rct) != (+1, +1):
                if key_dct[pg.K_UP]:
                    tori_rct.centery += 2
                if key_dct[pg.K_DOWN]:
                    tori_rct.centery -= 2
                if key_dct[pg.K_LEFT]:
                    tori_rct.centerx += 2
                if key_dct[pg.K_RIGHT]:
                    tori_rct.centerx -= 2
        scrn_sfc.blit(tori_sfc, tori_rct) 

        # 練習６
        bomb_rct.move_ip(vx, vy)
        scrn_sfc.blit(bomb_sfc, bomb_rct) 
        yoko, tate = check_bound(bomb_rct, scrn_rct)
        vx *= yoko
        vy *= tate

        #練習８
        if tori_rct.colliderect(bomb_rct):
            tori_sfc = pg.image.load("fig/1.png")
            tori_rct = tori_sfc.get_rect()
            tori_rct.center = tori_rct.centerx, tori_rct.centery
            
        
            pg.display.update()
            text = font.render("GAMEOVER", True, (0,0,0))            #[追加]着弾するとGAMEOVERが表示される
            scrn_sfc.blit(text,[200,400])
            pg.display.update()
            clock.tick(0.5)
            return
        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    count = 0
    main()
    
    pg.quit()
    sys.exit()