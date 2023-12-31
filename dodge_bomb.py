import random
import sys
import time
import pygame as pg
WIDTH, HEIGHT = 1600, 900

def check_bound(obj_rct: pg.Rect):  # 練習３：画面内監禁関数
    """
    引数：こうかとんRect、爆弾Rect
    変数：side = 縦, ver = 横
    画面外だとside、verがFalseへ変換
    """
    side = True
    ver = True
    if obj_rct.left < 0 or obj_rct.right > WIDTH:
        side = False
    if obj_rct.top < 0 or obj_rct.bottom > HEIGHT:
        ver = False
    return side, ver
        
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # Issue#1修正
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)
    
    bd_img = pg.Surface((20, 20))  # 練習１：爆弾Surfaceを作成する
    bd_img.set_colorkey((0, 0, 0))  # 練習１：黒い部分を透明にする
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()  # 練習１：SurfaceからRectを抽出する
    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bd_rct.center = (x, y)  # 練習１：Rectにランダムな座標を設定する
    
    vx, vy = +5, +5  # 練習２：爆弾の速度
    delta = {pg.K_UP:(0, -5), pg.K_DOWN:(0, +5), pg.K_LEFT:(-5, 0), pg.K_RIGHT:(+5, 0)}
    
    kk_imgs = [pg.transform.rotozoom(kk_img, angle, 1) for angle in range(0, -360, -45)]
    ttl_mv = {(0, 0):kk_imgs[0], (-5, 0):kk_imgs[0], 
              (-5, -5):kk_imgs[1], (0, -5):pg.transform.flip(kk_imgs[2], True, False),
              (+5, -5):pg.transform.flip(kk_imgs[1], True, False), (+5, 0):pg.transform.flip(kk_imgs[4], False, True), 
              (+5, +5):pg.transform.flip(kk_imgs[7], True, False),
              (0, +5):kk_imgs[6], (-5, +5):kk_imgs[7]}  # 演習１
    
    accs = [a for a in range(1, 11)]  # 加速の値
    
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
        
    
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])
        if kk_rct.colliderect(bd_rct):  # 練習５：こうかとん爆散時
            kk_imgs = pg.image.load("ex02/fig/8.png")  # 演習３画像切り替え
            kk_imgs = pg.transform.rotozoom(kk_imgs, 0, 2.0)
            screen.blit(kk_imgs, kk_rct)
            pg.display.update()
            time.sleep(2)
            print("Game Over")
            return

 
        sum_mv = [0, 0]
        key_lst = pg.key.get_pressed()
        for key , mv in delta.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(ttl_mv[tuple(sum_mv)], kk_rct)   # 練習３：こうかとん動かす  演習１
        
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]  # 演習２　加速
        bd_rct.move_ip(avx, avy)  # 練習２：爆弾を移動させる
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1  # 練習４
        screen.blit(bd_img, bd_rct)  # 練習１：Rectを使って試しにblit
        
        tmr += 1
        
        pg.display.update()
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()