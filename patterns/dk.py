# Navigate a pixel through the cube using Best First pathfinding
# Copyright (C) Liz Lyon <@lizzipfish>
# Released under the terms of the GNU General Public License version 3

import cubehelper
import numpy
import math
import random

RED = 0xff0000
YELLOW = 0xffff00
GREEN = 0x00ff00
BLUE = 0x00ffd8

maxRuns = 5 # Number of times to run pattern before finishing

platforms = [
            #face1
            (0,0,0),(1,0,0),(2,0,0),(3,0,0),(4,0,0),(5,0,0),(6,0,0),
            (7,0,2),(6,0,2),(5,0,2),(4,0,2),(3,0,2),(2,0,2),(1,0,2),
            (0,0,4),(1,0,4),(2,0,4),(3,0,4),(4,0,4),(5,0,4),(6,0,4),
            (7,0,6),(6,0,6),(5,0,6),(4,0,6),(3,0,6),(2,0,6),(1,0,6),
            #face2
            (0,0,0),(0,1,0),(0,2,0),(0,3,0),(0,4,0),(0,5,0),(0,6,0),
            (0,7,2),(0,6,2),(0,5,2),(0,4,2),(0,3,2),(0,2,2),(0,1,2),
            (0,0,4),(0,1,4),(0,2,4),(0,3,4),(0,4,4),(0,5,4),(0,6,4),
            (0,7,6),(0,6,6),(0,5,6),(0,4,6),(0,3,6),(0,2,6),(0,1,6),
            #face3
            (0,7,0),(1,7,0),(2,7,0),(3,7,0),(4,7,0),(5,7,0),
            (7,7,2),(6,7,2),(5,7,2),(4,7,2),(3,7,2),(2,7,2),(1,7,2),
            (0,7,4),(1,7,4),(2,7,4),(3,7,4),(4,7,4),(5,7,4),(6,7,4),
            (7,7,6),(6,7,6),(5,7,6),(4,7,6),(3,7,6),(2,7,6),(1,7,6),
            #face4
            (7,0,0),(7,1,0),(7,2,0),(7,3,0),(7,4,0),(7,5,0),
            (7,7,2),(7,6,2),(7,5,2),(7,4,2),(7,3,2),(7,2,2),(7,1,2),
            (7,0,4),(7,1,4),(7,2,4),(7,3,4),(7,4,4),(7,5,4),(7,6,4),
            (7,7,6),(7,6,6),(7,5,6),(7,4,6),(7,3,6),(7,2,6),(7,1,6),
            #face5
            (2,5,0),(2,4,0),(2,3,0),(2,2,0),
            (4,2,0),(4,3,0),(4,4,0),(4,5,0),(4,6,0),
            (6,5,0),(6,4,0),(6,3,0),(6,2,0),
            ]

def randomizePlatforms():
    destroyCount = 10
    plat = platforms[:]
    random.shuffle(plat)
    del plat[-destroyCount:]
    return plat

def distance(a,b):
    x = b[0] - a[0]
    y = b[1] - a[1]
    z = b[2] - a[2]

    x = x * x
    y = y * y
    z = z * z 

    return math.sqrt(x + y + z)

def createPath(closedNodes):
    path = []
    current = closedNodes[-1]

    while current[4] is not None:
        path.append((current[0], current[1], current[2]))
        current = current[4]

    return path

def existingPos(pos,arr):
    for p in arr: 
        if pos[0] == p[0] and pos[1] == p[1] and pos[2] == p[2]:
            return True 

    return False

def isEdgeOfCube(pos, size):
    if pos[0] == 0 or pos[0] == size or pos[1] == 0 or pos[1] == size or pos[2] == 0 or pos[2] == size:
        return True
        
    return False

def existingPlatform(pos, platforms):
    for p in platforms: 
        if pos[0] == p[0] and pos[1] == p[1] and pos[2] == p[2]:
            return True 
    
    return False

def bestFirst(start, end, size, platforms):
    closedNodes = []
    openNodes = []
    openNodes.append(start)

    while len(openNodes) > 0:
        openNodes.sort(key=lambda node: node[3])
        current = openNodes.pop(0)

        if current[0] == end[0] and current[1] == end[1] and current[2] == end[2]:
            closedNodes.append(current)
            return createPath(closedNodes)

        closedNodes.append(current)

        #Calulate neighbours 
        #x+1
        if current[0]+1 < size:
            pos = [current[0]+1,current[1],current[2]]

            if isEdgeOfCube(pos, size) and not existingPos(pos, openNodes) and not existingPos(pos, closedNodes) and not existingPlatform(pos, platforms):
                neighbour = pos
                neighbour.append(round(distance(neighbour, end),2))
                neighbour.append(closedNodes[-1])
                openNodes.append(neighbour)

        #x-1
        if current[0]-1 > -1:
            pos = [current[0]-1,current[1],current[2]]
            
            if isEdgeOfCube(pos, size) and not existingPos(pos, openNodes) and not existingPos(pos, closedNodes) and not existingPlatform(pos, platforms):
                neighbour = pos
                neighbour.append(round(distance(neighbour, end),2))
                neighbour.append(closedNodes[-1])
                openNodes.append(neighbour)

        #y+1
        if current[1]+1 < size:
            pos = [current[0],current[1]+1,current[2]]

            if isEdgeOfCube(pos, size) and not existingPos(pos, openNodes) and not existingPos(pos, closedNodes) and not existingPlatform(pos, platforms):
                neighbour = pos
                neighbour.append(round(distance(neighbour, end),2))
                neighbour.append(closedNodes[-1])
                openNodes.append(neighbour)

        #y-1
        if current[1]-1 > -1:
            pos = [current[0],current[1]-1,current[2]]
            
            if isEdgeOfCube(pos, size) and not existingPos(pos, openNodes) and not existingPos(pos, closedNodes) and not existingPlatform(pos, platforms):
                neighbour = pos
                neighbour.append(round(distance(neighbour, end),2))
                neighbour.append(closedNodes[-1])
                openNodes.append(neighbour)

        #z+1
        if current[2]+1 < size:
            pos = [current[0],current[1],current[2]+1]
            
            if isEdgeOfCube(pos, size) and not existingPos(pos, openNodes) and not existingPos(pos, closedNodes) and not existingPlatform(pos, platforms):
                neighbour = pos
                neighbour.append(round(distance(neighbour, end),2))
                neighbour.append(closedNodes[-1])
                openNodes.append(neighbour)

        #z-1
        if current[2]-1 > -1:
            pos = [current[0],current[1],current[2]-1]
            
            if isEdgeOfCube(pos, size) and not existingPos(pos, openNodes) and not existingPos(pos, closedNodes) and not existingPlatform(pos, platforms):
                neighbour = pos
                neighbour.append(round(distance(neighbour, end),2))
                neighbour.append(closedNodes[-1])
                openNodes.append(neighbour)

    return False



class Pattern(object):
    def init(self):
        self.runCount = 0
        self.double_buffer = True
        self.restart()
        return 1.0/10

    def restart(self):
        self.start = [7,0,7,None,None] #(x,y,z,dist,parent)
        self.end = [7,7,0,0,None]
        self.start[3] = round(distance(self.start, self.end),2)

        self.platforms = randomizePlatforms()
        self.path = bestFirst(self.start, self.end, self.cube.size, self.platforms)

        if not self.path:
            self.restart()

        self.ball = self.path.pop()


    def tick(self):
        self.cube.clear()

        for p in self.platforms:
            self.cube.set_pixel(p, YELLOW)

        self.cube.set_pixel((self.ball[0],self.ball[1],self.ball[2]), RED)
        self.cube.set_pixel((self.end[0],self.end[1],self.end[2]), BLUE)

        if len(self.path) == 0:
            if self.runCount >= maxRuns:
                raise StopIteration
            self.runCount += 1
            self.restart()

        self.ball = self.path.pop()