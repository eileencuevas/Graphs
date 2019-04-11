from room import Room
from stack import Stack
from queue import Queue
import random
import math


class World:
    def __init__(self):
        self.startingRoom = None
        self.rooms = {}
        self.roomGrid = []
        self.gridSize = 0

    def loadGraph(self, roomGraph):
        numRooms = len(roomGraph)
        rooms = [None] * numRooms
        gridSize = 1
        for i in range(0, numRooms):
            x = roomGraph[i][0][0]
            gridSize = max(gridSize, roomGraph[i][0][0], roomGraph[i][0][1])
            self.rooms[i] = Room(
                f"Room {i}", f"({roomGraph[i][0][0]},{roomGraph[i][0][1]})", i, roomGraph[i][0][0], roomGraph[i][0][1])
        self.roomGrid = []
        gridSize += 1
        self.gridSize = gridSize
        for i in range(0, gridSize):
            self.roomGrid.append([None] * gridSize)
        for roomID in roomGraph:
            room = self.rooms[roomID]
            self.roomGrid[room.x][room.y] = room
            if 'n' in roomGraph[roomID][1]:
                self.rooms[roomID].connectRooms(
                    'n', self.rooms[roomGraph[roomID][1]['n']])
            if 's' in roomGraph[roomID][1]:
                self.rooms[roomID].connectRooms(
                    's', self.rooms[roomGraph[roomID][1]['s']])
            if 'e' in roomGraph[roomID][1]:
                self.rooms[roomID].connectRooms(
                    'e', self.rooms[roomGraph[roomID][1]['e']])
            if 'w' in roomGraph[roomID][1]:
                self.rooms[roomID].connectRooms(
                    'w', self.rooms[roomGraph[roomID][1]['w']])
        self.startingRoom = self.rooms[0]

    def printRooms(self):
        rotatedRoomGrid = []
        for i in range(0, len(self.roomGrid)):
            rotatedRoomGrid.append([None] * len(self.roomGrid))
        for i in range(len(self.roomGrid)):
            for j in range(len(self.roomGrid[0])):
                rotatedRoomGrid[len(self.roomGrid[0]) -
                                j - 1][i] = self.roomGrid[i][j]
        print("#####")
        str = ""
        for row in rotatedRoomGrid:
            allNull = True
            for room in row:
                if room is not None:
                    allNull = False
                    break
            if allNull:
                continue
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
        print(str)
        print("#####")

    def opposite_direction(self, direction):
        if direction == 'n':
            return 's'
        if direction == 's':
            return 'n'
        if direction == 'e':
            return 'w'
        if direction == 'w':
            return 'e'

    def bfs(self, starting_room, traversal_path, dfs_visited):
        search_queue = Queue()
        search_queue.enqueue([starting_room])
        already_searched = set()
        while search_queue.size() > 0:
            current_path = search_queue.dequeue()
            current_room = current_path[-1]
            # check and see if we've already hit this room, and if not
            if current_room not in already_searched:
                # check in dfs_visited to see if this room got them ?. if yes, we gotta make a
                # path to append somehow and return the new current_room for dfs
                if '?' in dfs_visited[current_room]:
                    # MAKE THE PATH SOMEHOW AND APPEND IT TO TRAVERSAL_PATH

                    return current_room
            # add the room to the already_searched
            already_searched.add(current_room)
            # check the neighboring rooms for the same shit
            for neighbor in dfs_visited[current_room]:
                new_path = list(current_path)
                new_path.append(neighbor)
                search_queue.enqueue(new_path)
            # if nothing, just return.... Frederick I guess idk
        return None

    def dfs(self, starting_room, traversal_path=['n', 's']):
        search_stack = Stack()
        search_stack.push(starting_room)
        visited = {}
        last_room = None

        while search_stack.size() > 0:
            current_room = search_stack.pop()
            if current_room not in visited:
                # get all connecting rooms via room.getExits, which returns a list of exits
                current_room_exits = current_room.getExits()
                # loop through list and call room.getRoomInDirection
                # add all of this to dictionary in form of { direction: room }
                current_exits_dict = {
                    exit_direction: '?' for exit_direction in current_room_exits}
                if last_room is not None:
                    for exit_direction in current_exits_dict:
                        if current_room.getRoomInDirection(exit_direction) == visited[last_room]:
                            visited[last_room][self.opposite_direction(
                                exit_direction)] = current_room
                            current_exits_dict[exit_direction] = visited[last_room]

                # set dict as value for key of current_room
                visited[current_room] = current_exits_dict
                # start moving to neighbors, I guess
                possible_path = visited[current_room]
                last_room = current_room
                if '?' not in possible_path.values():
                    current_room = self.bfs(
                        current_room, traversal_path, visited)
                    if current_room is None:
                        search_stack = Stack()
                for exit_direction in possible_path:
                    if possible_path[exit_direction] == '?':
                        traversal_path.append(exit_direction)
                        search_stack.push(
                            current_room.getRoomInDirection(exit_direction))
        return visited
