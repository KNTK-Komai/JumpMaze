import math

# ゲーム設定
RES = WIDTH, HEIGHT = 1400, 800
FPS = 0

PLAYER_POS = 1.5,5 #プレイヤーのミニマップの座標
PLAYER_ANGLE = 0 # プレイヤーの角度
PLAYER_SPEED = 0.004 # プレイヤーの速度
PLAYER_ROT_SPEED = 0.005 # 回転速度
PLAYER_MAX_HEALTH = 100 # プレイヤーの最大体力

FOV = math.pi / 3 # 視野
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2 #光の精度
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20 #分解能