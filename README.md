# Tic-Tac-Toe-AI
This repository contains code to train a agent to play Tic-Tac-Toe using a reinforcement learning approach - Q learning
<p align="center">
<img src="/AI_draws.gif"/> 
</p>

## Training Summary

* The AI was trained with self-play
* After completion of each game, the Q-table was updated based on:

   **Qnew = Qprev + α * (R + γ * Max(Q) - Qprev)**

    _α = learning rate_
    
    _R = reward for latest action_
    
    _γ = discount factor_
    
    _Max(Q) = estimate of new value from best action_
* The exploration rate was intially set to 0.7 and decayed as number of games increased
* After 200K games, the AI seems to make the best moves 

