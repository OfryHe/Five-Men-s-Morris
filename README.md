# Five-Men-s-Morris
The project is based on a game called Five Men's Morris. The project includes full implementation of the game's logic, reinforcement learning and neural network ANN algorithms based agents, as well as a full GUI system.

All the models and dictionaries are saved in hugging face. repository name: "Five_Mens_Morris".
link: https://huggingface.co/OfryH/Five_Mens_Morris

Five Men's Morris Rules:

        1. Placement Phase (First 5 turns for each player):

           - Players take turns placing their pieces on any empty point on the board.

           - If a player forms a mill (three of their pieces in a straight line), they immediately remove one of their opponent's pieces that is not part of a mill.


        2. Moving Phase (After all pieces are placed):

           - Players take turns moving one of their pieces to an adjacent empty point along the lines of the board.

           - A player who forms a mill by moving a piece may remove one opponent's piece that is not part of a mill.
           

        3. Flying Phase (When a player has only 3 pieces left):

           - That player may move any of their pieces to any empty point on the board, not just adjacent ones.

           - The mill rule still applies.

        Winning the Game:

        - A player wins when their opponent has less than 3 pieces remaining, or when their opponent cannot make a legal move.

Important classes:
  1. Game(responsible for creating the game itself and playing a singular game):

       -  play_one_game : responsible for playing a single game(has many versions that include different agent styles such as: random player against random agent, random player against smart agent etc...).
       -  agent_turn : responsible for making a turn for the agent(which represents the computer), 3 versions that represents 3 types.
  
