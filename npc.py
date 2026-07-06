from random import randint,random,choice
import math
import pygame as pg
from setting import *

class NPC:
    def __init__(self,game,pos=(11.5,5.5)):
        self.game = game
        self.player = game.player
        self.x,self.y = pos
        self.speed = randint(10,25)/ 1000
        self.dist = 0
        self.attack_dist = randint(1,3)
        self.accuracy = 0.3
        self.attack_damage = randint(1,3)

        self.player_search_trigger = False
        self.ray_cast_value = False

    def update(self):
        self.draw_ray_cast()
        self.run_logic()

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos,self.player.map_pos)
        next_x,next_y = next_pos
        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y+0.5 - self.y,next_x+0.5 - self.x)
            dx = math.cos(angle)*self.speed
            dy = math.sin(angle)*self.speed
            self.check_wall_collision(dx,dy)

    def attack(self):
        if random() < self.accuracy and pg.time.get_ticks() % 20 == 0:
            self.player_search_trigger = False
            self.game.player.get_damage(self.attack_damage)

    def check_wall(self,x,y):
        return (x,y) not in self.game.map.world_map

    def check_wall_collision(self,dx,dy):
        #壁に沿って移動できるように個別に処理
        if self.check_wall(int(self.x+dx),int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x),int(self.y+dy)):
            self.y += dy

    @property
    def map_pos(self):
        return int(self.x),int(self.y)

    def run_logic(self):
        self.ray_cast_value = self.ray_cast_player_npc()
        if self.ray_cast_value:
            self.player_search_trigger = True

            if self.dist < self.attack_dist:
                self.attack()
            else:
                self.movement()
        elif self.player_search_trigger:
            self.movement()

    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True
        wall_dist_v , wall_dist_h = 0,0
        player_dist_v,player_dist_h = 0,0

        ox,oy = self.player.pos
        x_map,y_map = self.game.player.map_pos

        self.dist = math.hypot(self.x - ox,self.y - oy)
        ray_angle = math.atan2(self.y - oy,self.x - ox) + 1e-8

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # 行検知
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)  # ゼロ除算対策

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a  # 直角三角形による斜辺の導出
        dx = delta_depth * cos_a  # 直角三角形による高さ(底辺はdx固定)

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth
        #列検知
        x_vert,dx = (x_map + 1 , 1) if cos_a > 0 else (x_map - 1e-6 , -1) #ゼロ除算対策

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a # 直角三角形による斜辺の導出
        dy = delta_depth * sin_a # 直角三角形による高さ(底辺はdx固定)

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v,player_dist_h)
        wall_dist = max(wall_dist_v,wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def draw_ray_cast(self):
        pg.draw.circle(self.game.screen,"red",(50*self.x,50*self.y),15)
        if self.ray_cast_player_npc():
            pg.draw.line(self.game.screen,"orange",(50*self.player.x,50*self.player.y),
                         (50*self.x,50*self.y),2)
