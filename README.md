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
       -  agent_turn : responsible for making a turn for the agent(which represents the computer), 3 versions that represents 3 types of players(random, ANN based, dictionary based).

  2. Games(responsile for creating the dictionaries):
       - play_1000000_games : responsible for playing a million games and saving every board found and adding the boards to the dictionary if it doesn't exist already or recalculate the points awarded to the board if needed. this function has multiple versions for every kind of agent versus player types(random v random, smart v random, smart v smart etc...)

  3. FirstScreen(The screen that the player is able to interact with)
  4. Controller(connects between the games logic and the games GUI(FirstScreen)
  5. Logic(Responsible for the logic behind the game)

MVC methodology(used in the GUI creation):     
           Separate concerns: MVC divides an application into three interconnected parts, the Model (Logic), the View (FirstScreen), and the Controller (Controller), making development more organized and manageable.
           Improve maintainability: Code becomes easier to update and debug since changes in one component don't affect others.
           Enable code reusability: The modular structure allows for reuse of components across different parts of the application, reducing redundancy.

Reinforcement Learning(using dictionaries): 
           The agent uses a system of five dictionaries to store game states and their associated rewards, optimizing move selection.
           Initialization Dictionary (dict1): Focused on the early placement phase of the game.
           Regular Dictionary (dict2): For the general gameplay after the placement phase.
           Player Special Dictionary (dict3): Stores states where the player has only three pieces, entering the 'flying' phase.
           Agent Special Dictionary (dict4): Stores states where the agent has only three pieces.
           Special Dictionary (dict5): Captures states where both the agent and the player have three pieces.
           This division into five dictionaries allows the agent to more accurately evaluate board states and make more informed decisions based on the specific phase of the game.  The dictionaries are populated by having agents play against different types of agents and players(random v random, random player v smart             agent, random player v 80% smart agent and 20% random agent, smart player v smart agent) reaching 20 million games played and saved, ensuring a wide variety of encountered board states. The rewards for each state are updated using temporal difference learning. The dictionary is saved in a json file. When               the agent encounters a board that already exists in the dictionary, it will choose the move that will lead to the highest reward.



ANN based agent:
           The agent uses a four-layer neural network to predict the best move.  The network is trained on games played by the reinforcement learning agent, enabling it to generalize to unseen board states.  The layers are as follows:
           Input Layer: Receives the game board state (128 neurons).
           Hidden Layer 1: Learns complex features (64 neurons, ReLU activation).
           Hidden Layer 2: Refines learned representations (32 neurons, ReLU activation).
           Output Layer: Predicts move desirability (1 neuron, linear activation, output range: -1 to 1).
           The model uses the Adam optimizer and mean squared error loss function.
 
