import pygame as pg
import sys

def main():
    clock = pg.time.Clock()

    pg.display.set_caption("初めてのPyGame")
    scrn_sfc = pg.display.set_mode((800,600))

    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc,0,2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 400,300
    #scrn_sfcにtori_rctに従って、tori_sfcを貼り付ける
    scrn_sfc.blit(tori_sfc,tori_rct) 

    pg.display.update()
    clock.tick(0.2)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()