import turtle
import random
from generate_map import Map

class Enemy:
    
    def __init__(self, map, intelligence, start):
        self.map = map
        self.intelligence = intelligence
        self.position = start
        self.avatar = turtle.Turtle()
        self.avatar.shape("turtle")
        if intelligence == 1:
            self.avatar.color("yellow")
        else:
            self.avatar.color("red")
        self.avatar.penup()
        self.avatar.goto(start[0], start[1])
        
        self.found_player = False
        
        return None
        
    def can_move_to(self, vertex):
    
        tile_size = self.map.tile_size
        curr = self.position
        adjacent = [(curr[0] + tile_size, curr[1]),
                    (curr[0], curr[1] - tile_size),
                    (curr[0], curr[1] + tile_size),
                    (curr[0] - tile_size, curr[1])]
                    
        if vertex not in adjacent or vertex not in self.map.vertices:
            return False
            
        return True

    def move_to(self, vertex):
        if self.can_move_to(vertex):
            self.avatar.setheading((self.avatar.towards(vertex[0], vertex[1])))
            self.avatar.goto(vertex[0], vertex[1])
            self.position = vertex
            
        return None
        
    def direct_path(self, start, end):
        cells = self.map.cells
        tile_size = self.map.tile_size
        path = []
    
        horizontal_dir = 1
        vertical_dir = 1
        if start[0] - end[0] > 0:
            horizontal_dir = -1
        if start[1] - end[1] > 0:
            vertical_dir = -1
            
        i = start[0]
        while i != end[0]:
            path.append((i, start[1]))
            i += horizontal_dir * tile_size
            
        i = start[1]
        while i != end[1]:
            path.append((end[0], i))
            i += vertical_dir * tile_size    
        
        return path
        
    def shortest_path_grid(self, target):
        paths = {}
        infinity = self.map.width * self.map.height
        not_found = []
        
        for vertex in self.map.vertices:
            paths[vertex] = [infinity, (0,0)]
            not_found.append(vertex)
            
        start = self.position 
        paths[start] = [0, start]
        
        while len(not_found) > 0:
            #print(len(not_found))
            curr = not_found[0]
            for vertex in not_found:
                if paths[vertex][0] < paths[curr][0]:
                    curr = vertex
            
            not_found.remove(curr)
            
            if target == curr:
                #smallest path to target cell found, so make path.
                path = []
                next = curr
                
                while next != start:
                    #print(next)
                    path.insert(0, next)
                    next = paths[next][1]
                    
                return path
        
            for adjacent in self.map.get_adjacent(curr):
                dist = paths[curr][0] + self.map.distance(curr, adjacent)
                if adjacent in self.map.vertices and dist < paths[adjacent][0]:
                    paths[adjacent][0] = dist
                    paths[adjacent][1] = curr
        
        return []
        
    def shortest_path(self, target):
        cells = self.map.cells
        tile_size = self.map.tile_size
        path = []
        
        horizontal_dir = 1
        vertical_dir = 1
        if self.position[0] - target[0] > 0:
            horizontal_dir = -1
        if self.position[1] - target[1] > 0:
            vertical_dir = -1
        
        if self.map.same_cell(self.position, target):
            i = self.position[0]
            while i != target[0]:
                path.append((i, self.position[1]))
                i += horizontal_dir * tile_size
                
            i = self.position[1]
            while i != target[1]:
                path.append((target[0], i))
                i += vertical_dir * tile_size
        else:
            paths = {}
            infinity = self.map.width * self.map.height
            not_found = []
            
            for cell in self.map.cells:
                paths[cell] = [infinity, (0,0)]
                not_found.append(cell)
                
            start = self.map.get_cell(self.position) 
            paths[start] = [0, start]
            
            while len(not_found) > 0:
                print(len(not_found))
                curr = not_found[0]
                for cell in not_found:
                    if paths[cell][0] < paths[curr][0]:
                        curr = cell
                
                not_found.remove(curr)
                
                if target in cells[curr]:
                    #smallest path to target cell found, so make path.
                    cell_path = []
                    next = curr
                    print(next)
                    print(start)
                    while next != start:
                        print(next)
                        cell_path.insert(0, next)
                        next = paths[next][1]
                        
                    #path is just cells at this point, not individual tiles.
                    overlap = self.map.find_overlap(self.map.cells[start], cell_path[0])
                    if self.map.same_cell(start, overlap):
                        path = self.direct_path(start, overlap)
                    for i in range(len(cell_path) - 1):
                        overlap = self.map.find_overlap(self.map.cells[cell_path[i]], cell_path[i + 1])
                        if self.map.same_cell(cell_path[i], overlap):
                            path += self.direct_path(cell_path[i], overlap)
                    return path
            
                for adjacent in self.map.adjacency_graph[curr]:
                    dist = paths[curr][0] + self.map.distance(curr, adjacent)
                    if dist < paths[adjacent][0]:
                        paths[adjacent][0] = dist
                        paths[adjacent][1] = curr
        
        return path
        
    def move(self, objective, player):
        path = []
        next_move = (0,0)
        if self.found_player:
            path = self.shortest_path_grid(player)
            next_move = path[0]
        elif self.intelligence == 2 and not self.position in self.map.cells[self.map.get_cell(objective)]:
            path = self.shortest_path_grid(objective)
            next_move = path[0]
        else:
            adjacent = self.map.get_adjacent(self.position)
            next_move = adjacent[random.randint(0, len(adjacent)-1)]
            while next_move not in self.map.vertices:
                next_move = adjacent[random.randint(0, len(adjacent)-1)]
                
        self.move_to(next_move)

        return None
        
    def line_of_sight(self):
        can_see = []
        for cell in self.map.cells:
            if self.position in self.map.cells[cell]:
                can_see += self.map.cells[cell]
                
        return can_see
        
#==========================================================
def main():
    
    width = 500
    height = 500
    tile_size = 20
    tiles = 150
    
    the_map = Map(width, height, tile_size, tiles, 1)
    the_map.draw_grid()
    the_map.draw_graph("green")
    
    enemy = Enemy(the_map, 2, the_map.vertices[0])
    #target = enemy.position
    #cell = enemy.map.get_cell(target)
    tile_turtle = turtle.Turtle()
    tile_turtle.color("red")
    
    target = enemy.map.vertices[random.randint(0, len(enemy.map.vertices) - 1)]
    the_map.draw_tile(tile_turtle, target, 20)
    tile_turtle.ht()
    #path = enemy.shortest_path(target)
    path = enemy.shortest_path_grid(target)
    #path = enemy.direct_path(enemy.position, target)
    #print(path)
    tile_turtle.color("yellow")
    for tile in path:
        #the_map.draw_tile(tile_turtle, tile, 20)
        enemy.move_to(tile)
    
    
    input('Press enter to end.')  # keeps the turtle graphics window open

if __name__ == '__main__':
    main()
