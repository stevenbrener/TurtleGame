
import turtle
import random
import math
import sys, getopt

class Map:

    def __init__(self, width, height, tile_size, tiles, type):
    
        if width % tile_size != 0:
            width +=  tile_size - width % tile_size 
        if height % tile_size != 0:
            height += tile_size - height % tile_size
            
        columns = width // tile_size
        rows = height // tile_size

        if tiles >= rows * columns:
            tiles = 2 * (tiles // 3)
        
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tile_count = tiles
        
        if type == 2:
            self.vertices = self.generate_bad_random_graph(tiles, width, height, tile_size)
            self.cells = {self.vertices[0] : self.vertices}
        else:
            cells = self.generate_cells(tiles, width, height, tile_size)
            self.connect_cells(cells, tile_size)
            self.cells = cells
            self.vertices = sorted(self.cells_to_vertices(cells))

        self.adjacency_graph = self.make_adjacency_graph()    
        
        return None
        
    def draw_grid(self): # width, height, tile_size):
        ''' Included in init now. Can remove?
        if self.width % self.tile_size != 0:
            width +=  tile_size - width % tile_size 
        if height % tile_size != 0:
            height += tile_size - height % tile_size
        '''
        
        right_edge = self.width // 2
        left_edge = -right_edge
        top_edge = self.height // 2
        bottom_edge = -top_edge
        grid_turtle = turtle.Turtle()
        grid_turtle.speed(0)
        grid_turtle.penup()
        grid_turtle.goto(left_edge, bottom_edge)
        grid_turtle.setheading(0)
        grid_turtle.pendown()
        
        grid_turtle.forward(self.width)
        grid_turtle.left(90)
        grid_turtle.forward(self.height)
        grid_turtle.left(90)
        grid_turtle.forward(self.width)
        grid_turtle.left(90)
        grid_turtle.forward(self.height)
        
        grid_turtle.left(90)
        
        columns = self.width // self.tile_size
        rows = self.height // self.tile_size
        
        for i in range(1, columns):
            grid_turtle.penup()
            grid_turtle.goto(left_edge + i * self.tile_size, bottom_edge)
            grid_turtle.setheading(90)
            grid_turtle.pendown()
            grid_turtle.forward(self.height)
            
        for i in range(1, rows):
            grid_turtle.penup()
            grid_turtle.goto(left_edge, bottom_edge + self.tile_size * i)
            grid_turtle.setheading(0)
            grid_turtle.pendown()
            grid_turtle.forward(self.height)    
        
        grid_turtle.ht()
        return None
        
    def center_to_corner(self, vertex, tile_size):
        x = vertex[0] - tile_size // 2
        y = vertex[1] - tile_size // 2
        return (x, y)
        
    def draw_tile(self, tile_turtle, vertex, tile_size):
        tile_turtle.penup()
        vertex = self.center_to_corner(vertex, tile_size)
        tile_turtle.goto(vertex[0], vertex[1])
        tile_turtle.setheading(0)
        tile_turtle.pendown()
        
        tile_turtle.begin_fill()
        for i in range(4):
            tile_turtle.forward(tile_size)
            tile_turtle.left(90)
        tile_turtle.end_fill()
        
        return None
        
    def draw_graph(self, tile_color):

        graph_turtle = turtle.Turtle()
        graph_turtle.fillcolor(tile_color)
        graph_turtle.speed(0)
        
        for i in range(len(self.vertices)):
            self.draw_tile(graph_turtle, self.vertices[i], self.tile_size)
        
        #Debug code to draw centers
        '''
        graph_turtle.fillcolor("red")
        for cell in self.cells:
            self.draw_tile(graph_turtle, cell, self.tile_size)
        '''
        
        graph_turtle.ht()
        return None
        
    def generate_bad_random_graph(self, size, width, height, tile_size):
        
        if width % tile_size != 0:
            width +=  tile_size - width % tile_size 
        if height % tile_size != 0:
            height += tile_size - height % tile_size
            
        right_edge = width // 2 - tile_size
        left_edge = -right_edge + tile_size
        top_edge = height // 2 - tile_size
        bottom_edge = -top_edge + tile_size
        columns = width // tile_size
        rows = height // tile_size
        
        first_column = random.randint(1, columns - 2)
        first_row = random.randint(1, rows - 2)
        
        tiles = [(first_column, first_row)]
        
        while len(tiles) < size:
            initial = random.randint(0, len(tiles) - 1)
            tile = tiles[initial]
            direction = random.randint(0, 3)
            while tile in tiles:
                if direction == 0:
                    tile = (tile[0] + 1, tile[1])
                if direction == 1:
                    tile = (tile[0] - 1, tile[1])
                if direction == 2:
                    tile = (tile[0], tile[1] + 1)    
                if direction == 3:
                    tile = (tile[0], tile[1] - 1)
                    
            if tile[0] > 0 and tile[1] > 0 and tile[0] < columns and tile[1] < rows:
                tiles.append(tile)
        
        vertices = []
        for i in range(len(tiles)):
            x = tiles[i][0] * tile_size + tile_size // 2 - width // 2
            y = tiles[i][1] * tile_size + tile_size // 2 - height // 2
            vertices.append((x,y))
            
        return vertices
             

    def generate_cells(self, tiles, width, height, tile_size):
        
        columns = width // tile_size
        rows = height // tile_size
        
        max_cell_width = columns // 5
        max_cell_height = rows // 5
        
        cell_tiles = tiles - tiles // 20
        
        cells = {}
        vertices = []
        
        while len(vertices) < cell_tiles:
            
            column = random.randint(max_cell_width // 2, columns - (max_cell_width // 2) - 1)
            row = random.randint(max_cell_height // 2, rows - (max_cell_height // 2) - 1)
            x = column * tile_size + tile_size // 2 - width // 2
            y = row * tile_size + tile_size // 2 - height // 2
            center = (x, y)
            
            if self.distance_to_a_center(center, cells) < 4 * tile_size:
                continue
            
            cells[center] = []
            
            cell_width = random.randint(2, max_cell_width)
            cell_height = random.randint(2, max_cell_height)
            
            i = x - ((cell_width // 2) * tile_size)
            while i < x + ((cell_width // 2) * tile_size):
                j = y - ((cell_height // 2) * tile_size)
                while j < y + ((cell_height // 2) * tile_size):
                    cells[center].append((i,j))
                    if (i,j) not in vertices:
                        vertices.append((i,j))
                    j += tile_size    
                i += tile_size

        return cells
        
    def find_shortest_edge(self, graph):
        shortest_length = 1000000000
        shortest_edge = ((0,0), (0,0))
        for vertex1 in graph:
            for vertex2 in graph[vertex1]:
                edge_dist = self.distance(vertex1, vertex2)
                if edge_dist < shortest_length:
                    shortest_edge = (vertex1, vertex2)
                    shortest_length = edge_dist
                    
        return shortest_edge   

    def path_exists(self, vertex1, vertex2, graph):
        if vertex1 not in graph or vertex2 not in graph:
            return False
            
        marked = []
        not_checked = [vertex1]
        while len(not_checked) > 0:
            next = not_checked.pop()
            if next not in marked:
                marked.append(next)
                for v in graph[next]:
                    if v not in marked and v not in not_checked:
                        not_checked.append(v)
                        
            if vertex2 in marked:
                return True
                
        return False
        
    def make_hallway(self, cell1, cell2, cells, tile_size):
        start = cells[cell1][random.randint(0, len(cells[cell1])-1)]
        end = cells[cell2][random.randint(0, len(cells[cell2])-1)]
        
        horizontal_dir = 1
        vertical_dir = -1
        if start[0] - end[0] > 0:
            horizontal_dir = -1
        if start[1] - end[1] > 0:
            vertical_dir = 1

        hall1 = []
        hall2 = []
        
        i = start[0]
        while i != end[0]:
            if (i, start[1]) not in cell1:
                hall1.append((i,start[1]))
                i += horizontal_dir * tile_size
            
        i = end[1]
        while i != start[1]:
            if (end[0], i) not in cell2:
                hall2.append((end[0], i))
                i += vertical_dir * tile_size

        hall1.append((end[0], start[1]))
        hall2.append((end[0], start[1]))
        
        return [hall1, hall2]
        
    def print_graph(self, graph):
        for vertex in graph:
            print(str(vertex) + ":")
            print(graph[vertex])
            print()
            
        return None
        
    def connected(self, graph):
        if len(graph.keys()) == 0:
            return False
        
        vertices = list(graph.keys())
        start = vertices[0]
        #Should speed up by not using path_exists function
        for vertex in vertices:
            if vertex != start:
                if not self.path_exists(start, vertex, graph):
                    return False

        return True
        
    def connect_cells(self, cells, tile_size):
        '''
        Connects cells using Kruskal's algorithm
        '''
        full_graph = {}
        for cell in cells:
            full_graph[cell] = list(cells.keys())
        
        for vertex in full_graph:
            full_graph[vertex].remove(vertex)
        
        mst_graph = {}
        while (len(mst_graph.keys()) < len(full_graph.keys())) or (not self.connected(mst_graph)):
            edge = self.find_shortest_edge(full_graph)
            if not self.path_exists(edge[0], edge[1], mst_graph):
            
                if edge[0] in mst_graph:
                    mst_graph[edge[0]].append(edge[1])
                else:
                    mst_graph[edge[0]] = [edge[1]]
                if edge[1] in mst_graph:
                    mst_graph[edge[1]].append(edge[0])
                else:
                    mst_graph[edge[1]] = [edge[0]]    
                    
            full_graph[edge[0]].remove(edge[1])
            full_graph[edge[1]].remove(edge[0])
            
        extra_edges = (len(full_graph.keys()) ** 2) // 50
        #print(extra_edges)

        
        for i in range(extra_edges):
            edge = self.find_shortest_edge(full_graph)
            if edge[0] in mst_graph:
                mst_graph[edge[0]].append(edge[1])
            else:
                mst_graph[edge[0]] = [edge[1]]
            if edge[1] in mst_graph:
                mst_graph[edge[1]].append(edge[0])
            else:
                mst_graph[edge[1]] = [edge[0]]    
                    
            full_graph[edge[0]].remove(edge[1])
            full_graph[edge[1]].remove(edge[0])
        
        hallways = []
        marked = []
        for start_cell in mst_graph:
            for end_cell in mst_graph[start_cell]:
                if (start_cell, end_cell) not in marked and (end_cell, start_cell) not in marked:
                    marked.append((start_cell, end_cell))
                    if not self.is_adjacent(cells[start_cell], cells[end_cell]):
                        hallway = self.make_hallway(start_cell, end_cell, cells, tile_size)
                        hallways.append(hallway[0])
                        hallways.append(hallway[1])
                    
        for hallway in hallways:
            center = hallway[len(hallway) // 2]
            if center in cells:
                cells[center] += hallway
            else:
                cells[center] = hallway
                
        return None    
         
            
    def distance(self, vertex1, vertex2):
        a = vertex1[0] - vertex2[0]
        b = vertex1[1] - vertex2[1]
        c = math.sqrt(a ** 2 + b ** 2)
        return c
        
    def distance_to_a_center(self, vertex, cells):
        centers = list(cells.keys())
        min_dist = 10000000000000000
        for center in centers:
            curr_dist = self.distance(vertex, center)
            if curr_dist < min_dist:
                min_dist = curr_dist 
        
        return min_dist

    def cells_to_vertices(self, cells):
        vertices = []
        for cell in cells:
            for vertex in cells[cell]:
                if vertex not in vertices:
                    vertices.append(vertex)
            
        return vertices
        
    def get_adjacent(self, vertex):
        adjacent = [(vertex[0] + self.tile_size, vertex[1]),
                    (vertex[0], vertex[1] - self.tile_size),
                    (vertex[0], vertex[1] + self.tile_size),
                    (vertex[0] - self.tile_size, vertex[1])]
        return adjacent            
        
    def is_adjacent(self, cell1, cell2):
        for curr in cell1:
            adjacent = [(curr[0] + self.tile_size, curr[1]),
                        (curr[0], curr[1] - self.tile_size),
                        (curr[0], curr[1] + self.tile_size),
                        (curr[0] - self.tile_size, curr[1])]
            for vertex in cell2:
                if vertex in adjacent:
                    return True
        
        return False

    def find_adjacent(self, cell1, cell2):
        for curr in cell1:
            adjacent = [(curr[0] + self.tile_size, curr[1]),
                        (curr[0], curr[1] - self.tile_size),
                        (curr[0], curr[1] + self.tile_size),
                        (curr[0] - self.tile_size, curr[1])]
            for vertex in cell2:
                if vertex in adjacent:
                    return (curr, vertex)
        
        return ((1000,1000),(1000,1000))
        
    def make_adjacency_graph(self):
        graph = {}
        
        for cell1 in self.cells:
            graph[cell1] = []
            for cell2 in self.cells:
                if cell1 != cell2 and self.is_adjacent(self.cells[cell1], self.cells[cell2]):
                    graph[cell1].append(cell2)
                    #Side effect of adding a vertex to each cell to make them overlap
                    to_add = self.find_adjacent(self.cells[cell1], self.cells[cell2])
                    self.cells[cell1].append(to_add[1])
                    self.cells[cell2].append(to_add[0])
        
        return graph
        
    def get_cell(self, vertex):
        for cell in self.cells:
            if vertex in self.cells[cell]:
                return cell
        return vertex
        
    def same_cell(self, vertex1, vertex2):
        for cell in self.cells:
            if vertex1 in self.cells[cell] and vertex2 in self.cells[cell]:
                return True
                
        return False
        
    def find_overlap(self, cell1, cell2):
        for vertex in cell1:
            if vertex in cell2:
                return vertex
                
        return (1000,1000)   

    def draw_map(self):
        self.draw_grid()
        self.draw_graph("green")
#==========================================================
def main(argv):

    width = 500
    height = 500
    tile_size = 20
    tiles = 150
    type = 1
    try:
        opts, args = getopt.getopt(argv, "t:")
    except getopt.getoptError:
        print("Specify a type")
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == "-t":
            type = int(arg)

    the_map = Map(width, height, tile_size, tiles, type)
    
    the_map.draw_grid()
    #draw_grid(width, height, tile_size)
    
    #cells = generate_cells(tiles, width, height, tile_size)
    #connect_cells(cells, tile_size)
    #vertices = sorted(cells_to_vertices(cells))
    #vertices = generate_bad_random_graph(tiles, width, height, tile_size)
    
    the_map.draw_graph("green")
    #print(the_map.adjacency_graph)
    #draw_graph(list(cells.keys()), tile_size, "red")
    
    input('Press enter to end.')  # keeps the turtle graphics window open

if __name__ == '__main__':
    main(sys.argv[1:])
