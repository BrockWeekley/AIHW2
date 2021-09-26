import json
import time

start = time.time()

# First five expanded nodes, instance one: (2, 2), (3, 2), (1, 2), (2, 3), (2, 1)
# First five expanded nodes, instance two: (3, 2), (4, 2), (2, 2), (3, 3), (3, 1)

# Path found: (2, 2), (1, 2), (2, 2), (2, 3), (2, 4), (3, 4), (3, 5) Cost: 5.5
# Path 2 found: (3, 2), (2, 2), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3), (4, 4), (3, 4), (2, 4) Cost: 7.7

# Action costs defined
action_left = 10
action_right = 9
action_up = 8
action_down = 7
action_suck = 2


# Node object which holds the node location, cost, and cleanliness status
class Node(object):
    location_row = 0
    location_col = 0
    cost = 0
    status = 0

    def __init__(self, location_row, location_col, cost, status):
        self.location_row = location_row
        self.location_col = location_col
        self.cost = cost
        self.status = status


if __name__ == '__main__':
    print('Uniform Cost Tree')
    inputFile = open('instanceTwo.json')
    squares = json.load(inputFile)['squares']
    startingRow = 0
    startingCol = 0
    actionCost = 0

    rowNum = 0
    colNum = 0

    # This loop finds the starting point for the vacuum within the graph and sets it to 0
    for row in squares:

        for col in row:

            if col == 2:
                startingCol = colNum
                startingRow = rowNum
                squares[rowNum][colNum] = 0
            colNum += 1
        rowNum += 1
        colNum = 0

    # Define the size of the room, the initial fringe node, and the initial number of nodes to be expanded
    fringe = [Node(startingRow, startingCol, 0, 0)]

    rowNum = len(squares)
    colNum = len(squares[0])
    currentRow = 0
    currentCol = 0
    expandedNodes = 0

    # While there are still nodes in the fringe
    while len(fringe) > 0:
        # Find the lowest cost node to expand
        i = 0
        lowestNode = 0
        previousNode = fringe[0]
        for node in fringe:
            if node.cost < fringe[lowestNode].cost:
                lowestNode = i
            previousNode = node
            i += 1
        currentNode = fringe.pop(lowestNode)
        expandedNodes += 1

        print('Expanded Node: ' + '(' + str(currentNode.location_row + 1) + ', ' + str(currentNode.location_col + 1) +
              ') Cost: ' + str(currentNode.cost) + ' Status: ' + str(currentNode.status))

        # If the room is dirty, clean it and check if we're finished
        if currentNode.status == 1:
            squares[currentNode.location_row][currentNode.location_col] = 0
            for row in squares:
                print(row)
            if not any(1 in square for square in squares):
                end = time.time()
                print('Expanded Nodes: ' + str(expandedNodes) +
                      ' Generated Nodes: ' + str(len(fringe) + expandedNodes) +
                      ' Execution Time: ' + str(end - start))
                print('Success')
                exit(0)
            # Add a node for the suck operation
            fringe.append(Node(currentNode.location_row,
                               currentNode.location_col,
                               currentNode.cost + action_suck,
                               0
                               ))
        # If it is in bounds, add a node for the down operation (down first because it is the lowest cost)
        if currentNode.location_row + 1 < rowNum:
            fringe.append(Node(currentNode.location_row + 1,
                               currentNode.location_col,
                               currentNode.cost + action_down,
                               squares[currentNode.location_row + 1][currentNode.location_col]
                               ))
        # If it is in bounds, add a node for the up operation (up next because it is the next lowest cost)
        if currentNode.location_row - 1 > -1:
            fringe.append(Node(currentNode.location_row - 1,
                               currentNode.location_col,
                               currentNode.cost + action_up,
                               squares[currentNode.location_row - 1][currentNode.location_col]
                               ))
        # If it is in bounds, add a node for the right operation (right next because it is the next lowest cost)
        if currentNode.location_col + 1 < colNum:
            fringe.append(Node(currentNode.location_row,
                               currentNode.location_col + 1,
                               currentNode.cost + action_right,
                               squares[currentNode.location_row][currentNode.location_col + 1]
                               ))
        # If it is in bounds, add a node for the left operation (left last because it is the highest cost)
        if currentNode.location_col - 1 > -1:
            fringe.append(Node(currentNode.location_row,
                               currentNode.location_col - 1,
                               currentNode.cost + action_left,
                               squares[currentNode.location_row][currentNode.location_col - 1]
                               ))
    print('Failure')
    exit(1)
