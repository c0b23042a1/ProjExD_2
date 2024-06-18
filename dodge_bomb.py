import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5), 
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
} 

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数: こうかとんRectか爆弾Rect
    戻り値: タプル(横方向判定結果, 縦方向判定結果)
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: #  横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: #  縦方向判定
        tate = False
    return yoko, tate

def way(kk_img: pg.image) ->dict:
    """
    引数: こうかとんimage
    戻り値: 辞書
    """
    kk_way = { 
        (0, 0): kk_img,
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5, 5): pg.transform.rotozoom(kk_img, 45, 1.0),
        (0, -5): pg.transform.flip(pg.transform.rotozoom(kk_img, 90, 1.0), False, True),
        (5, -5): pg.transform.flip(pg.transform.rotozoom(kk_img, 135, 1.0), False, True),
        (5, 0): pg.transform.flip(pg.transform.rotozoom(kk_img, 180, 1.0), False, True),
        (5, 5): pg.transform.flip(pg.transform.rotozoom(kk_img, 225, 1.0), False, True),
        (0, 5): pg.transform.flip(pg.transform.rotozoom(kk_img, 270, 1.0), False, True),
        (-5, -5): pg.transform.rotozoom(kk_img, 315, 1.0),
    }
    return kk_way

def addiction(tmr):
    accs = [a for a in range(1, 11)]


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    kk_way = way(kk_img)

    enn = pg.Surface((20, 20))
    pg.draw.circle(enn, (255, 0, 0), (10, 10), 10)
    enn.set_colorkey((0, 0, 0))
    enn_rct = enn.get_rect()
    enn_rct.center = random.randint(0, WIDTH),random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 移動速度

    clock = pg.time.Clock()
    tmr = 0
    accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        enn = pg.Surface((20*r, 20*r))
        pg.draw.circle(enn, (255, 0, 0), (10*r, 10*r), 10*r)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(enn_rct): #  衝突判定
            return #  gemeover
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]

        kk_img = kk_way.get(tuple(sum_mv), kk_img)  # kk_imgの更新
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        enn_rct.move_ip(vx, vy)
        yoko, tate = check_bound(enn_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(enn, enn_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
