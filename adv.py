from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

# Depth First Traversal
def dft(starting_room):
    # Create an empty stack and add the starting_room to the stack
    s = []
    s.append(starting_room)

    # My own traversal graph; update when a room is newly visited
    visited = {}

    # get the current room ID
    room_id = player.current_room.id

    # get the directions a player can move in the current room they're in
    cur_room_exits = player.current_room.get_exits()

    direction = {}
    # get every cardinal direction a player can move from current room
    for cur_room_exit in cur_room_exits:
        direction.update({cur_room_exit: '?'})
        visited.update({room_id: direction})
        

    print('VISITED:', visited)

    # While the stack is not empty
    while len(s) > 0:
        # Pop last item from stack
        cur_room = s.pop()

        # If that room hasn't been visited...
        if cur_room not in visited:
            print('in room:', cur_room)
            # Mark it as visited
            visited.add(cur_room)

            # get the exits of the current room
            cur_room_exits = player.current_room.get_exits()
            print(cur_room_exits)

            # for every way the player can move
            for cur_room_exit in cur_room_exits:
                # get the room in that direction
                connected_room = player.current_room.get_room_in_direction(cur_room_exit)
                # add the connected room to the stack
                print('appending:', connected_room)
                s.append(connected_room)
            # # add the direction taken to traversal_path
            # traversal_path.append(cur_room_exit)
            # move player
            player.travel(cur_room_exits[-1])
            print('travel:', cur_room_exits[-1])
        # If dead end, travel back
        else:
            # add those instructions to traversal_path
            pass


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

# !call this depth traversal fxn to populate traversal_path
dft(world.starting_room)
print('traversal_path', traversal_path)

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


'''
- do I need to keep track of visited?
    - yes, but I can't ignore them entirely as a person has to travel back a room to check for their neighbors when it is a dead end.
- How does the n, w, e, w inputs play into the traversal?
- How do I keep track of the path and convert those to instructions?
- I need to keep track of the path to travel back up?
- where am i actually moving the player?
- How do I move back when I reach a dead end?
- How do I know I reached a dead end?
- I'm only appending rooms to the stack, but to travel I need to also save the direction
    - https://youtu.be/V6Nv14Nf3qI?t=4348
'''