*This project has been created as part of the 42 curriculum by khnoman , aayat .*

# 🟡  👻 Pac_Man 🟡  👻


## Description 


Pac-Man is a recreation of the classic arcade game developed in Python. The player navigates through a maze, collects pac-gums, and avoids ghosts to complete each level. The game includes multiple levels, AI-controlled ghosts, collision detection, score tracking, and a highscore system.

### Features

+ Player Movement: Control Pac-Man and navigate through the maze.

+ Ghost AI: Four different ghosts with individual identities and behaviors:

    + Blinky

    + Pinky

    + Inky

    + Clyde

+ Ghost States: Ghosts can switch between Chase, Scatter, Frightened, and Eaten states.

+ Pac-Gums: Collect Pac-Gums to increase your score.

+ Super Pac-Gums: Temporarily frighten ghosts, allowing Pac-Man to eat them.

+ Multiple Levels: Progress through 10 levels with different mazes.

+ Scoring System: Earn points by collecting Pac-Gums and eating frightened ghosts.

+ Lives System: Start with three lives.

+ Highscore: Track and display the best game scores.

+ Game States: Menu, Playing, Paused, Game Over, and Victory.

+ Cheats: Support additional gameplay options.

## Instructions

### Installation
1. Clone the repository:

    -   git clone [repository-url]

    -   cd [project-directory]

2.   Install the required dependencies:

        -   make install

### Execution
1. Run the game using:

    -   make run


### Configuration

The game uses a configuration system to manage gameplay parameters.

The default configuration includes:

| Parameter                 | Default Value      |
|-------------------------- |--------------------|
| number of lives           |  3                 |
| pac-gums per level        | 5                  |
| pac-gums score            | 10                 |
| super pac-gums score      |     20             |
| eaten ghost               | 100                |
| seed                      |  42                |
| level time                | 90                 |


### Highscore

The highscore system keeps track of player performance.

It is designed to:

Record completed game scores.

Compare scores to identify the highest results.

Display the leaderboard.

The scoring system rewards players for collecting Pac-Gums, collecting Super Pac-Gums, and eating frightened ghosts.

### Maze Generation

The game uses the A-Maze-ing maze generation project to generate the game mazes.

Maze generation is responsible for creating the maze structure and defining the available paths and walls.

The generated maze is represented as a grid, where each cell contains information about its surrounding walls.



## Resources

[pac_mac logic ](https://www.geekslop.com/old-school/2020/the-logic-and-programming-behind-pac-man-all-the-crazy-cool-stuff-you-ever-wanted-to-know-about-how-the-classic-pac-man-game-works-under-the-hood)   
[Greedy algorithm](https://plainenglish.io/python/greedy-algorithm-in-python-4b66e250d088)

### Ai usage
-  Understanding programming concepts and algorithms.
-  Improving code documentation and project structure.