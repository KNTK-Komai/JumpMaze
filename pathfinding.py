from collections import deque

class Pathfinding:
    def __init__(self,game):
        self.game = game
        self.map = game.map.mini_map
        self.ways = [-1,0],[0,-1],[1,0],[0,1],[-1,-1],[-1,1],[1,-1],[1,1]
        self.graph = {}
        self.get_graph()

    def get_path(self,start,end):
        self.visited = self.bfs(start,end,self.graph)
        path = [end]
        step = self.visited.get(end,start)

        while step != start and step:
            path.append(step)
            step = self.visited[step]
        return path[-1]

    def bfs(self,start,goal,graph):
        queue = deque([start])
        visited = {start:None}

        while queue:
            current = queue.popleft()
            if current == goal:
                break
            next_nodes = graph[current]

            for next_node in next_nodes :
                if next_node not in visited and next_node not in self.game.object_handler.npc_positions:
                    queue.append(next_node)
                    visited[next_node] = current
        return visited

    def get_next_node(self,x,y):
        return [(x+dx,y+dy) for (dx,dy) in self.ways if (x+dx,y+dy) not in self.game.map.world_map]

    def get_graph(self):
        for y,row in enumerate(self.map):
            for x,cell in enumerate(row):
                if not cell:
                    self.graph[(x,y)] = self.graph.get((x,y),[])+self.get_next_node(x,y)