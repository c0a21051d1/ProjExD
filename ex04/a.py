import pygame as pg
import sys
import random
import time


def main():
    # ウィンドウ設定
    (w, h) = (int(1600/2), int(900/2))             # 画面サイズ
    pg.init()                       # pygameの初期化
    pg.display.set_mode((w, h))     # 画面設定
    screen = pg.display.get_surface()
    scrn_rct = screen.get_rect()
    pg.display.set_caption("逃げろ！こうかとん")    # ウィンドウのタイトル設定
    bg = pg.image.load("fig/pg_bg.jpg")  # 背景画像取得
    bg = pg.transform.rotozoom(bg, 0, 0.5)
    rect_bg = bg.get_rect()
    (cx, cy) = (w/2, h/2)   # キャラクターの座標
    tori = pg.image.load("fig/3.png")
    tori_cry = pg.image.load("fig/8.png")
    #animal = pg.transform.rotozoom(animal, 0, 0.2)

    bomb_number = 5     # 爆弾の総個数
    bomb_draw = 1       # 爆弾の描画個数

    seqx = list(range(10, int(cx)-80)) + list(range(int(cx)+80, w-10))    # キャラクターの初期位置を避けたx座標のリスト
    seqy = list(range(10, int(cy)-80)) + list(range(int(cy)+80, h-10))    # キャラクターの初期位置を避けたy座標のリスト
    random_x = [random.choice(seqx) for i in range(bomb_number)]    # 爆弾の初期位置のx座標のリスト
    random_y = [random.choice(seqy) for i in range(bomb_number)]    # 爆弾の初期位置のy座標のリスト
    v = 1  # 初期速度
    l = [-v, v]
    vx = random.choices(l, k=bomb_number)   # x座標の進む方向リスト
    vy = random.choices(l, k=bomb_number)   # y座標の進む方向リスト

    # 爆弾の描画設定
    bomb_sfc = pg.Surface((20, 26))     # 正方形の空のSurface
    bomb_sfc.set_colorkey((0, 0, 0))
    circle = pg.draw.circle(bomb_sfc, "red", (10, 16), 10)      # 爆弾の丸部分を描画
    cord = pg.draw.rect(bomb_sfc, "red", (8, 0, 4, 8))   # 爆弾の紐部分を描画
    bomb_rct = bomb_sfc.get_rect()

    # 文字の設定
    font = pg.font.Font(None, 120)
    end_text = font.render("Game Over", True, "red")
    end_text_rect = end_text.get_rect(center=(w//2, h//2))
    font2 = pg.font.Font(None, 60)

    timer_hantei1 = 0   # 特定のタイマーの値を一時的に保持するための変数1
    timer_hantei2 = 0   # 特定のタイマーの値を一時的に保持するための変数2
    score = 0           # ゲームスコアを格納する変数

    start(screen, bg, rect_bg, w, h, score)    # スタート画面の表示
    last_game_ended = int(pg.time.get_ticks()/1000)     # スタートまでの経過時間を格納


    while True:
        # タイマーの設定
        now = int(pg.time.get_ticks()/1000)
        timer = now-last_game_ended
        timer_text = font2.render(str(timer), True, "red")
        timer_text_rect = timer_text.get_rect(center=(40, 30))
        screen.blit(timer_text, timer_text_rect)    # タイマーのテキスト

        # 30秒経ったら背景を地獄に変更
        if timer >= 30:
            bg = pg.image.load("fig/hell.jpg")
            bg = pg.transform.rotozoom(bg, 0, 0.5)
        
        pg.display.update()         # 画面更新
        pg.time.wait(30)            # 更新時間感覚
        screen.blit(bg, rect_bg)    # 背景画像の描画
        rect_tori = tori.get_rect(center=(cx, cy))  # こうかとん画像の座標設定
        screen.blit(tori, rect_tori)   # こうかとん画像の描画
        clock = pg.time.Clock()
        clock.tick(1000)

        # 終了用のイベント処理
        for event in pg.event.get():
            if event.type == pg.QUIT:           # 閉じるボタンが押された時
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:        # キーが押された時
                if event.key == pg.K_ESCAPE:    # Escキーが押された時
                    pg.quit()
                    sys.exit()
        
        # キャラクターの移動処理
        pressed_key = pg.key.get_pressed()
        if pressed_key[pg.K_RIGHT]:
            cx += 10
            if cx > w-20:
                cx = w-20
        if pressed_key[pg.K_LEFT]:
            cx -= 10
            if cx < 20:
                cx = 20
        if pressed_key[pg.K_UP]:
            cy -= 10
            if cy < 20:
                cy = 20
        if pressed_key[pg.K_DOWN]:
            cy += 10
            if cy > h-20:
                cy = h-20
        
        # 爆弾
        for i in range(bomb_draw):
            # 何秒か毎に速度を上げる
            if int(timer) % 5 == 0 and timer != 0 and timer_hantei1 != timer:
                vx[i] = (abs(vx[i]) + 1) * (abs(vx[i])/vx[i])
                vy[i] = (abs(vy[i]) + 1) * (abs(vy[i])/vy[i])
            # 何秒か毎に爆弾の数を(一定数になるまで)１ずつ増やす
            if int(timer) % 8 == 0 and bomb_draw < bomb_number and timer_hantei2 != timer:
                bomb_draw += 1
                timer_hantei2 = timer
            
            # 爆弾描画
            bomb_rct.center = random_x[i], random_y[i]+3
            screen.blit(bomb_sfc, bomb_rct)
            # 進む方向
            yoko, tate =  check_bound(bomb_rct, scrn_rct)
            vx[i] *= yoko
            vy[i] *= tate
            random_x[i] += vx[i]
            random_y[i] += vy[i]
        
            # 衝突判定
            if rect_tori.colliderect(bomb_rct):
                screen.blit(bg, rect_bg)    # 背景画像の描画
                screen.blit(tori_cry, rect_tori)   # 悲しみのこうかとん画像の描画
                screen.blit(end_text, end_text_rect)    # Game Overのテキスト
                pg.display.update()         # 画面更新
                time.sleep(2)               # 2秒後に以下を実行
                
                if score < timer:       # timerがscoreより大きかったら
                    score = timer       # 最高スコア更新
                bg = pg.image.load("fig/pg_bg.jpg")  # 背景の再設定
                bg = pg.transform.rotozoom(bg, 0, 0.5)
                start(screen, bg, rect_bg, w, h, score)        # スタート画面の関数

                # 変数の初期化
                (cx, cy) = (w/2, h/2)
                random_x = [random.choice(seqx) for i in range(bomb_number)]    # 爆弾の初期位置のx座標のリスト
                random_y = [random.choice(seqy) for i in range(bomb_number)]    # 爆弾の初期位置のy座標のリスト
                vx = random.choices(l, k=bomb_number)       # x座標の進む方向リスト
                vy = random.choices(l, k=bomb_number)       # y座標の進む方向リスト
                now = int(pg.time.get_ticks()/1000)         # プログラム実行からの時間
                last_game_ended = now                       # 上記を変数に格納
                timer_hantei1, timer_hantei2 = 0, 0
                bomb_draw = 1
                continue
            
        timer_hantei1 = timer


def check_bound(obj_rct, scr_rct):
    # 第１引数：こうかとんrectまたは爆弾rect
    # 第２引数：スクリーンrect
    # 範囲内：+1／範囲外：-1
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


# スタート画面の処理関数
def start(screen, bg, rect_bg, w, h, score):
    font = pg.font.SysFont("hg正楷書体pro", 70)                         # フォント設定
    font2 = pg.font.SysFont("hg正楷書体pro", 30)                         # フォント設定
    title_text = font.render("逃げろ！こうかとん", True, "darkgreen")    # ゲームタイトルテキスト
    title_text_rect = title_text.get_rect(center=(w//2, h//2-100))      # タイトルrect
    start_text = font.render("Start", True, "seagreen")                 # スタートボタンテキスト
    start_text_rect = start_text.get_rect(center=(w//2, h//2+90))       # スタートrect
    score_text = font2.render("スコア：" + str(score), True, "blue")                   # スコアテキスト
    score_text_rect = score_text.get_rect()            # スコアrect

    while True:
        pg.display.update()         # 画面更新
        pg.time.wait(30)            # 更新時間感覚
        screen.blit(bg, rect_bg)    # 背景画像の描画
        screen.blit(score_text, score_text_rect)    # スコアのテキスト
        screen.blit(title_text, title_text_rect)    # ゲームタイトルのテキスト
        pg.draw.rect(screen, "white", (150, h/2+50, w-300, 80))     # スタートボタン用の白い四角形を描画
        screen.blit(start_text, start_text_rect)    # ゲームスタートのテキスト

        for event in pg.event.get():
            # 終了用のイベント処理
            if event.type == pg.QUIT:           # 閉じるボタンが押された時
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:        # キーが押された時
                if event.key == pg.K_ESCAPE:    # Escキーが押された時
                    pg.quit()
                    sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:    # マウスのボタンが押された時
                if event.button == 1:               # 左クリックが押された時
                    place = pg.mouse.get_pos()      # マウスの座標を取得
                    if 150 < place[0] < w-150:      # マウスのx座標がスタートボタンのx座標の範囲内だったら
                        if h/2+50 < place[1] < h/2+130:     # マウスのy座標がスタートボタンのy座標の範囲内だったら
                            return                          # スタート画面を終了


if __name__ == "__main__":
    main()  # main関数の呼び出し