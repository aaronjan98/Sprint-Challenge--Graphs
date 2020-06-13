from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()

# My own traversal graph; update when a room is newly visited
visited = {}

#! Breadth First Search to find the path to the shortest unexplored room
def bfs(starting_room):

    # keep track of explored rooms
    explored = []
    # keep track of all the paths to be checked
    queue = [[starting_room]]

    # keeps looping until all possible paths have been checked
    while queue:
        # pop the first path from the queue
        path = queue.pop(0)
        # get the last room from the path
        room = path[-1]

        if room not in explored:
            # Loop through the room exits
            for connected_rm_id in visited[room].values():
                # if one of the exits aren't visited
                if connected_rm_id == '?':
                    return path
                # If an exit has been visited (not '?'), you can put it in the queue
                else:
                    new_path = list(path)
                    new_path.append(connected_rm_id)
                    queue.append(new_path)

            # mark room as explored
            explored.append(room)

#! Depth First Traversal
def traverse_rooms(starting_room):

    # get the current room ID
    room_id = player.current_room.id

    def add_visited():
        directions = {}
        # get every cardinal direction a player can move from current room
        for room_exit in player.current_room.get_exits():
            directions.update({room_exit: '?'})
            visited.update({player.current_room.id: directions})
        
    add_visited()

    # function returns whether a '?' is in the rooms
    def get_ques(val): 
        for directions in visited.values():
            for dir_rm in directions.values():
                if val == dir_rm:
                    return True
        return False
    
    def opp_exit(direction):
        if direction == 'n':
            return 's'
        elif direction == 's':
            return 'n'
        elif direction == 'e':
            return 'w'
        elif direction == 'w':
            return 'e'
        else:
            return None

    #! Loop until there are exactly 500 entries in your graph and no '?' in the adjacency dictionaries.
    while len(visited) < graph_entries or get_ques('?'):
        limit_reached = 0
        num_connected_rms = len(visited[room_id])

        # Loop through the room exits, and travel into the first exit == '?'
        for rm_exit, connected_rm_id in visited[room_id].items():
            # if the exit is unvisited, has a '?'
            if connected_rm_id == '?':
                # have player travel to the room
                player.travel(rm_exit)
                # create a exit hash table for the new room ONLY if it doesn't exist already
                try:
                    visited[player.current_room.id]
                except KeyError:
                    add_visited()

                # update which room the exit connects to, replace '?'
                visited[room_id].update({rm_exit: player.current_room.id})
                # update the connected room's hash table, replace '?'
                visited[player.current_room.id].update({opp_exit(rm_exit): room_id})
                # update traversal_path
                traversal_path.append(rm_exit)
                # update room_id to the new room the player traveled to
                room_id = player.current_room.id
                break
            # exit is not '?'
            else:
                limit_reached += 1

        # if all exits have been visited
        if num_connected_rms == limit_reached:
            # returns a path that the player came from
            path = bfs(player.current_room.id)
            
            for i in path:
                for room_exit in player.current_room.get_exits():
                    if visited[player.current_room.id][room_exit] == i:
                        player.travel(room_exit)
                        # update traversal_path
                        traversal_path.append(room_exit)
                        room_id = player.current_room.id

graph_entries = 500

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

#! call this depth traversal fxn to populate traversal_path
traverse_rooms(world.starting_room)

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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
