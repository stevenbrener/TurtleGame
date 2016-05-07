import random
import turtle
from generate_map import Map
from enemy_bot import Enemy

class Game:
    
    def __init__(self, map):
        self.map = map
        self.player_turtle = turtle.Turtle()
        self.player_turtle.shape("turtle")
        self.player_turtle.color("blue")
        self.player_turtle.penup()
        start = map.vertices[random.randint(0, len(map.vertices) - 1)]
        self.player_turtle.goto(start[0], start[1])
        
        self.treasure = map.vertices[random.randint(0, len(map.vertices) - 1)]
        while map.same_cell(self.treasure, self.player_turtle.pos()):
            self.treasure = map.vertices[random.randint(0, len(map.vertices) - 1)]
        tile_turtle = turtle.Turtle()
        tile_turtle.fillcolor("yellow")
        self.map.draw_tile(tile_turtle, self.treasure, self.map.tile_size)
        
        self.exit = map.vertices[random.randint(0, len(map.vertices) - 1)]
        while map.same_cell(self.exit, self.player_turtle.pos()) or map.same_cell(self.exit, self.treasure):
            self.exit = map.vertices[random.randint(0, len(map.vertices) - 1)]
        tile_turtle.fillcolor("red")
        self.map.draw_tile(tile_turtle, self.exit, self.map.tile_size)    
        tile_turtle.ht()
        
        self.enemies = []
        while len(self.enemies) < 5:
            enemy_start = map.vertices[random.randint(0, len(map.vertices) - 1)]
            if not (map.same_cell(enemy_start, self.player_turtle.pos()) or  \
                    map.same_cell(enemy_start, self.treasure) or \
                    map.same_cell(enemy_start, self.exit)):
                intelligence = 1
                if random.randint(1, 4) == 1:
                    intelligence = 2
                enemy = Enemy(self.map, intelligence, enemy_start)
                self.enemies.append(enemy)
        
        self.stolen = False
        self.escaped = False
        
        return None
        
    def player_can_move_to(self, vertex):
    
        tile_size = self.map.tile_size
        curr = self.player_turtle.pos()
        adjacent = [(curr[0] + tile_size, curr[1]),
                    (curr[0], curr[1] - tile_size),
                    (curr[0], curr[1] + tile_size),
                    (curr[0] - tile_size, curr[1])]
                    
        if vertex not in adjacent or vertex not in self.map.vertices:
            return False
            
        return True

    def player_move_to(self, vertex):
        if self.player_can_move_to(vertex):
            self.player_turtle.setheading((self.player_turtle.towards(vertex[0], vertex[1])))
            self.player_turtle.goto(vertex[0], vertex[1])
            
        return None             
                
    def game_over(self):
    
        if self.escaped:
            print("YOU ESCAPED WITH THE TREASURE!")
            return True
    
        for enemy in self.enemies:
            if enemy.position == self.player_turtle.pos() or \
                enemy.position in self.map.get_adjacent(self.player_turtle.pos()):
                print("YOU WERE CAPTURED!")
                return True
                
        return False
        
    def play_round(self, player_move):
        tile_size = self.map.tile_size
        x = self.player_turtle.xcor()
        y = self.player_turtle.ycor()
        
        if player_move == "w":
            y += tile_size
        elif player_move == "a":
            x -= tile_size
        elif player_move == "s":
            y -= tile_size
        elif player_move == "d":
            x += tile_size
        else:
            print("Invalid input. Move with w, a, s, and d")
            return
        
        if self.player_can_move_to((x,y)):
            self.player_move_to((x,y))
            if (x,y) == self.treasure:
                self.stolen = True
                tile_turtle = turtle.Turtle()
                tile_turtle.fillcolor("green")
                self.map.draw_tile(tile_turtle, self.treasure, self.map.tile_size)
                tile_turtle.ht()
                
            if (x,y) == self.exit and self.stolen:
                self.escaped = True
                
        else:
            print("You can't move there")
            return None
            
        objective = self.treasure    
        if self.stolen:        
            objective = self.exit
            
        for enemy in self.enemies:
            player_pos = (self.player_turtle.xcor(), self.player_turtle.ycor())
            if player_pos in enemy.line_of_sight():
                enemy.found_player = True
            enemy.move(objective, player_pos)
            
        return None    
            

#==========================================================
def main():

    width = 500
    height = 500
    tile_size = 20
    tiles = 150
 
    game_map = Map(width, height, tile_size, tiles, 1)
    game_map.draw_map()
    the_game = Game(game_map)
    
    quit = False
    while not the_game.game_over() and not quit:
        commands = input(">")
        commands = commands.lower()
        for command in commands:
            if command == "q":
                quit = True
            else:    
                the_game.play_round(command)
        
 
    input('Press enter to end.')  # keeps the turtle graphics window open

if __name__ == '__main__':
    main()
