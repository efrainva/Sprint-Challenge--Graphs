from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# 
def next_path(starting_room, all_rooms=set()):
    visited = set()

    for room in all_rooms:  
        visited.add(room) 
        path = [] 
        opposite = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'} # directions 

        def add_to_path(r, back_to=None):
            visited.add(r)
            exits = r.get_exits() 
            for direction in exits:
                # print(direction)
                if r.get_room_in_direction(direction) not in visited: 
                    path.append(direction) 
                    add_to_path(r.get_room_in_direction(direction), opposite[direction]) 

            if back_to: #  is None
                path.append(back_to) 

        add_to_path(starting_room) 
        return path

def create_path(starting_room, visited=set()):
    path = []
    opposite = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'} 

    def add_to_path(room, back_to=None):
        visited.add(room)  
        exits = room.get_exits() 
        path_length = {} 
        traverse_order = [] 
        # print("show traverse order as empty", traverse_order)

        for direction in exits:
            # print(direction)
            path_length[direction] = len(next_path(room.get_room_in_direction(direction), visited))


        for key, value in sorted(path_length.items(), key=lambda val: val[1]): 
            print("this is the len of our path", key, value)
            print(key, value) 
            traverse_order.append(key) 

            print(" my traverse order list", traverse_order)

        for direction in traverse_order: 
            # print(direction)
            if room.get_room_in_direction(direction) not in visited: 
                path.append(direction) 
                add_to_path(room.get_room_in_direction(direction), opposite[direction]) 

        if len(visited) == len(world.rooms): 
            return 
        elif back_to:
            path.append(back_to) 

    add_to_path(starting_room) 
    return path 


traversal_path = create_path(world.starting_room) 

# 


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
