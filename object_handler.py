from npc import *

class ObjectHandler:
    def __init__(self,game):
        self.game = game
        self.npc_list = []
        add_npc = self.add_npc
        self.npc_positions = {}

        add_npc(NPC(game))
        add_npc(NPC(game,pos=(2.5,12.5)))
        add_npc(NPC(game,pos=(12.5,10.5)))
        add_npc(NPC(game,pos=(19.5,14.5)))
        add_npc(NPC(game,pos=(18.5,3.5)))

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list}
        [npc.update() for npc in self.npc_list]

    def add_npc(self,npc):
        self.npc_list.append(npc)