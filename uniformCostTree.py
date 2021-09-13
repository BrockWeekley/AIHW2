import json

if __name__ == '__main__':
    print('Uniform Cost Tree')
    inputFile = open('instanceOne.json')
    squares = json.load(inputFile)['squares']
    startingRow = 0
    startingCol = 0

    rowNum = 0
    colNum = 0

    for row in squares:
        rowNum += 1
        for col in row:
            colNum += 1
            if col == 2:
                startingCol = colNum
                startingRow = rowNum
                squares[rowNum - 1][colNum - 1] = 0
        colNum = 0

    print(squares)
    print(str(startingRow) + " " + str(startingCol))