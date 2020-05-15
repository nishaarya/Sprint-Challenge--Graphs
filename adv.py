from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

# STEPS
# First pass solution: 
# Record the room in visited
# Get all the exits with the room.
# Move in one direction, add this to the traversal path and pop it off the directions associated with the room
# Work out the opposite direction and add this to a reverse path so that backtracking is possible and remove the opposite direction from the unexplored paths
# Get exits for the new room and keep note of this (in visited)
# Move in a random direction again and add to the traversal path and pop it off the possible directions
# Keep moving until you reach a dead end
# When there are no more unexplored exits - backtrack along the last direction on the backtracked path and remove it from the backtracked path and add it to the traversal path
# Check that room for unexplored directions and repeat the process again
# This keeps going until the number of rooms visited reaches the length of the rooms graph



# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
moving_player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Traversal

def traversal(visited=None, previous=None, came_from=None):
    # Then we set the current room with the player inside and ID
    current_room = player.current_room.id
    # Then we show all avaiable exits
    exits = player.current_room.get_exits()
    # Then all possible reverse
    reverse = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

    # Check if visited or not
    if visited is None:
        # create dictionary
        visited = {}
    
    # if its not visisted, we check
    if current_room not in visited:
        visited[current_room] = {}
    
    # Check the previous node if were not on the first node
    if previous:
        # how did we get to the current room from the previous?
        visited[previous][came_from] = current_room
        # how would we have to get back to the previous 
        visited[current_room][reverse[came_from]] = previous
    
    # now we check on the direction on the exits
    for direction in exits:
        # if its not in visisted
        if direction not in visited[current_room]:
            # we then append (add) onto the existing list
            traversal_path.append(direction)
            # we get the direction the player was travelling
            player.travel(direction)
            # for each possible direction in every node, we repeat this for loop
            traversal(visited, previous=current_room, came_from=direction)
        
    # however, if the direction is in visisted and we have not yet touched all the nodes
    if len(visited) < len(room_graph):
        # we then retrace the steps to find out where we came from
        retrace = reverse[came_from]
        # we retrace the players travel
        player.travel(retrace)
        # we then append (add) what we retrace onto the existing list
        traversal_path.append(retrace)

traversal()

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
#    cmds = input("-> ").lower().split(" ")
#    if cmds[0] in ["n", "s", "e", "w"]:
#        player.travel(cmds[0], True)
#    elif cmds[0] == "q":
#        break
#    else:
#        print("I did not understand that command.")
