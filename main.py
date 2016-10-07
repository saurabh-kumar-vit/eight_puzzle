'''
    Created By Saurabh Kumar

    This a bot that plays an online version of the popular game '8 Puzzle' hosted on http://mypuzzle.org/sliding
    It uses the A star search algorithm along with the manhatan distance heuristic for quickly traverse
    the state space of the game.

    It is a fully automated bot and is able to very quickly find out the optimal path by just evaluating 
    very few nodes.
'''

import pyautogui, time, os, sys, random, copy
from queue import PriorityQueue    

''' 
    width 457
    height 449

    These are the fixed width and height of the game region, 
    the game is not responsive to window size, so using hard coded 
    values works just fine
'''

WIDTH = 457
HEIGHT = 449
GAME_REGION = ()

NODES = 0

'''
    the reletive position of each block to the top left corner of the game region
'''
REGIONS = {
    (82, 80): 0,
    (182, 80): 1,
    (282, 80): 2,
    (82, 180): 3,
    (182, 180): 4,
    (282, 180): 5,
    (82, 280): 6,
    (182, 280): 7,
    (282, 280): 8
}



BLANK = ()


def imPath(filename):
    return os.path.join('images', filename)
'''
    automating the process of finding the game region on the screen,
    it tries to find the game region based on the location of certain
    buttons that dont change position relative to game region.
'''
def getGameRegion():
    global GAME_REGION, HEIGHT

    searchParameter = imPath('searchGame.png')
    region = pyautogui.locateOnScreen(searchParameter)

    if region == None:
        print ('Game region cannot be found')

    topx = region[0]
    topy = region[1] + region[3]

    GAME_REGION = (topx, topy, WIDTH, HEIGHT)

'''
    find out what the configuration of the board is.
'''
def findNumberLoc():
    '''
        The board is stored as a 1D array in order to reduce space usage,
        this allows for qucikly checking for win, and generating successors.
    '''
    numbers = [0 for _ in range(9)]

    for num in range(1, 9):
        numberImg = imPath('numbers/' + str(num) + '.png')
        region = pyautogui.locateOnScreen(numberImg)

        if region != None:
            region = (region[0] - GAME_REGION[0], region[1] - GAME_REGION[1])
            numbers[REGIONS[region]] = num

    return numbers

def isGoalState(state):
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    return state == goal

def getSuccessor(state):
    blank = state.index(0)

    top = blank - 3
    bottom = blank + 3
    left = blank - 1
    right = blank + 1

    legalMoves = []

    if blank not in [0, 3, 6]:
        legalMoves.append(left)
    if blank not in [0, 1, 2]:
        legalMoves.append(top)
    if blank not in [2, 5, 8]:
        legalMoves.append(right)
    if blank not in [6, 7, 8]:
        legalMoves.append(bottom)

    successor = []
    for move in legalMoves:
        copyState = state[:]
        copyState[blank], copyState[move] = copyState[move], copyState[blank]
        successor.append((copyState, move))

    return successor

def tostr(li):
    return ''.join([str(x) for x in li])

'''
    supporting function for A start algo,
    it calculates the manhatan distance between the required and actual position.
    this calcuation is a little diffrent since the array is 1D.
'''
def heuristic (state):
    goalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    for position, number in enumerate(goalState):
        positionInState = state.index(number)
        rowOfGoalNumber = position // 3
        rowOfStateNumber = positionInState // 3

        colTraversal = abs(rowOfStateNumber - rowOfGoalNumber)

        lowerNumber = min(position, positionInState)
        highNumber = max(position, positionInState)

        rowTraversal = abs((lowerNumber + (3 * colTraversal) - highNumber))

        return rowTraversal + colTraversal

def aStarSearch (root):
    global NODES

    visited = set()
    fringe = PriorityQueue()
    fringe.put((0, (root, [], 0)))

    while fringe:
        node, path, cost = fringe.get()[1]
        if isGoalState(node):
            return path
        for successor, move in getSuccessor(node):
            if tostr(successor) not in visited:
                gx = cost + 1
                hx = heuristic(successor)
                fx = hx + gx
                fringe.put((fx, (successor, path + [move], gx)))
                NODES += 1

        visited.add(tostr(node))
    return []   

'''
    automated method to perform clicks on an array of moves,
    a move is a location at which the mouse must be clicked
'''
def clickPlay (moves):
    CLICK_REGION = {
        0: (127 + GAME_REGION[0], 127 + GAME_REGION[1]),
        1: (227 + GAME_REGION[0], 127 + GAME_REGION[1]),
        2: (327 + GAME_REGION[0], 127 + GAME_REGION[1]),
        3: (127 + GAME_REGION[0], 227 + GAME_REGION[1]),
        4: (227 + GAME_REGION[0], 227 + GAME_REGION[1]),
        5: (327 + GAME_REGION[0], 227 + GAME_REGION[1]),
        6: (127 + GAME_REGION[0], 327 + GAME_REGION[1]),
        7: (227 + GAME_REGION[0], 327 + GAME_REGION[1]),
        8: (327 + GAME_REGION[0], 327 + GAME_REGION[1])
    }

    pyautogui.PAUSE = 1.0

    pyautogui.click(CLICK_REGION[4])

    for move in moves:
        pyautogui.click(CLICK_REGION[move])

def main():
    global BLANK, NODES

    print ('Finding game region .... ')
    getGameRegion()
    print ('Game region found, getting board configuration ....')
    root = findNumberLoc()
    print ('The board configuration is ....')
    print (root)

    print ('Finding Solution for the current configuration ....')
    move = aStarSearch(root)

    print ('Nodes expanded : ', NODES)
    print ('The Solution is')
    print (move)

    clickPlay(move)
    
if __name__ == '__main__':
    main()
