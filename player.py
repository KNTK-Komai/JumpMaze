from setting import *
import pygame as pg
import math


class Player:
    def __init__(self,game):
        self.game = game
        self.x,self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx,dy = 0,0
        #プレイヤーはハードウェアのFPSを考慮し、オーバークロックを阻止する。
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed*sin_a
        speed_cos = speed*cos_a

        # WASD用の移動処理
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx,dy)

        #矢印用の角度処理
        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        #0 <= angle <= 2pi用
        self.angle %= math.tau

    def check_wall(self,x,y):
        return (x,y) not in self.game.map.world_map

    def check_wall_collision(self,dx,dy):
        #壁に沿って移動できるように個別に処理
        if self.check_wall(int(self.x+dx),int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x),int(self.y+dy)):
            self.y += dy

    def draw(self):
        pg.draw.line(self.game.screen,"yellow",(self.x*50,self.y*50),
                     (self.x*50 + WIDTH * math.cos(self.angle),
                            self.y*50 + WIDTH * math.sin(self.angle)),2)
        pg.draw.circle(self.game.screen,"green",(self.x*50,self.y*50),15)

    def update(self):
        self.movement()

    @property
    def pos(self):
        return self.x,self.y

    #ミニマップ上の座標
    @property
    def map_pos(self):
        return int(self.x),int(self.y)