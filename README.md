# Tron Light Cycle Agent

## Project Overview

An AI agent developed to play the *Tron Light Cycle* game, originally inspired by the Codingame challenge. The game is a turn-based survival competition where two light cycles (players) move on a 30x20 grid, leaving trails behind. The player who avoids crashing into trails or going out of bounds the longest wins.

This agent uses adversarial search techniques, combining **Minimax with Alpha-Beta Pruning** and a **Flood Fill-based evaluation strategy** to make optimal decisions each turn within strict time constraints (100ms per move).

<p align="center">
  <img src="https://github.com/AmirAAZ818/AI-Final-Project-2024/blob/main/Assets/Battle.gif" alt="Tron Battle">
  <div align="center">
    <figcaption><em align="center">I'm the yellow light bar :)</em></figcaption>
  </div>
</p>

---

## State Type

The game operates in a **discrete, deterministic, fully observable, static, and turn-based environment**. The game state (grid and positions of agents) does not change unless an agent makes a move, and agents receive complete state information every turn.

---

## Key Features

* **Minimax with Alpha-Beta Pruning:** Efficient two-player adversarial search algorithm used to simulate and evaluate future game states.
* **Lazy Flood Fill Evaluation:** A BFS-based evaluation that estimates the free space available to both players and strategically compares territory control. A lazy mechanism is also integrated to meet the time constraint.
* **Scalable Depth Search:** Supports configurable search depth to trade off between decision quality and runtime performance.

---

## File Structure

```bash
tron_bot.py          # Main AI code
test_tron_ai.py      # Independent tester script
sample_input.txt     # Optional: example input for redirection
README.md            # This file
```

---

## How It Works

Each turn, the AI agent performs the following:

1. **Reads input** from standard input:

   * Total number of players `N`
   * Your player number `P`
   * For each player, the tail and head of their light ribbon: `(X0, Y0, X1, Y1)`

2. **Parses the game state** into a grid of size 30x20 (width x height).

   * Cells occupied by light ribbons are marked with player numbers.
   * Cells are updated every turn to reflect the current game status.

3. **Checks for valid moves** using the `get_actions()` function, which evaluates all 4 cardinal directions and filters out invalid or dangerous paths.

4. **Calls the Minimax algorithm** with alpha-beta pruning to simulate future game states:

   * Explores potential outcomes up to a fixed depth
   * Uses flood fill to estimate available space for both players in each state
   * Selects the action that maximizes the agent's space advantage over the opponent

5. **Prints the chosen direction** (`UP`, `DOWN`, `LEFT`, or `RIGHT`) to standard output.

---

## Example Input/Output

Let’s consider a full input-output cycle for a turn:

```plaintext
Input:
2 0                # N=2 players, P=0 (you are Player 0)
9 5 9 5            # Player 0 starts at (9,5), no movement yet
10 7 10 7          # Player 1 starts at (10,7), no movement yet

Output:
RIGHT              # You move from (9,5) to (10,5)
```

The next turn would then have:

```plaintext
Input:
2 1
9 5 10 5           # Player 0 moved RIGHT
10 7 10 7          # Player 1 hasn't moved yet
```

On subsequent turns, players continue making moves in turns. The game ends when a player hits a wall, trail, or edge.

---

## Running the Code

### Requirements

* Python 3.x
* `numpy`

Install the required package (if not already):

```bash
pip install numpy
```

### How to Run

You can run the agent using a static input simulation by redirecting a prepared input file, like:

```bash
python tron_bot.py < sample_input.txt
```

### Testing with Sample Inputs

You can also test it with this Python testing script that runs 5 sample turns:

```bash
python test_tron_bot.py
```
