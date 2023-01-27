import pygame as pg
from copy import deepcopy
from random import choice, randrange

W, H = 10, 20
TILE = 45
window_w, window_h = W*TILE, H*TILE
FPS = 25

pg.init()

game_sc = pg.display.set_mode((window_w, window_h))
clock = pg.time.Clock()

grid = [pg.Rect(x*TILE, y*TILE, TILE, TILE) for x in range(W) for y in range(H)]

an_count, an_speed, an_limit = 0, 100, 2000

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pg.Rect(x + W//2, y+1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pg.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for j in range(H)]
figure = deepcopy(choice(figures))

def borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

while True:
    dx, rotate = 0, False
    game_sc.fill(pg.Color('black'))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                dx = -1
            elif event.key == pg.K_RIGHT:
                dx = +1
            elif event.key == pg.K_DOWN:
                an_limit = 100
            elif event.key == pg.K_UP:
                rotate = True

    [pg.draw.rect(game_sc, (60, 60 , 60), i_rect, 1) for i_rect in grid]

    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not borders():
            figure = deepcopy(figure_old)
            break

    an_count += an_speed

    if an_count > an_limit:
        an_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = pg.Color('white')
                figure = deepcopy(choice(figures))
                an_limit = 1000
                break


    center = figure[0]

    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not borders():
                figure = deepcopy(figure_old)
                break

    line = H - 1
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count +=1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1

    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pg.draw.rect(game_sc, pg.Color('white'), figure_rect)

    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pg.draw.rect(game_sc, col, figure_rect)

    pg.display.flip()
    clock.tick(FPS)




