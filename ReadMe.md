# Colosseum Survival!

<p align="center">
  <img src="https://cdn.britannica.com/36/162636-050-932C5D49/Colosseum-Rome-Italy.jpg?w=690&h=388&c=crop">
</p>

## Note

We currently only support $`2`$-player version of this game. 

## Playing a game

To start playing a game, we need to implement _agents_. For example, to play the game using two random agents (agents which take a random action), run the following:

```bash
python simulator.py --player_1 random_agent --player_2 random_agent
```

This will spawn a random game board of size NxN, and run the two agents. You will be able to see their moves in the console.

## Visualizing a game

To visualize the moves within a game, use the `--display` flag. You can set the delay (in seconds) using `--display_delay` argument to better visualize the steps the agents take to win a game.

```bash
python simulator.py --player_1 random_agent --player_2 random_agent --display
```

## Play on your own!

To play the game on your own, use a `human_agent` to play the game.

```bash
python simulator.py --player_1 human_agent --player_2 random_agent --display
```

## Autoplaying multiple games

Since boards are drawn randomly (between a `MIN_BOARD_SIZE` and `MAX_BOARD_SIZE`) you can compute an aggregate win % over your agents. Use the `--autoplay` flag to run $n$ games sequentially, where $n$ can be set using `--autoplay_runs`.

```bash
python simulator.py --player_1 random_agent --player_2 random_agent --autoplay
```

**Notes**

- Not all agents supports autoplay. The variable `self.autoplay` in Agent can be set to `True` to allow the agent to be autoplayed. Typically this flag is set to false for a `human_agent`.
- UI display will be disabled in an autoplay.

## Write your own agent

You need to write your own agent and submit it for the class project. To do so: 

1. Create a new file in `agents/` directory, and extend the `agents.Agent` class. 
2. Implement the `step` function with your game logic
3. Register your agent using the decorator `register_agent`
4. Import your agent in the `__init__.py` file in `agents/` directory
5. Run and test your agent using the information above
6. Check autoplay with your agent and `random_agent` is working

## Full API

```bash
python simulator.py -h       
usage: simulator.py [-h] [--player_1 PLAYER_1] [--player_2 PLAYER_2]
                    [--board_size BOARD_SIZE] [--display]
                    [--display_delay DISPLAY_DELAY]

optional arguments:
  -h, --help            show this help message and exit
  --player_1 PLAYER_1
  --player_2 PLAYER_2
  --board_size BOARD_SIZE
  --display
  --display_delay DISPLAY_DELAY
  --autoplay
  --autoplay_runs AUTOPLAY_RUNS
```


## Gameboard

<p align="center">
  <img src="Gameboard.png" width="600" height="600">
</p>

## Game Setting
On an $`M \times M`$ chess board, $`n`$ players are randomly distributed on the board with one player occupying one block.

## Game Moving
In each iteration, one player moves at most $`K`$ steps (between $`0`$ and $`K`$) in either horizontal or vertical direction, and must put a barrier around him or her in one of the 4 directions except the boarders of the chess board. The players move in a round-robin way.

### Note: 
 - Each player cannot go into other player's place or put barriers in areas that already have barriers.
 - Currently the maximal number of steps is set to $`K = (M + 1) // 2`$.

## Game Ending
The game ends when each player is separated in a closed zone by the barriers and boundaries. The final score for each player will be the number of blocks in that zone.
```math
S_i = \#\text{Blocks of Zone}_i
```

## Goal
Each player should maximize the final score of itself, i.e., the number of blocks in his zone in the endgame.

## Example Gameplay
Here we show a gameplay describing a $`2`$-player game on a $`5\times 5`$ chessboard. Each player can move at most $`3`$ steps in each round.

<p align="center">
  <img src="Gameplay.gif" width="600" height="600">
</p>

The final score is $`A:B = 15:10`$. So A wins the game.
