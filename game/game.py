import pygame as pg
import random as rnd
import time
from dataclasses import dataclass

pg.init()
width, columns, rows = 400, 15, 30
distance = width // columns
height = distance * rows
gird = [0] * columns * rows
speed, score, level, temp = 1000, 0, 1, 0
picture = []
for n in range(8):
    picture.append(pg.transform.scale(pg.image.load(f'T_{n}.png'),(distance, distance)))

screen = pg.display.set_mode([width, height])
pg.display.set_caption('Mira game')
pg.key.set_repeat(1, 100)

tetroromino_down = pg.USEREVENT + 1
#speedup = pg.USEREVENT + 2
pg.time.set_timer(tetroromino_down, speed)
#pg.time.set_timer(speedup, 30000)

tetrorominos = [[0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], #O
                [0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0], #I
                [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0], #J
                [0, 0, 4, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0], #L
                [0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #S
                [6, 6, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0], #Z
                [0, 0, 0, 0, 7, 7, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0]] #T

@dataclass
class tetroromino():
    tetro: list
    row: int = 0
    column: int = 5
    def show(self):
        for n, color in enumerate(self.tetro):
            if color > 0:
                x = (self.column + n%4) * distance
                y = (self.row + n//4) * distance
                screen.blit(picture[color], (x, y))
    def check(self, r ,c):
        for n, color in enumerate(self.tetro):
            if color > 0:
                rs = r + n//4
                cs = c + n%4
                if cs < 0 or rs >= rows or cs >= columns or gird[rs * columns + cs] > 0:
                    return False
        return True
    def update(self, r, c):
        if self.check(self.row + r, self.column + c):
            self.row += r
            self.column += c
            return True
        return False
    def rotate(self):
        savetetro = self.tetro.copy()
        for n, color in enumerate(savetetro):
            self.tetro[(2-(n%4))*4 + (n//4)] = color
        if not self.check(self.row, self.column):
            self.tetro = savetetro.copy()
def ObjectOnGridLine():
    for n, color in enumerate(character.tetro):
        if color > 0:
            gird[(character.row + n//4) * columns + (character.column + n%4)] = color
def DeleteAllRow():
    fullrow = 0
    for row in range(rows):
        for column in range(columns):
            if gird[row * columns + column] == 0:
                break
            else:
                del gird[row * columns : row * columns + column]
                gird[0:0] = [0] * columns
                fullrow += 1
    return fullrow**2*100

character = tetroromino(rnd.choice(tetrorominos))
status = True
while status:
    pg.time.delay(100)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            status = False
        if event.type == tetroromino_down:
            if not character.update(1, 0):
                ObjectOnGridLine()
                score += DeleteAllRow()
                if score > 0 and score // 500 >= level and temp != score:
                    speed = int(speed * 0.7)
                    pg.time.set_timer(tetroromino_down, speed)
                    level = score // 500 + 1
                    temp = score
                character = tetroromino(rnd.choice(tetrorominos))
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                character.update(0, -1)
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                character.update(0, 1)
            if event.key == pg.K_DOWN or event.key == pg.K_s:
                character.update(1, 0)
            if event.key == pg.K_SPACE:
                character.rotate()
    
    screen.fill((128, 128, 128))
    character.show()
    textsurface = pg.font.SysFont('consolas', 40).render(f'{score:,}', False, (255, 255, 255))
    screen.blit(textsurface, (width//2 - textsurface.get_width()//2, 5))
    textsurface = pg.font.SysFont('consolas', 20).render(f'Level: {level}', False, (255, 255, 255))
    screen.blit(textsurface, (width//2 - textsurface.get_width()//2, 55))

    for n, color in enumerate(gird):
        if color > 0:
            x = n % columns * distance
            y = n // columns * distance
            screen.blit(picture[color],(x, y))
    pg.display.flip()
pg.quit()
