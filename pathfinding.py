import logging
import curses
from curses import wrapper
from time import sleep

logging.basicConfig(
    filename='log.log', 
    encoding='utf-8',
    format=format("%(levelname)s :%(asctime)s = %(message)s (in %(module)s)"),
    level=logging.DEBUG)

E = "X" # END
S = "O" # START
O = "-" # OBJECT
P = " " # PATH


maze1 = [
    [O, O, O, O, S, O, O],
    [O, P, P, P, P, P, P],
    [O, P, O, O, O, P, O],
    [O, P, O, O, O, O, O],
    [O, P, O, O, O, O, O],
    [O, P, P, P, P, P, P],
    [O, O, O, O, O, E, O]
]



def main(stdscr):
    # curses.init_color(10, 225, 0, 0)
    # curses.init_color(20, 0, 0, 225)
    # curses.init_color(30, 0, 225, 0)
    # curses.init_color(40, 225, 225, 225)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)


    RED = curses.color_pair(1)
    BLUE = curses.color_pair(2)
    GREEN = curses.color_pair(3)
    WHITE = curses.color_pair(4)

    standard_color = {
        E:RED,
        P:WHITE,
        S:GREEN,
        O:BLUE
    }


    class Maze:
        def __init__(self, maze:list, stdscr, colors:dict=standard_color) -> None:
            self.maze = maze
            self.std = stdscr
            self.colors = colors
        
        def __getattr__(self, name: str) -> any:
            returnValue = []

            if name == "pathIndex":
                for column, i in enumerate(self.maze):
                    for row, j in enumerate(i):
                        if j == P:
                            returnValue.append([column, row])

            elif name == "objectIndex":
                for column, i in enumerate(self.maze):
                    for row, j in enumerate(i):
                        if j == O:
                            returnValue.append([column, row])
                            
            elif name == "startIndex":
                for column, i in enumerate(self.maze):
                    for row, j in enumerate(i):
                        if j == S:
                            returnValue = [column, row]


            elif name == "endIndex":
                for column, i in enumerate(self.maze):
                    for row, j in enumerate(i):
                        if j == E:
                            returnValue = [column, row]

            return returnValue

        def display_path(self, printBool=True):
            for row, i in enumerate(self.maze):
                for column, j in enumerate(i):
                    if printBool:
                        print(j+" ", end=" ")
                    else:
                        self.std.addstr(row, column*2, j, self.colors[j])
                
                if printBool:
                    print('\n')

        def get(self, column:int, row:int):
            return self.maze[column, row]

        def getAround(self, currentColumn:int, currentRow:int, matrixReturn=False, printIn=False, useStd=False):
            returnValue = []

            iterationList = [
                [-1, -1],
                [0, -1],
                [1, -1],
                [1, 0],
                [1, 1],
                [0, 1],
                [-1, 1],
                [-1, 0]
            ]

            printPos = [
                [0, 0],
                [1, 0],
                [2, 0],
                [2, 1],
                [2, 2],
                [1, 2],
                [0, 2],
                [0, 1]
            ]
            for index, pos in enumerate(iterationList):
                printIndex = printPos[index]
                index1 = currentColumn + pos[0]
                index2 = currentRow + pos[1]
                if not matrixReturn:
                    try:
                        if printIn:
                            if useStd:
                                self.std.addstr(printIndex[1], printIndex[0]*2, self.maze[index2][index1])
                                logging.info(str(self.maze[index2][index1])) # LOGGING
                            else:
                                print(self.maze[index1][index2])
                        else:
                            returnValue.append(self.maze[index1][index2])
                    except:
                        if printIn:
                            if useStd:
                                self.std.addstr(printIndex[1], printIndex[0], "R")
                            else:
                                print(None)
                        else:
                            returnValue.append(None)
                else:
                    if printIn:
                        if useStd:
                            self.std.addstr(printIndex[1], printIndex[0], str([index2, index1]))
                        else:
                            print([index1, index2])
                    else:
                        returnValue.append([index1, index2])

            if not printIn:
                return returnValue

        def displayAround(self, currentColumn:int, currentRow:int):
            around = self.getAround(currentColumn, currentRow)
            around.insert(4, " ")
            logging.info(' '.join(around))
            stdscr.getch()
            for index, i in enumerate(around):
                if (index + 1) % 3 == 0:
                    print("\n")

                print(i, end=" ")

                    

    class PathFinding:
        def __init__(self) -> None:
            self.result = ""
            
        def __str__(self) -> str:
            return self.result

        def process(self, maze:Maze, pos:tuple):
            self.result = ""
            currentIndex = maze.startIndex
            maze.getAround(pos[0], pos[1], printIn=True, useStd=True)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)

    RED = curses.color_pair(1)
    BLUE = curses.color_pair(2)

    stdscr.clear()
    Maze1 = Maze(maze1, stdscr=stdscr)
    Maze1.display_path(printBool=False)
    stdscr.getch()
    stdscr.clear()
    path = PathFinding()
    path.process(Maze1, (1, 4))
    stdscr.refresh()
    stdscr.getch()

wrapper(main)
