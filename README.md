# Planes
Planes, Board Game (similar to Battleships) - Python implementation using Object-Oriented Programming and Layered Architecture

Planes is a board game in which each player draws 3 planes on his own 10x10 board. Players take turns by saying the name of a cell (for example E9) and the other player 
gives a response: miss, hit or dead, depending of whether there is a part of a plane on that cell or not. A plane is dead only if its head has been hit. The goal is to 
'kill' all 3 planes of the opponent. The winner is the first player who accomplishes this.

The game has a console based user interface. It interacts with the user by waiting for him to enter commands: either the name of a cell, the orientation of a plane or
what player takes the first hit. 

It is a Computer vs. Human game. The computer strategy is designed in the following way: the planes are placed in a random manner (because placing the planes completely 
random is already a good strategy itself; the planes could be exactly one near another, therefore it can be very hard for a human player to distinguish which plane is 
which); first moves of the computer are in the center of the board (most likely cells to contain a part of a plane), then on the neighboring cells of the center cells 
and so on... Whenever the computer hits a plane, it continues to hit all the neighboring cells (in random order), performing a DFS (Depth-First Search), a simulation
of a stack being used to achieve that.

The game can be played by running the file start.py
