import logging
import json
from collections import deque 

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
from collections import deque 

  
# To store matrix cell cordinates 
class Point: 
    def __init__(self,x: int, y: int): 
        self.x = x 
        self.y = y 
  
# A data structure for queue used in BFS 
class queueNode: 
    def __init__(self,pt: Point, dist: int): 
        self.pt = pt  # The cordinates of the cell 
        self.dist = dist  # Cell's distance from the source 
  
# Check whether given cell(row,col) 
# is a valid cell or not 
def isValid(row: int, col: int, ROW, COL): 
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL) 
  
# These arrays are used to get row and column  
# numbers of 4 neighbours of a given cell  
rowNum = [-1, 0, 0, 1] 
colNum = [0, -1, 1, 0] 
  
# Function to find the shortest path between  
# a given source cell to a destination cell.  
def BFS(mat, src: Point, dest: Point, ROW, COL): 
      
    # check source and destination cell  
    # of the matrix have value 1  
    if mat[src.x][src.y]!=0 or mat[dest.x][dest.y]!=0: 
        return -1
      
    visited = [[False for i in range(COL)] for j in range(ROW)] 
      
    # Mark the source cell as visited  
    visited[src.x][src.y] = True
      
    # Create a queue for BFS  
    q = deque() 
      
    # Distance of source cell is 0 
    s = queueNode(src,0) 
    q.append(s) #  Enqueue source cell 
      
    # Do a BFS starting from source cell  
    while q: 
  
        curr = q.popleft() # Dequeue the front cell 
          
        # If we have reached the destination cell,  
        # we are done  
        pt = curr.pt 
        if pt.x == dest.x and pt.y == dest.y: 
            return curr.dist 
          
        # Otherwise enqueue its adjacent cells  
        for i in range(4): 
            row = pt.x + rowNum[i] 
            col = pt.y + colNum[i] 
              
            # if adjacent cell is valid, has path   
            # and not visited yet, enqueue it. 
            if (isValid(row,col,ROW,COL) and mat[row][col] == 0 and not visited[row][col]): 
                visited[row][col] = True
                Adjcell = queueNode(Point(row,col),curr.dist+1) 
                q.append(Adjcell) 
      
    # Return -1 if destination cannot be reached  
    return -1

@app.route('/supermarket', methods=['POST'])
def evaluateSupermarket():
    data = request.get_json()
    tests = data["tests"]
    results = {}

    
    for t in tests:
        mat = tests[t]["maze"]
        ROW = len(mat)
        COL = len(mat[0])
        source = Point(tests[t]["start"][1],tests[t]["start"][0]) 
        dest = Point(tests[t]["end"][1],tests[t]["end"][0])
      
        dist = BFS(mat,source,dest, ROW, COL) 
      
        if dist!=-1: 
            results[str(t)] = dist
            print("Shortest Path is",dist)

        else: 
            results[str(t)] = -1
            print("Shortest Path doesn't exist") 
    
    logging.info("data sent for evaluation {}".format(data))
    logging.info({"answers": results})
    return jsonify({"answers": results})


