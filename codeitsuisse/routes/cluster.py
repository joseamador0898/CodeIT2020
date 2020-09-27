import logging
import json
from collections import deque 

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
from collections import deque 



@app.route('/cluster', methods=['POST'])
def evaluateCluster():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    #logging.info({"answers": results})
    #return jsonify({"answers": results})
    newSolution = clusterSolution()
    result = newSolution.numClusters(data)
    return jsonify({"answer": result})

class clusterSolution:
    def dfs(self, grid, i, j):
        if i<0 or j<0 or i>=len(grid) or j>=len(grid[0]) or grid[i][j] == '*'):
            return
        grid[i][j] = '#'
        self.dfs(grid, i, j+1)
        self.dfs(grid, i+1, j+1)
        self.dfs(grid, i+1, j)
        self.dfs(grid, i+1, j-1)
        self.dfs(grid, i, j-1)
        self.dfs(grid, i-1, j-1)
        self.dfs(grid, i-1, j)
        self.dfs(grid, i-1, j+1)

    def numClusters(self, grid):
        if not grid:
            return 0
            
        count = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == '1':
                    self.dfs(grid, i, j)
                    count += 1
        return count


    

    



