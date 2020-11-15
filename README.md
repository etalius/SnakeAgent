## SnakeAgent
Training an agent to play snake with reinforcement learning, specifically Q-learning. 

### Introduction
The classic game snake played on a 10x10 board where the snake attempts to eat randomly spawned apples while avoiding hitting the walls of the board or its own tail. This agent was trained using Q-learning in which it interacted with the world and recieved positive and negative rewards for 500 game to learn a policy. The policy is saved in q.csv and game.py can be run to watch the snake play the game!

### Q Learning Approach
States are represented as tuples of immediate obstacles on sides of the head of the snake, the relative horizontal location of the apple and snake head, and relative vertical location of the apple and snake head. The snake recieves a reward of +5 for eating an apple and -10 for dying. There is also a reward of +1 for moving towards the apple and -1 for moving away from the apple. After each turn, the snake updates the Q-value for the state and action pair based on the bellmen update equation. 

### Files

**game.py** File to run the game played by the agent, initializes the policy the the policy stored in q.csv.<br />
**snake.py** Snake class, updates and tracks the location of the snake and apple. <br />
**agent.py** Agent class, updates the Q table as the game is played. <br />
**q.csv** Learned policy after being trained on 500 games. 

## Results

Agent performance after 500 games:
[![ezgif-com-video-to-gif.gif](https://i.postimg.cc/SRLB36GR/ezgif-com-video-to-gif.gif)](https://postimg.cc/xNCpbbhV)
