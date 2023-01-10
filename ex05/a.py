import pygame as pg
import sys
import random
from pygame.locals import * 
import time


### Screenクラス
class Screen:
    def __init__(self, title, wh, img_path):
        pg.display.set_caption(title)               # "逃げろ！こうかとん"
        self.sfc = pg.display.set_mode(wh)          # (1600/2, 900/2)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(img_path)      # "fig/pg_bg.png"
        self.bgi_sfc = pg.transform.rotozoom(self.bgi_sfc, 0, 0.5)      # 背景画像を0.5倍の大きさにする
        self.bgi_rct = self.bgi_sfc.get_rect()
    
    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)


### Birdクラス
class Bird:
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    def __init__(self, img_path, ratio, xy):
        self.sfc = pg.image.load(img_path)                      # "fig/3.png"
        self.sfc = pg.transform.rotozoom(self.sfc, 0, ratio)    # こうかとんの拡大縮小
        self.rct = self.sfc.get_rect()
        self.rct.center = xy                                    # w/2, h/2
    
    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)
    
    def update(self, scr:Screen):
        key_dct = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_dct[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
            if check_bound(self.rct, scr.rct) != (+1, +1):
                self.rct.centerx -= delta[0]
                self.rct.centery -= delta[1]
        self.blit(scr)


### Bombクラス
class Bomb:
    count = 0
    hantei = []
    def __init__(self, color, rad, vxy, scr:Screen):
        self.sfc = pg.Surface((2*rad, 2*rad)) # 正方形の空のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(10, scr.rct.width-10)
        self.rct.centery = random.randint(10, scr.rct.height-10)
        #self.vx = vxy[0]
        #self.vy = vxy[1]
        self.vx, self.vy = vxy
        self.count = Bomb.count
        Bomb.hantei.append(True)
        Bomb.count += 1

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)
    
    def update(self, scr:Screen):
        if Bomb.hantei[self.count]:
            self.rct.move_ip(self.vx, self.vy)
            yoko, tate = check_bound(self.rct, scr.rct)
            self.vx *= yoko
            self.vy *= tate
            self.blit(scr)


# Timerクラス
class Timer:
    def __init__(self, font):
        self.font = font
        self.timer = int(pg.time.get_ticks()/1000)
        self.text = self.font.render(str(self.timer), True, "red")
        self.rct = self.text.get_rect(center=(40, 30))

    def update(self, scr:Screen):
        self.timer = int(pg.time.get_ticks()/1000)
        self.text = self.font.render(str(self.timer), True, "red")
        scr.sfc.blit(self.text, self.rct)    # タイマーのテキスト


### Shotクラス（攻撃）
class Shot(pg.sprite.Sprite):
    speed = -11
    hantei = True
    def __init__(self, image):
        self.sfc = pg.image.load(image)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, 0.05)    # 拡大縮小
        self.rct = self.sfc.get_rect()
        self.x, self.y = -5, -5
    
    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)
    
    def go(self, scr:Screen, bird:Bird):
        if Shot.hantei:
            Shot.hantei = False
            self.x = bird.rct.centerx
            self.y = bird.rct.centery
            self.rct.center = (self.x, self.y)
            self.blit(scr)
    
    def update(self, scr:Screen):
        if Shot.hantei != True:
            if self.y < -10:
                Shot.hantei = True
                return
            self.y += Shot.speed
            self.rct.move_ip(0, Shot.speed)
            self.blit(scr)
        else:
            self.rct.move(-100, -100)


# Textクラス
class Text:
    def __init__(self, font, txt, xy, color, scr:Screen):
        self.font = font
        self.color = color
        self.timer = int(pg.time.get_ticks()/1000)
        self.text = self.font.render(str(txt), True, self.color)
        self.rct = self.text.get_rect()
        self.rct.center = xy 

    def blit(self, scr:Screen):
        scr.sfc.blit(self.text, self.rct)    # タイマーのテキスト
    
    def update(self, txt, scr:Screen):
        self.text = self.font.render(str(txt), True, self.color)
        scr.sfc.blit(self.text, self.rct)


### チェック関数
def check_bound(obj_rct, scr_rct):
    """
    第1引数：こうかとんrectまたは爆弾rect
    第2引数：スクリーンrect
    範囲内：+1／範囲外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


### メイン関数
def main():
    # 爆弾の総個数
    bomb_number = 30
    # 何秒ごとに爆弾が増える
    bomb_plus = 1

    clock = pg.time.Clock()

    # 練習１
    (w, h) = (int(1600/2), int(900/2))                              # ウィンドウサイズ
    scr = Screen("逃げろ！こうかとん", (w ,h), "fig/pg_bg.jpg")       # Screenクラス

    # 練習３
    (cx, cy) = (w/2, h/2)   # キャラクターの座標
    kkt = Bird("fig/6.png", 1.0, (cx, cy))
    # scrn_sfcにtori_rctに従ってtori_sfcを貼り付ける
    kkt.blit(scr)

    # 練習５（爆弾の作成）
    bomb_draw = 1       # 爆弾の描画個数
    timer_hantei = 0    # 時間判定のための変数
    bombs = []
    # 色をランダムで生成
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(bomb_number)]
    for i in range(bomb_number):
        color = colors[i]
        vx = random.choice([-1, +1])
        vy = random.choice([-1, +1])
        bombs.append(Bomb(color, 10, (vx, vy), scr))

    # 時間の作成
    font = pg.font.Font(None, 60)
    tim = Timer(font)

    # カウントテキスト
    bomb_count = 0
    count_text = Text(font, str(bomb_count)+"/"+str(bomb_number), (w-65, 30), "darkgreen", scr)

    # 攻撃の作成
    gun = Shot("fig/shot.png")

    # ゲームオーバー
    font = pg.font.Font(None, 120)
    end_text = Text(font, "Game Over", (w/2 ,h/2), "red", scr)

    # クリア
    clear_text = Text(font, "Game Clear", (w/2, h/2), "blue", scr)

    while True:
        scr.blit()      # scrn_sfc.blit()
        # タイマーの表示
        tim.update(scr)

        # 処理が重すぎて断念
        """
        # 30秒経ったら背景の変更
        if tim.timer >= 15:
            scr.bgi_sfc = pg.image.load("fig/hell.jpg")
            scr.bgi_sfc = pg.transform.rotozoom(scr.bgi_sfc, 0, 0.5)
        """

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                # Spaceが押されたら攻撃
                if event.key == K_SPACE:
                    gun.go(scr, kkt)

        # こうかとんと攻撃のアップデート
        kkt.update(scr)
        gun.update(scr)
        count_text.update(str(bomb_count)+"/"+str(bomb_number), scr)

        # クリア判定（破壊した爆弾の個数==爆弾総数）
        if bomb_count == bomb_number:
                if True not in Bomb.hantei:
                    clear_text.blit(scr)    # Game Clearのテキスト
                    pg.display.update()         # 画面更新
                    time.sleep(2)               # 2秒後に以下を実行
                    return
        
        for i in range(bomb_draw):
            # こうかとんと爆弾の衝突判定
            bombs[i].update(scr)
            if kkt.rct.colliderect(bombs[i].rct): 
                end_text.blit(scr)    # Game Overのテキスト
                pg.display.update()         # 画面更新
                time.sleep(2)               # 2秒後に以下を実行
                return

            # 爆弾と攻撃の衝突判定
            if bombs[i].rct.colliderect(gun.rct):
                if Bomb.hantei[bombs[i].count]:
                    Bomb.hantei[bombs[i].count] = False
                    bomb_count += 1
        
        # 一定時間毎に描画する爆弾の数を増やす
        if int(tim.timer) % bomb_plus == 0 and bomb_draw < bomb_number and timer_hantei != tim.timer:
            bomb_draw += 1
            timer_hantei = tim.timer

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()  # main関数の呼び出し
    pg.quit()
    sys.exit()