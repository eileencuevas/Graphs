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

    def room_search(self, starting_room, traversal_path=None):
        search_queue = Stack()
        search_queue.push([starting_room])
        visited = {}
        if traversal_path is None:
            traversal_path = []
        else:
            traversal_path.pop()
            traversal_path.pop()
        last_room = None
        while search_queue.size() > 0:
            current_path = search_queue.pop()
            current_room = current_path[-1]
            if current_room not in visited:
                visited[current_room] = current_path
                current_room_exits = current_room.getExits()
                if last_room is not None:
                    dir_traveled = ''
                    for room_exit in current_room_exits:
                        if current_room.getRoomInDirection(room_exit) == last_room:
                            dir_traveled = self.opposite_direction(room_exit)
                    if len(dir_traveled) > 0:
                        traversal_path.append(dir_traveled)
                    else:
                     # find path from last room to this room and append it to traversal path
                        dir_traveled = self.bfs_with_target(
                            last_room, current_room)
                        traversal_path.extend(dir_traveled)
                last_room = current_room
                for room_exit in current_room_exits:
                    next_room = current_room.getRoomInDirection(room_exit)
                    new_path = list(current_path)
                    new_path.append(next_room)
                    search_queue.push(new_path)
        return traversal_path

    def bfs_with_target(self, starting_room, target_room):
        search_queue = Queue()
        search_queue.enqueue([starting_room])
        visited = {}
        while search_queue.size() > 0:
            current_path = search_queue.dequeue()
            current_room = current_path[-1]
            if current_room not in visited:
                if current_room == target_room:
                    # we're getting a list of room objects here.
                    # make cardinal directions list
                    possible_dir = ['n', 's', 'e', 'w']
                    # iterate through current path up to second to last room
                    # for each room, iterate through directions list
                    # if room at direction == room + 1, append dir to list
                    path_with_dirs = [d for i in range(len(
                        current_path)-1) for d in possible_dir if current_path[i].getRoomInDirection(d) == current_path[i+1]]
                    return path_with_dirs
                visited[current_room] = current_path
                current_room_exits = current_room.getExits()
                for room_exit in current_room_exits:
                    next_room = current_room.getRoomInDirection(room_exit)
                    new_path = list(current_path)
                    new_path.append(next_room)
                    search_queue.enqueue(new_path)
