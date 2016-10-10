# AI Bot for playing 8 puzzle

The 8-puzzle (also called Gem Puzzle, Boss Puzzle, Game of Eight, Mystic Square and many others) is a sliding puzzle that consists of a frame of numbered square tiles in random order with one tile missing

## Getting Started

The project is hosted on Github, there are a number of ways to download it:
* Clone the git repository via https, ssh or with the Github Windows or Mac clients.
* Download as zip or tar.gz

### Prerequisities

The project requires the following things before you can play the game:
* Python version > 3
* PyAutoGui
* A working internet connection, as the game is hosted online

### Installing

If you are using Linux or Mac OS then you don't need to do anything to install python, you can simply use the interpreter by opening the terminal and typing the command.

```
python3 main.py
```

For windows systems, the steps are a bit more complex. You can use this guide in order to properly setup python on you windows desktop [How to Install Python on Windows](http://www.howtogeek.com/197947/how-to-install-python-on-windows/). Remember that you need to install a version > 3 for this project.

Pyautogui provied a cross platform python module for gui automation. We will be using it for performing tasks like geting the game configuration and performing click. [Use this guide for installing Pyautogui.](https://pyautogui.readthedocs.io/en/latest/install.html)

## Running the game

* Open the website [Online Eight Puzzle](http://mypuzzle.org/sliding)
* Make sure that the game are is not obstructed by anything like the mouse of other windows
* While the game are is still visible run the code by the command:
```
python3 main.py
```
The bot will try and find the game region on screen and then figure out the board configuration. The bot uses Image procesing to this and may fail depending on various factors, but it will work for the most part.

## How does the bot work

The bot treats the game as a search problem. Each move that you can made from a state is added as a node in the state space search tree. After this bot only need to traverse this tree and find the optimal route to the goal state.

The search tree of 8 puzzle problem can be quite large, a simple solution such as BFS could take several minutes before it gives the answer. So in order to speed up the search we will be using A Start search.

Using A Start search the bot is able to calculate the path to the goal state in just a few seconds.

### Heuristic

A Start Search is quite similar to the greedy Uniform Cost Search except for the fact that is directed by a heuristic. The heuristic is simple measure of how far away you think you are from the goal state. This allows the search to concentrate on regions that will get it closer to the goal state.

For the 8 puzzle the heuristic that I have used is the manahattan distance of each number from its expected position.

For example, If the expected board configuration is (0 is the blank slot):
```
0 1 2 
3 4 5 
6 7 8
```
and the current state is:
```
0 2 3 
1 4 6
7 8 5
```
then the heuristic will return the sum of the manhatan distance of each number from its expected position
```
0 1 2 3 4 5 6 7 8
0 2 3 1 4 6 7 8 5
-----------------
0 2 1 3 0 1 4 1 1    manahatan distance of each number

heuristic = 13
```

This heuristic is both admissible and consistent and is constantly decreasing the closer we get to the end goal state
## Built With

* Python
* PyAutoGui

## Contributing

The code is open for anyone to copy and modify. Feel free to use it as a base for you own projects. I have tried to make the code as modular as possible so that adding new features is easy.
 

## Authors

* [**Saurabh Kumar**](https://github.com/saurabh-kumar-vit)
