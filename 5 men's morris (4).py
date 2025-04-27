import numpy as np
import random
import json


class Games:#builds the dictionary that contains the points of each board
    def __init__(self):
        self.x = list() #a list that saves every final board of every game
        self.y = list() #a list that saves every winner of every game
        self.dict_reg = {} #a dictionary that contains every board where the agent and the player have 4-5 soldiers
        self.dict_init = {}#a dictionary that contains every board where the players place their soldiers on the board
        self.dict_player_special = {} #a dictionary that contains every board where the agent has 4-5 soldiers and the player has 3
        self.dict_agent_special = {}#a dictionary that contains every board where the player has 4-5 soldiers and the agent has 3
        self.dict_special = {} #a dictionary that contains every board where the agent has 4-5 soldiers and the player has 3
        self.playerWin = 0 #amount of times the player has won
        self.agentWin = 0 #amount of times the agent has won
        self.ties = 0 #amount of times there was a tie

    def players_count(self, player, string): #returns the amount of soldiers in the board for the player recieved
        count = 0
        for n in range(len(string)):
            if player == 1:
                if string[n] == 'x':
                     count+=1
            else:
                if string[n] == 'o':
                     count+=1
        return count

    def games_100000_explore_explicit(self, dict_init, dict_reg, dict_player_special, dict_agent_special, dict_special):
        #builds the dictionary while every 5 turns the agent makes a random move
        count_boards_found = 0
        count_boards_not_found = 0
        count_boards_found1 = 0
        count_boards_not_found1 = 0
        count_turns = 0
        for i in range(1000000):
            my_game = Game()
            initiate = True
            count_boards_found1, count_boards_not_found1, count_turns = my_game.play_one_game_explore_explicit(dict_init, dict_reg, dict_player_special, dict_agent_special, dict_special, count_boards_found, count_boards_not_found,count_turns)
            count_boards_found = count_boards_found1
            count_boards_not_found = count_boards_not_found1
            listStr = my_game.gamesStr

            for j in range(len(listStr)):
                key = listStr[j][0]
                points = listStr[j][1]
                if points != 0:
                    if j<10:
                        if listStr[j][0] in dict_init:
                            dict_init[key] = ((dict_init[key][0] * dict_init[key][1] + points) / (dict_init[key][1] + 1),dict_init[key][1] + 1)
                        else:
                            dict_init[key] = (points, 1)
                    else:
                        if self.players_count(1,key) > 3 and self.players_count(-1,key) > 3:
                            if listStr[j][0] in dict_reg:
                                dict_reg[key] = ((dict_reg[key][0]*dict_reg[key][1]+points)/(dict_reg[key][1]+1),dict_reg[key][1]+1)
                            else:
                                dict_reg[key] = (points,1)
                        elif self.players_count(1,key) > 3 and self.players_count(-1,key) == 3:
                            if listStr[j][0] in dict_player_special:
                                dict_player_special[key] = ((dict_player_special[key][0]*dict_player_special[key][1]+points)/(dict_player_special[key][1]+1),dict_player_special[key][1]+1)
                            else:
                                dict_player_special[key] = (points,1)
                        elif self.players_count(1,key) == 3 and self.players_count(-1,key) > 3:
                            if listStr[j][0] in dict_agent_special:
                                dict_agent_special[key] = ((dict_agent_special[key][0]*dict_agent_special[key][1]+points)/(dict_agent_special[key][1]+1),dict_agent_special[key][1]+1)
                            else:
                                dict_agent_special[key] = (points,1)
                        else:
                            if listStr[j][0] in dict_special:
                                dict_special[key] = ((dict_special[key][0]*dict_special[key][1]+points)/(dict_special[key][1]+1),dict_special[key][1]+1)
                            else:
                                dict_special[key] = (points,1)
            self.x.append((my_game.outside_board,my_game.inside_board))
            winner = my_game.check_win()
            the_winner = ""
            if winner == 1:
                self.agentWin+=1
                the_winner = "agent"
            else:
                if winner == -1:
                    self.playerWin += 1
                    the_winner = "player"
                else:
                    self.ties += 1
                    the_winner = "draw"
            self.y.append(the_winner)
        print("the agent won ",self.agentWin," games")
        print("the player won " ,self.playerWin , " games")
        print("there were ", self.ties, " ties")

        # np.save('final board', self.x)
        # np.save('winner', self.y)
        return dict_init, dict_reg, dict_player_special,dict_agent_special,dict_special, count_boards_found, count_boards_not_found

    def games_100000(self, dict_init, dict_reg, dict_player_special, dict_agent_special, dict_special):
        #builds the dictionary while the agent plays using the dictionary and the player plays randomly
        count_boards_found = 0
        count_boards_not_found = 0
        count_boards_found1 = 0
        count_boards_not_found1 = 0
        for i in range(1000000):
            my_game = Game()
            initiate = True
            count_boards_found1, count_boards_not_found1 = my_game.play_one_game_smart_agent(dict_init, dict_reg, dict_player_special, dict_agent_special, dict_special, count_boards_found, count_boards_not_found)
            count_boards_found = count_boards_found1
            count_boards_not_found = count_boards_not_found1
            listStr = my_game.gamesStr

            for j in range(len(listStr)):
                key = listStr[j][0]
                points = listStr[j][1]
                if points != 0:
                    if j<10:
                        if listStr[j][0] in dict_init:
                            dict_init[key] = ((dict_init[key][0] * dict_init[key][1] + points) / (dict_init[key][1] + 1),dict_init[key][1] + 1)
                        else:
                            dict_init[key] = (points, 1)
                    else:
                        if self.players_count(1,key) > 3 and self.players_count(-1,key) > 3:
                            if listStr[j][0] in dict_reg:
                                dict_reg[key] = ((dict_reg[key][0]*dict_reg[key][1]+points)/(dict_reg[key][1]+1),dict_reg[key][1]+1)
                            else:
                                dict_reg[key] = (points,1)
                        elif self.players_count(1,key) > 3 and self.players_count(-1,key) == 3:
                            if listStr[j][0] in dict_player_special:
                                dict_player_special[key] = ((dict_player_special[key][0]*dict_player_special[key][1]+points)/(dict_player_special[key][1]+1),dict_player_special[key][1]+1)
                            else:
                                dict_player_special[key] = (points,1)
                        elif self.players_count(1,key) == 3 and self.players_count(-1,key) > 3:
                            if listStr[j][0] in dict_agent_special:
                                dict_agent_special[key] = ((dict_agent_special[key][0]*dict_agent_special[key][1]+points)/(dict_agent_special[key][1]+1),dict_agent_special[key][1]+1)
                            else:
                                dict_agent_special[key] = (points,1)
                        else:
                            if listStr[j][0] in dict_special:
                                dict_special[key] = ((dict_special[key][0]*dict_special[key][1]+points)/(dict_special[key][1]+1),dict_special[key][1]+1)
                            else:
                                dict_special[key] = (points,1)
            self.x.append((my_game.outside_board,my_game.inside_board))
            winner = my_game.check_win()
            the_winner = ""
            if winner == 1:
                self.agentWin+=1
                the_winner = "agent"
            else:
                if winner == -1:
                    self.playerWin += 1
                    the_winner = "player"
                else:
                    self.ties += 1
                    the_winner = "draw"
            self.y.append(the_winner)
        print("the agent won ",self.agentWin," games")
        print("the player won " ,self.playerWin , " games")
        print("there were ", self.ties, " ties")

        # np.save('final board', self.x)
        # np.save('winner', self.y)
        return dict_init, dict_reg, dict_player_special,dict_agent_special,dict_special, count_boards_found, count_boards_not_found

    def games_100000_smartest(self, dict_init, dict_reg, dict_player_special, dict_agent_special, dict_special):
        #builds the dictionary while the agent and the player play cleverly
        count_boards_found = 0
        count_boards_not_found = 0
        count_boards_found1 = 0
        count_boards_not_found1 = 0
        for i in range(1000000):
            my_game = Game()
            initiate = True
            count_boards_found1, count_boards_not_found1 = my_game.play_one_game_smartest(dict_init, dict_reg, dict_player_special, dict_agent_special, dict_special, count_boards_found, count_boards_not_found)
            count_boards_found = count_boards_found1
            count_boards_not_found = count_boards_not_found1
            listStr = my_game.gamesStr

            for j in range(len(listStr)):
                key = listStr[j][0]
                points = listStr[j][1]
                if j<10:
                    if listStr[j][0] in dict_init:
                        dict_init[key] = ((dict_init[key][0] * dict_init[key][1] + points) / (dict_init[key][1] + 1),dict_init[key][1] + 1)
                    else:
                        dict_init[key] = (points, 1)
                else:
                    if self.players_count(1,key) > 3 and self.players_count(-1,key) > 3:
                        if listStr[j][0] in dict_reg:
                            dict_reg[key] = ((dict_reg[key][0]*dict_reg[key][1]+points)/(dict_reg[key][1]+1),dict_reg[key][1]+1)
                        else:
                            dict_reg[key] = (points,1)
                    elif self.players_count(1,key) > 3 and self.players_count(-1,key) == 3:
                        if listStr[j][0] in dict_player_special:
                            dict_player_special[key] = ((dict_player_special[key][0]*dict_player_special[key][1]+points)/(dict_player_special[key][1]+1),dict_player_special[key][1]+1)
                        else:
                            dict_player_special[key] = (points,1)
                    elif self.players_count(1,key) == 3 and self.players_count(-1,key) > 3:
                        if listStr[j][0] in dict_agent_special:
                            dict_agent_special[key] = ((dict_agent_special[key][0]*dict_agent_special[key][1]+points)/(dict_agent_special[key][1]+1),dict_agent_special[key][1]+1)
                        else:
                            dict_agent_special[key] = (points,1)
                    else:
                        if listStr[j][0] in dict_special:
                            dict_special[key] = ((dict_special[key][0]*dict_special[key][1]+points)/(dict_special[key][1]+1),dict_special[key][1]+1)
                        else:
                            dict_special[key] = (points,1)
            self.x.append((my_game.outside_board,my_game.inside_board))
            winner = my_game.check_win()
            the_winner = ""
            if winner == 1:
                self.agentWin+=1
                the_winner = "agent"
            else:
                if winner == -1:
                    self.playerWin += 1
                    the_winner = "player"
                else:
                    self.ties += 1
                    the_winner = "draw"
            self.y.append(the_winner)
        print("the agent won ",self.agentWin," games")
        print("the player won " ,self.playerWin , " games")
        print("there were ", self.ties, " ties")

        # np.save('final board', self.x)
        # np.save('winner', self.y)
        return dict_init, dict_reg, dict_player_special,dict_agent_special,dict_special, count_boards_found, count_boards_not_found


    def games_100000_dumb1(self, dict_init, dict_reg, dict_player_special, dict_agent_special, dict_special):
        #builds the dictionary while both players play randomly
        for i in range(1000000):
            my_game = Game()
            initiate = True
            my_game.play_one_game()
            listStr = my_game.gamesStr

            for j in range(len(listStr)):
                key = listStr[j][0]
                points = listStr[j][1]
                if j<10:
                    if listStr[j][0] in dict_init:
                        dict_init[key] = ((dict_init[key][0] * dict_init[key][1] + points) / (dict_init[key][1] + 1),dict_init[key][1] + 1)
                    else:
                        dict_init[key] = (points, 1)
                else:
                    if self.players_count(1,key) > 3 and self.players_count(-1,key) > 3:
                        if listStr[j][0] in dict_reg:
                            dict_reg[key] = ((dict_reg[key][0]*dict_reg[key][1]+points)/(dict_reg[key][1]+1),dict_reg[key][1]+1)
                        else:
                            dict_reg[key] = (points,1)
                    elif self.players_count(1,key) > 3 and self.players_count(-1,key) == 3:
                        if listStr[j][0] in self.dict_player_special:
                            dict_player_special[key] = ((dict_player_special[key][0]*dict_player_special[key][1]+points)/(dict_player_special[key][1]+1),dict_player_special[key][1]+1)
                        else:
                            dict_player_special[key] = (points,1)
                    elif self.players_count(1,key) == 3 and self.players_count(-1,key) > 3:
                        if listStr[j][0] in dict_agent_special:
                            dict_agent_special[key] = ((dict_agent_special[key][0]*dict_agent_special[key][1]+points)/(dict_agent_special[key][1]+1),dict_agent_special[key][1]+1)
                        else:
                            dict_agent_special[key] = (points,1)
                    else:
                        if listStr[j][0] in dict_special:
                            dict_special[key] = ((dict_special[key][0]*dict_special[key][1]+points)/(dict_special[key][1]+1),dict_special[key][1]+1)
                        else:
                            dict_special[key] = (points,1)
            self.x.append((my_game.outside_board,my_game.inside_board))
            winner = my_game.check_win()
            the_winner = ""
            if winner == 1:
                self.agentWin+=1
                the_winner = "agent"
            else:
                if winner == -1:
                    self.playerWin += 1
                    the_winner = "player"
                else:
                    self.ties += 1
                    the_winner = "draw"
            self.y.append(the_winner)
        print("the agent won ",self.agentWin," games")
        print("the player won " ,self.playerWin , " games")
        print("there were ", self.ties, " ties")
        np.save('final board', self.x)
        np.save('winner', self.y)
        return dict_init, dict_reg, dict_player_special,dict_agent_special,dict_special


    def games_100000_dumb(self):
        #creates the dictionary while both players play randomly
        for i in range(1000000):
            my_game = Game()
            initiate = True
            my_game.play_one_game()
            listStr = my_game.gamesStr

            for j in range(len(listStr)):
                key = listStr[j][0]
                points = listStr[j][1]
                if j<10:
                    if listStr[j][0] in self.dict_init:
                        self.dict_init[key] = ((self.dict_init[key][0] * self.dict_init[key][1] + points) / (self.dict_init[key][1] + 1),self.dict_init[key][1] + 1)
                    else:
                        self.dict_init[key] = (points, 1)
                else:
                    if self.players_count(1,key) > 3 and self.players_count(-1,key) > 3:
                        if listStr[j][0] in self.dict_reg:
                            self.dict_reg[key] = ((self.dict_reg[key][0]*self.dict_reg[key][1]+points)/(self.dict_reg[key][1]+1),self.dict_reg[key][1]+1)
                        else:
                            self.dict_reg[key] = (points,1)
                    elif self.players_count(1,key) > 3 and self.players_count(-1,key) == 3:
                        if listStr[j][0] in self.dict_player_special:
                            self.dict_player_special[key] = ((self.dict_player_special[key][0]*self.dict_player_special[key][1]+points)/(self.dict_player_special[key][1]+1),self.dict_player_special[key][1]+1)
                        else:
                            self.dict_player_special[key] = (points,1)
                    elif self.players_count(1,key) == 3 and self.players_count(-1,key) > 3:
                        if listStr[j][0] in self.dict_agent_special:
                            self.dict_agent_special[key] = ((self.dict_agent_special[key][0]*self.dict_agent_special[key][1]+points)/(self.dict_agent_special[key][1]+1),self.dict_agent_special[key][1]+1)
                        else:
                            self.dict_agent_special[key] = (points,1)
                    else:
                        if listStr[j][0] in self.dict_special:
                            self.dict_special[key] = ((self.dict_special[key][0]*self.dict_special[key][1]+points)/(self.dict_special[key][1]+1),self.dict_special[key][1]+1)
                        else:
                            self.dict_special[key] = (points,1)
            self.x.append((my_game.outside_board,my_game.inside_board))
            winner = my_game.check_win()
            the_winner = ""
            if winner == 1:
                self.agentWin+=1
                the_winner = "agent"
            else:
                if winner == -1:
                    self.playerWin += 1
                    the_winner = "player"
                else:
                    self.ties += 1
                    the_winner = "draw"
            self.y.append(the_winner)
        print("the agent won ",self.agentWin," games")
        print("the player won " ,self.playerWin , " games")
        print("there were ", self.ties, " ties")
        np.save('final board', self.x)
        np.save('winner', self.y)
        return self.dict_init, self.dict_reg, self.dict_player_special,self.dict_agent_special,self.dict_special


class Game:#class responsible for creating a single full game
    def __init__(self):
        self.outside_board = np.zeros((3, 3), dtype=int) #the outside game board
        self.inside_board = np.zeros((3, 3), dtype=int)  # the inside game board
        self.games = list() #the list that saves every board throughout a game
        self.gamma = 0.9 #the multiplier for the point system
        self.draw = 50 #points if there is a draw
        self.win = 100 #points if the agent wins
        self.loss = 0 #points if the agent loses
        self.gamesStr = list() #a list that contains all the boards throughout the game as well as the points of every board

    def check_three(self, outside_board, inside_board, player, board, row, col):
        #checks wether or not there is a new three created for a certain player
        if board == 0:
            if self.between_boards(row,col) == True:
                if row == 1:
                    if outside_board[row][col] == player and outside_board[row+1][col] == player and outside_board[row-1][col] == player:
                        return True
                elif row == 2 or row == 0:
                    if outside_board[row][col] == player and outside_board[row][col+1] == player and outside_board[row][col-1] == player:
                        return True
            else:
                if row == 0 and col == 0:
                    if outside_board[0][0] == player and outside_board[1][0] == player and outside_board[2][0] == player:
                        return True
                    elif outside_board[0][0] == player and outside_board[0][1] == player and outside_board[0][2] == player:
                        return True
                elif row == 0 and col == 2:
                    if outside_board[0][2] == player and outside_board[1][2] == player and outside_board[2][2] == player:
                        return True
                    elif outside_board[0][2] == player and outside_board[0][1] == player and outside_board[0][0] == player:
                        return True
                elif row == 2 and col == 2:
                    if outside_board[2][2] == player and outside_board[1][2] == player and outside_board[0][2] == player:
                        return True
                    elif outside_board[2][2] == player and outside_board[2][1] == player and outside_board[2][0] == player:
                        return True
                else:
                    if outside_board[2][0] == player and outside_board[1][0] == player and outside_board[0][0] == player:
                        return True
                    elif outside_board[2][0] == player and outside_board[2][1] == player and outside_board[2][2] == player:
                        return True
        else:
            if self.between_boards(row,col) == True:
                if row == 1:
                    if inside_board[row][col] == player and inside_board[row+1][col] == player and inside_board[row-1][col] == player:
                        return True
                elif row == 2 or row == 0:
                    if inside_board[row][col] == player and inside_board[row][col+1] == player and inside_board[row][col-1] == player:
                        return True
            else:
                if row == 0 and col == 0:
                    if inside_board[0][0] == player and inside_board[1][0] == player and inside_board[2][0] == player:
                        return True
                    elif inside_board[0][0] == player and inside_board[0][1] == player and inside_board[0][2] == player:
                        return True
                elif row == 0 and col == 2:
                    if inside_board[0][2] == player and inside_board[1][2] == player and inside_board[2][2] == player:
                        return True
                    elif inside_board[0][2] == player and inside_board[0][1] == player and inside_board[0][0] == player:
                        return True
                elif row == 2 and col == 2:
                    if inside_board[2][2] == player and inside_board[1][2] == player and inside_board[0][2] == player:
                        return True
                    elif inside_board[2][2] == player and inside_board[2][1] == player and inside_board[2][0] == player:
                        return True
                else:
                    if inside_board[2][0] == player and inside_board[1][0] == player and inside_board[0][0] == player:
                        return True
                    elif inside_board[2][0] == player and inside_board[2][1] == player and inside_board[2][2] == player:
                        return True

        return False

    def found_three(self, outside_board, inside_board, player):
        #checks wether or not there is a three in the board for a certain player
        if outside_board[0][0] == player and outside_board[0][1] == player and outside_board[0][2] == player:
            return True
        if outside_board[0][0] == player and outside_board[1][0] == player and outside_board[2][0] == player:
            return True
        if outside_board[2][0] == player and outside_board[2][1] == player and outside_board[2][2] == player:
            return True
        if outside_board[0][2] == player and outside_board[1][2] == player and outside_board[2][2] == player:
            return True
        if inside_board[0][0] == player and inside_board[0][1] == player and inside_board[0][2] == player:
            return True
        if inside_board[0][0] == player and inside_board[1][0] == player and inside_board[2][0] == player:
            return True
        if inside_board[2][0] == player and inside_board[2][1] == player and inside_board[2][2] == player:
            return True
        if inside_board[0][2] == player and inside_board[1][2] == player and inside_board[2][2] == player:
            return True

        return False

    def remove_enemy(self, player):
        #picks a player's soldier randomly and removes it
        players_list = self.list_of_players(self.outside_board, self.inside_board, player)
        three_found = self.found_three(self.outside_board, self.inside_board, player)
        num_soldier = random.randint(0, len(players_list)-1)
        soldier = players_list[num_soldier]
        basic_soldier = soldier
        if three_found:
            if len(players_list) > 3:
                while self.check_three(self.outside_board, self.inside_board, player, soldier[0], soldier[1], soldier[2]) == True and len(players_list) != 0:
                    tuple_to_remove = soldier
                    players_list.remove(tuple_to_remove)
                    if len(players_list) != 0:
                        num_soldier = random.randint(0, len(players_list) - 1)
                        soldier = players_list[num_soldier]
        if len(players_list) == 0:
            soldier = basic_soldier
        if soldier[0] == 0:
            self.outside_board[soldier[1]][soldier[2]] = 0
        else:
            self.inside_board[soldier[1]][soldier[2]] = 0

    def one_person_check_last_stage(self):
        #checks wether or not one of the players has 3 players
        if len(self.list_of_players(self.outside_board, self.inside_board, 1)) == 3:
            return 1
        elif len(self.list_of_players(self.outside_board, self.inside_board, -1)) == 3:
            return -1

        return 0

    def check_last_stage(self):
        #checks wether or not we have arrived to the last stage of the game where both players have 3 soldiers
        if len(self.list_of_players(self.outside_board, self.inside_board,1)) == 3 and len(self.list_of_players(self.outside_board, self.inside_board,-1)) == 3:
            return True

        return False


    def check_win(self):
        #checks and returns 1 if the agent has won, -1 if the player has won and 0 if there is no win
        count_1 = 0
        count_2= 0
        for n in range(3):
            for j in range(3):
                if self.outside_board[n][j] == -1:
                    count_2+=1
                elif self.outside_board[n][j] == 1:
                    count_1+=1
        for n in range(3):
            for j in range(3):
                if self.inside_board[n][j] == -1:
                    count_2+=1
                elif self.inside_board[n][j] == 1:
                    count_1+=1

        if count_1==2:
            return -1
        if count_2 == 2:
            return 1

        return 0

    def list_of_players(self, outside_board, inside_board, player):
        #returns a list that contains the placement of every player's soldier
        players_list = list()
        for n in range(3):
            for j in range(3):
                if n != 1 or j != 1:
                    if outside_board[n][j] == player:
                        players_list.append([0, n, j])
        for n in range(3):
            for j in range(3):
                if n!=1 or j!=1:
                    if inside_board[n][j] == player:
                        players_list.append([1, n, j])
        return players_list

    def empty_places_outside(self, outside_board, inside_board):
        #returns a list of every empty place on the outside part of the board
        empty_list = list()
        for n in range(3):
            for j in range(3):
                if n!=1 or j!=1:
                    if outside_board[n][j] == 0:
                        empty_list.append([n,j])
        return empty_list

    def empty_places_inside(self, outside_board, inside_board):
        #returns a list of every empty place on the inside part of the board
        empty_list = list()
        for n in range(3):
            for j in range(3):
                if n!=1 or j!=1:
                    if inside_board[n][j] == 0:
                        empty_list.append([n,j])
        return empty_list

    def between_boards(self, row,col):
        #return true if the given place is in a position to switch boards
        if row == 0 and col == 1:
            return True
        if row == 1 and col == 0:
            return True
        if row == 1 and col == 2:
            return True
        if row == 2 and col == 1:
            return True
        return False

    def can_soldier_move(self,outside_board, inside_board, player):
        #checks wether or not any player's soldiers can move
        agent_soldiers = self.list_of_players(outside_board, inside_board, player)
        for i in range(len(agent_soldiers)):
            soldier = agent_soldiers[i]
            if self.between_boards(soldier[1],soldier[2])==True:
                if self.mid_can_move(outside_board, inside_board, soldier[0], soldier[1], soldier[2]):
                    return True
            else:
                if self.edge_can_move(outside_board, inside_board, soldier[0], soldier[1], soldier[2]):
                    return True
        return False

    def edge_is_valid(self, curr_row, curr_col, row, col):
        #checking wether or not a move for a soldier that was in an edge is valid
        if row == 1 and curr_col == col:
            return True

        if col == 1 and curr_row == row:
            return True

        return False

    def edge_can_move(self, outside_board, inside_board, board, row, col):
        #checking wether or not an edge piece chosen has a valid move to make
        empty_list_outside = self.empty_places_outside(outside_board, inside_board)
        empty_list_inside = self.empty_places_inside(outside_board, inside_board)
        if board == 0:
            for k in range(len(empty_list_outside)):
                if empty_list_outside[k][0] == 1 and empty_list_outside[k][1] == col:
                    return True

                if empty_list_outside[k][1] == 1 and empty_list_outside[k][0] == row:
                    return True

        else:
            for k in range(len(empty_list_inside)):
                if empty_list_inside[k][0] == 1 and empty_list_inside[k][1] == col:
                    return True

                if empty_list_inside[k][1] == 1 and empty_list_inside[k][0] == row:
                    return True

        return False


    def mid_is_valid(self, curr_row, curr_col, row, col):
        #checking wether or not a move for a soldier that was in a middle position is valid
        if curr_row == row and curr_col == col:
            return True
        if curr_row == 0 and curr_row == row:
            if col == 0 or col == 2:
                return True
        elif curr_row == 2 and curr_row == row:
            if col == 0 or col == 2:
                return True

        if curr_col == 0 and curr_col == col:
            if row == 0 or row == 2:
                return True
        elif curr_col == 2 and curr_col == col:
            if row == 0 or row == 2:
                return True
        return False

    def mid_can_move(self, outside_board, inside_board, board, row, col):
        #checking wether or not a middle position piece chosen has a valid move to make
        empty_list_outside = self.empty_places_outside(outside_board, inside_board)
        empty_list_inside = self.empty_places_inside(outside_board, inside_board)
        if board == 0:
            for k in range(len(empty_list_inside)):
                if empty_list_inside[k][0] == row and empty_list_inside[k][1] == col:
                    return True
            for k in range(len(empty_list_outside)):
                if row == 0 and row == empty_list_outside[k][0]:
                    if empty_list_outside[k][1] == 0 or empty_list_outside[k][1] == 2:
                        return True
                elif row == 2 and row == empty_list_outside[k][0]:
                    if empty_list_outside[k][1] == 0 or empty_list_outside[k][1] == 2:
                        return True

                if col == 0 and col == empty_list_outside[k][1]:
                    if empty_list_outside[k][0] == 0 or empty_list_outside[k][0] == 2:
                        return True
                elif col == 2 and col == empty_list_outside[k][1]:
                    if empty_list_outside[k][0] == 0 or empty_list_outside[k][0] == 2:
                        return True
        else:
            for k in range(len(empty_list_outside)):
                if empty_list_outside[k][0] == row and empty_list_outside[k][1] == col:
                    return True
            for k in range(len(empty_list_inside)):
                if row == 0 and row == empty_list_inside[k][0]:
                    if empty_list_inside[k][1] == 0 or empty_list_inside[k][1] == 2:
                        return True
                elif row == 2 and row == empty_list_inside[k][0]:
                    if empty_list_inside[k][1] == 0 or empty_list_inside[k][1] == 2:
                        return True

                if col == 0 and col == empty_list_inside[k][1]:
                    if empty_list_inside[k][0] == 0 or empty_list_inside[k][0] == 2:
                        return True
                elif col == 2 and col == empty_list_inside[k][1]:
                    if empty_list_inside[k][0] == 0 or empty_list_inside[k][0] == 2:
                        return True

        return False

    def all_places_available(self, outside_board, inside_board, board,row,col):
        #returns a list of all the valid moves for a certain soldier in a regular moving ability
        empty_list_outside = self.empty_places_outside(outside_board, inside_board)
        empty_list_inside = self.empty_places_inside(outside_board, inside_board)
        all_places_available = list()
        if self.between_boards(row,col) == True:
            if board == 0:
                for k in range(len(empty_list_inside)):
                    if empty_list_inside[k][0] == row and empty_list_inside[k][1] == col:
                        all_places_available.append((1,empty_list_inside[k][0],empty_list_inside[k][1]))
                for k in range(len(empty_list_outside)):
                    if row == 0 and row == empty_list_outside[k][0]:
                        if empty_list_outside[k][1] == 0 or empty_list_outside[k][1] == 2:
                            all_places_available.append((0,empty_list_outside[k][0],empty_list_outside[k][1]))
                    elif row == 2 and row == empty_list_outside[k][0]:
                        if empty_list_outside[k][1] == 0 or empty_list_outside[k][1] == 2:
                            all_places_available.append((0,empty_list_outside[k][0],empty_list_outside[k][1]))
                    if col == 0 and col == empty_list_outside[k][1]:
                        if empty_list_outside[k][0] == 0 or empty_list_outside[k][0] == 2:
                            all_places_available.append((0,empty_list_outside[k][0],empty_list_outside[k][1]))
                    elif col == 2 and col == empty_list_outside[k][1]:
                        if empty_list_outside[k][0] == 0 or empty_list_outside[k][0] == 2:
                            all_places_available.append((0,empty_list_outside[k][0],empty_list_outside[k][1]))
            else:
                for k in range(len(empty_list_outside)):
                    if empty_list_outside[k][0] == row and empty_list_outside[k][1] == col:
                        all_places_available.append((0,empty_list_outside[k][0],empty_list_outside[k][1]))
                for k in range(len(empty_list_inside)):
                    if row == 0 and row == empty_list_inside[k][0]:
                        if empty_list_inside[k][1] == 0 or empty_list_inside[k][1] == 2:
                            all_places_available.append((1,empty_list_inside[k][0],empty_list_inside[k][1]))
                    elif row == 2 and row == empty_list_inside[k][0]:
                        if empty_list_inside[k][1] == 0 or empty_list_inside[k][1] == 2:
                            all_places_available.append((1,empty_list_inside[k][0],empty_list_inside[k][1]))
                    if col == 0 and col == empty_list_inside[k][1]:
                        if empty_list_inside[k][0] == 0 or empty_list_inside[k][0] == 2:
                            all_places_available.append((1,empty_list_inside[k][0],empty_list_inside[k][1]))
                    elif col == 2 and col == empty_list_inside[k][1]:
                        if empty_list_inside[k][0] == 0 or empty_list_inside[k][0] == 2:
                            all_places_available.append((1,empty_list_inside[k][0],empty_list_inside[k][1]))
        else:
            if board == 0:
                for k in range(len(empty_list_outside)):
                    if empty_list_outside[k][0] == 1 and empty_list_outside[k][1] == col:
                        all_places_available.append((0,empty_list_outside[k][0],empty_list_outside[k][1]))

                    if empty_list_outside[k][1] == 1 and empty_list_outside[k][0] == row:
                        all_places_available.append((0,empty_list_outside[k][0],empty_list_outside[k][1]))

            else:
                for k in range(len(empty_list_inside)):
                    if empty_list_inside[k][0] == 1 and empty_list_inside[k][1] == col:
                        all_places_available.append((1,empty_list_inside[k][0],empty_list_inside[k][1]))

                    if empty_list_inside[k][1] == 1 and empty_list_inside[k][0] == row:
                        all_places_available.append((1,empty_list_inside[k][0],empty_list_inside[k][1]))

        return all_places_available

    def amount_of_moves_found_init(self, dict1, dict2):
        #returns the amount of next moves found in the dictionary and the amount of moves that aren't found for the initialization part of the game
        empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
        empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
        count_smart = 0
        count_dumb = 0
        player_list = self.list_of_players(self.outside_board, self.inside_board,1)
        outside_board_next = self.outside_board.copy()
        inside_board_next = self.inside_board.copy()
        for j in range(len(empty_list_outside)):
            next_row = empty_list_outside[j][0]
            next_col = empty_list_outside[j][1]
            outside_board_next[next_row][next_col] = 1
            board_str = self.change_to_string2(outside_board_next, inside_board_next)
            if self.check_three(outside_board_next, inside_board_next,1, 0, next_row, next_col) == True:
                opposing_player_list = self.list_of_players(outside_board_next, inside_board_next, -1)
                for k in range(len(opposing_player_list)):
                    if opposing_player_list[k][0] == 0:
                        outside_board_next[opposing_player_list[k][1]][opposing_player_list[k][2]] = 0
                    else:
                        inside_board_next[opposing_player_list[k][1]][opposing_player_list[k][2]] = 0
                    board_str = self.change_to_string2(outside_board_next, inside_board_next)
                    if board_str in dict1 or board_str in dict2:
                        count_smart += 1
                    else:
                        count_dumb += 1
                    outside_board_next = self.outside_board.copy()
                    inside_board_next = self.inside_board.copy()
            else:
                if board_str in dict1 or board_str in dict2:
                    count_smart += 1
                else:
                    count_dumb += 1
            outside_board_next = self.outside_board.copy()
            inside_board_next = self.inside_board.copy()
        for j in range(len(empty_list_inside)):
            next_row = empty_list_inside[j][0]
            next_col = empty_list_inside[j][1]
            inside_board_next[next_row][next_col] = 1
            board_str = self.change_to_string2(outside_board_next, inside_board_next)
            if self.check_three(outside_board_next, inside_board_next,1, 1, next_row, next_col) == True:
                opposing_player_list = self.list_of_players(outside_board_next, inside_board_next, -1)
                for k in range(len(opposing_player_list)):
                    if opposing_player_list[k][0] == 0:
                        outside_board_next[opposing_player_list[k][1]][opposing_player_list[k][2]] = 0
                    else:
                        inside_board_next[opposing_player_list[k][1]][opposing_player_list[k][2]] = 0
                    board_str = self.change_to_string2(outside_board_next, inside_board_next)
                    if board_str in dict1 or board_str in dict2:
                        count_smart += 1
                    else:
                        count_dumb += 1
                    outside_board_next = self.outside_board.copy()
                    inside_board_next = self.inside_board.copy()
            else:
                if board_str in dict1 or board_str in dict2:
                    count_smart += 1
                else:
                    count_dumb += 1
            outside_board_next = self.outside_board.copy()
            inside_board_next = self.inside_board.copy()

        return count_smart, count_dumb

    def amount_of_moves_found_reg(self, dict1, dict2):
        #returns the amount of next moves found in the dictionary and the amount of moves that aren't found for the regular part of the game
        empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
        empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
        count_smart = 0
        count_dumb = 0
        player_list = self.list_of_players(self.outside_board, self.inside_board, 1)
        for i in range(len(player_list)):
            board = player_list[i][0]
            row = player_list[i][1]
            col = player_list[i][2]
            all_places_available = self.all_places_available(self.outside_board, self.inside_board, board,row,col)
            for j in range(len(all_places_available)):
                outside_board_next = self.outside_board.copy()
                inside_board_next = self.inside_board.copy()
                if board == 0:
                    outside_board_next[row][col] = 0
                else:
                    inside_board_next[row][col] = 0
                if all_places_available[j][0] == 1:
                    inside_board_next[all_places_available[j][1]][all_places_available[j][2]] = 1
                else:
                    outside_board_next[all_places_available[j][1]][all_places_available[j][2]] = 1
                board_str = self.change_to_string2(outside_board_next, inside_board_next)
                if self.check_three(outside_board_next, inside_board_next,1, all_places_available[j][0], all_places_available[j][1], all_places_available[j][2]) == True:
                    opposing_player_list = self.list_of_players(outside_board_next, inside_board_next, -1)
                    for k in range(len(opposing_player_list)):
                        if opposing_player_list[k][0] == 0:
                            outside_board_next[opposing_player_list[k][1]][opposing_player_list[k][2]] = 0
                        else:
                            inside_board_next[opposing_player_list[k][1]][opposing_player_list[k][2]] = 0
                        board_str = self.change_to_string2(outside_board_next, inside_board_next)
                        if board_str in dict1 or board_str in dict2:
                            count_smart += 1
                        else:
                            count_dumb += 1
                        outside_board_next = self.outside_board.copy()
                        inside_board_next = self.inside_board.copy()
                else:
                    if board_str in dict1 or board_str in dict2:
                        count_smart += 1
                    else:
                        count_dumb += 1
        return count_smart, count_dumb


    def amount_of_moves_found_special(self, dict1, dict2):
        #returns the amount of next moves found in the dictionary and the amount of moves that aren't found for the special part of the game
        empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
        empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
        count_smart = 0
        count_dumb = 0
        player_list = self.list_of_players(self.outside_board, self.inside_board, 1)
        for i in range(len(player_list)):
            board = player_list[i][0]
            row = player_list[i][1]
            col = player_list[i][2]

            for j in range(len(empty_list_outside)):
                outside_board_current = self.outside_board.copy()
                inside_board_current = self.inside_board.copy()
                if board == 0:
                    outside_board_current[row][col] = 0
                else:
                    inside_board_current[row][col] = 0
                next_row = empty_list_outside[j][0]
                next_col = empty_list_outside[j][1]
                outside_board_current[next_row][next_col] = 1
                board_str = self.change_to_string2(outside_board_current, inside_board_current)
                if self.check_three(outside_board_current, inside_board_current, 1, 0, next_row, next_col) == True:
                    opposing_player_list = self.list_of_players(outside_board_current, inside_board_current, -1)
                    outside_board_next = outside_board_current
                    inside_board_next = inside_board_current
                    for k in range(len(opposing_player_list)):
                        if opposing_player_list[k][0] == 0:
                            outside_board_next[opposing_player_list[k][1]][opposing_player_list[k][2]] = 0
                        else:
                            inside_board_next[opposing_player_list[k][1]][opposing_player_list[k][2]] = 0
                        board_str = self.change_to_string2(outside_board_next, inside_board_next)
                        if board_str in dict1 or board_str in dict2:
                            count_smart += 1
                        else:
                            count_dumb += 1
                        outside_board_next = outside_board_current
                        inside_board_next = inside_board_current
                else:
                    if board_str in dict1 or board_str in dict2:
                        count_smart += 1
                    else:
                        count_dumb += 1
            for j in range(len(empty_list_inside)):
                outside_board_current = self.outside_board.copy()
                inside_board_current = self.inside_board.copy()
                if board == 0:
                    outside_board_current[row][col] = 0
                else:
                    inside_board_current[row][col] = 0
                next_row = empty_list_inside[j][0]
                next_col = empty_list_inside[j][1]
                inside_board_current[next_row][next_col] = 1
                board_str = self.change_to_string2(outside_board_current, inside_board_current)
                if self.check_three(outside_board_current, inside_board_current, 1, 1, next_row, next_col) == True:
                    opposing_player_list = self.list_of_players(outside_board_current, inside_board_current, -1)
                    outside_board_next = outside_board_current
                    inside_board_next = inside_board_current
                    for k in range(len(opposing_player_list)):
                        if opposing_player_list[k][0] == 0:
                            outside_board_next[opposing_player_list[k][1]][opposing_player_list[k][2]] = 0
                        else:
                            inside_board_next[opposing_player_list[k][1]][opposing_player_list[k][2]] = 0
                        board_str = self.change_to_string2(outside_board_next, inside_board_next)
                        if board_str in dict1 or board_str in dict2:
                            count_smart += 1
                        else:
                            count_dumb += 1
                        outside_board_next = outside_board_current
                        inside_board_next = inside_board_current
                else:
                    if board_str in dict1 or board_str in dict2:
                        count_smart += 1
                    else:
                        count_dumb += 1

        return count_smart, count_dumb





    def smart_a_remove(self, dict1, dict2, str1):
        #checks the dictionary for the best player's soldier to remove
        best_take = str1
        current_score = -1
        best_score = -1
        take = list(str1)

        for i in range(len(take)):
            if take[i] == 'o':
                take[i] = '-'
                new_take = ''.join(take)

                if new_take in dict1:
                    current_score = dict1[new_take][0]

                if new_take in dict2:
                    current_score = dict2[new_take][0]

                if current_score > best_score:
                    best_score = current_score
                    best_take = new_take



                take[i] = 'o'
        return best_take



    def smart_a_init(self,outside_board, inside_board, dict_init):
        #check the dictionary for the best placement of the agent's soldier in the initialization part of the game
        player_list = self.list_of_players(outside_board, inside_board, 1)
        best_score = -1
        best_board = '----------------'
        current_score = -1
        board = -1
        best_row = -1
        best_col = -1
        empty_places_outside = self.empty_places_outside(outside_board, inside_board)
        empty_places_inside = self.empty_places_inside(outside_board, inside_board)
        count_smart, count_dumb = self.amount_of_moves_found_init(dict_init, dict_init)
        if count_smart>count_dumb:
            for i in range(len(empty_places_outside)):
                outside_board_next = outside_board.copy()
                inside_board_next = inside_board.copy()
                row = empty_places_outside[i][0]
                col = empty_places_outside[i][1]
                outside_board_next[row][col] = 1
                board_str = self.change_to_string2(outside_board_next, inside_board_next)
                if self.check_three(outside_board_next, inside_board_next,1, 0, row, col) == True:
                    str_after_take = self.smart_a_remove(dict_init, dict_init, board_str)
                    board_str = str_after_take
                    board = 0
                    best_row = row
                    best_col = col
                    best_board = board_str
                    outside_board_best, inside_board_best = self.change_from_string(best_board)
                    self.outside_board = outside_board_best.copy()
                    self.inside_board = inside_board_best.copy()
                    soldier = [board, best_row, best_col]
                    return soldier
                if board_str in dict_init:
                    current_score = dict_init[board_str][0]
                if current_score > best_score:
                    board = 0
                    best_row = row
                    best_col = col
                    best_board = board_str
                    best_score = current_score
            for i in range(len(empty_places_inside)):
                outside_board_next = outside_board.copy()
                inside_board_next = inside_board.copy()
                row = empty_places_inside[i][0]
                col = empty_places_inside[i][1]
                inside_board_next[row][col] = 1
                board_str = self.change_to_string2(outside_board_next, inside_board_next)
                if self.check_three(outside_board_next, inside_board_next,1, 1, row, col) == True:
                    str_after_take = self.smart_a_remove(dict_init, dict_init, board_str)
                    board_str = str_after_take
                    board = 1
                    best_row = row
                    best_col = col
                    best_board = board_str
                    outside_board_best, inside_board_best = self.change_from_string(best_board)
                    self.outside_board = outside_board_best.copy()
                    self.inside_board = inside_board_best.copy()
                    soldier = [board, best_row, best_col]
                    return soldier

                if board_str in dict_init:
                    current_score = dict_init[board_str][0]
                if current_score > best_score:
                    board = 1
                    best_row = row
                    best_col = col
                    best_board = board_str
                    best_score = current_score

        if board != -1:
            outside_board_best, inside_board_best = self.change_from_string(best_board)
            self.outside_board = outside_board_best.copy()
            self.inside_board = inside_board_best.copy()

        soldier = [board, best_row, best_col]
        return soldier

    def smart_a_reg(self,outside_board, inside_board, dict_reg, dict1):
        #check the dictionary for the best placement of the agent's soldier in the regular part of the game
        player_list = self.list_of_players(outside_board, inside_board, 1)
        best_score = -1
        best_board = '----------------'
        current_score = -1
        this_board = -1
        best_row = -1
        best_col = -1
        board_next = -1
        row_next = -1
        col_next = -1
        count_smart, count_dumb = self.amount_of_moves_found_reg(dict_reg, dict1)
        if count_smart > count_dumb:
            for i in range(len(player_list)):
                board = player_list[i][0]
                row = player_list[i][1]
                col = player_list[i][2]
                all_places_available = self.all_places_available(outside_board, inside_board, board,row,col)
                for j in range(len(all_places_available)):
                    outside_board_next = outside_board.copy()
                    inside_board_next = inside_board.copy()
                    if board == 0:
                        outside_board_next[row][col] = 0
                    else:
                        inside_board_next[row][col] = 0
                    if all_places_available[j][0] == 1:
                        inside_board_next[all_places_available[j][1]][all_places_available[j][2]] = 1
                    else:
                        outside_board_next[all_places_available[j][1]][all_places_available[j][2]] = 1
                    board_next = all_places_available[j][0]
                    row_next = all_places_available[j][1]
                    col_next = all_places_available[j][2]
                    board_str = self.change_to_string2(outside_board_next,inside_board_next)
                    if self.check_three(outside_board_next,inside_board_next,1 , board_next, row_next, col_next) == True:
                        str_after_take = self.smart_a_remove(dict_reg, dict1, board_str)
                        board_str = str_after_take
                        best_board = board_str
                        outside_board_best, inside_board_best = self.change_from_string(best_board)
                        self.outside_board = outside_board_best.copy()
                        self.inside_board = inside_board_best.copy()
                        soldier = [board_next, row_next, col_next]
                        return soldier
                    if board_str in dict_reg:
                        current_score = dict_reg[board_str][0]
                    elif board_str in dict1:
                        current_score = dict1[board_str][0]
                    if current_score>best_score:
                        this_board = board_next
                        best_row = row_next
                        best_col = col_next
                        best_board = board_str
                        best_score = current_score
        if this_board != -1:
            outside_board_best, inside_board_best = self.change_from_string(best_board)
            self.outside_board = outside_board_best.copy()
            self.inside_board = inside_board_best.copy()

        soldier = [this_board, best_row, best_col]
        return soldier


    def smart_a_special(self,outside_board, inside_board,  dict_special, dict1):
        #check the dictionary for the best placement of the agent's soldier in the special part of the game
        player_list = self.list_of_players(outside_board, inside_board, 1)
        empty_places_outside = self.empty_places_outside(outside_board, inside_board)
        empty_places_inside = self.empty_places_inside(outside_board, inside_board)
        best_score = -1
        best_board = '----------------'
        current_score = -1
        this_board = -1
        best_row = -1
        best_col = -1
        count_smart, count_dumb = self.amount_of_moves_found_special(dict_special, dict1)
        if count_smart > count_dumb:
            for i in range(len(player_list)):
                board = player_list[i][0]
                row = player_list[i][1]
                col = player_list[i][2]
                outside_board_current = outside_board.copy()
                inside_board_current = inside_board.copy()
                if board == 0:
                    outside_board_current[row][col] = 0
                else:
                    inside_board_current[row][col] = 0
                outside_board_next = outside_board_current.copy()
                inside_board_next = inside_board_current.copy()
                for j in range(len(empty_places_outside)):
                    next_row = empty_places_outside[j][0]
                    next_col = empty_places_outside[j][1]
                    outside_board_next[next_row][next_col] = 1
                    board_str = self.change_to_string2(outside_board_next, inside_board_next)
                    if self.check_three(outside_board_next, inside_board_next, 1, 0, next_row, next_col) == True:
                        str_after_take = self.smart_a_remove(dict_special, dict1, board_str)
                        board_str = str_after_take
                        board = 0
                        best_row = row
                        best_col = col
                        best_board = board_str
                        outside_board_best, inside_board_best = self.change_from_string(best_board)
                        self.outside_board = outside_board_best.copy()
                        self.inside_board = inside_board_best.copy()
                        soldier = [board, best_row, best_col]
                        return soldier


                    if board_str in dict_special:
                        current_score = dict_special[board_str][0]
                    elif board_str in dict1:
                        current_score = dict1[board_str][0]
                    if current_score > best_score:
                        this_board = 0
                        best_row = next_row
                        best_col = next_col
                        best_board = board_str
                        best_score = current_score
                    outside_board_next = outside_board_current.copy()
                    inside_board_next = inside_board_current.copy()
                for j in range(len(empty_places_inside)):
                    outside_board_next = outside_board_current.copy()
                    inside_board_next = inside_board_current.copy()
                    next_row = empty_places_inside[j][0]
                    next_col = empty_places_inside[j][1]
                    inside_board_next[next_row][next_col] = 1
                    board_str = self.change_to_string2(outside_board_next, inside_board_next)
                    if self.check_three(outside_board_next, inside_board_next, 1, 1, next_row, next_col) == True:
                        str_after_take = self.smart_a_remove(dict_special, dict1, board_str)
                        board_str = str_after_take
                        board = 1
                        best_row = row
                        best_col = col
                        best_board = board_str
                        outside_board_best, inside_board_best = self.change_from_string(best_board)
                        self.outside_board = outside_board_best.copy()
                        self.inside_board = inside_board_best.copy()
                        soldier = [board, best_row, best_col]
                        return soldier
                    if board_str in dict_special:
                        current_score = dict_special[board_str][0]
                    elif board_str in dict1:
                        current_score = dict1[board_str][0]
                    if current_score > best_score:
                        this_board = 1
                        best_row = next_row
                        best_col = next_col
                        best_board = board_str
                        best_score = current_score
                    outside_board_next = outside_board_current.copy()
                    inside_board_next = inside_board_current.copy()
        if this_board != -1:
            outside_board_best, inside_board_best = self.change_from_string(best_board)
            self.outside_board = outside_board_best.copy()
            self.inside_board = inside_board_best.copy()

        soldier = [this_board, best_row, best_col]
        return soldier



    def agent_turn_initialize(self):
        #randomly makes a move for the agent's soldier in the initialization part of the game
        empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
        empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
        board = random.randint(0,1)
        if (board == 0 and len(empty_list_outside)!=0) or len(empty_list_inside)==0:
            max_num = random.randint(0,len(empty_list_outside)-1)
            place = empty_list_outside[max_num]
            row = place[0]
            col = place[1]
            self.outside_board[row][col] = 1
        else:
            max_num = random.randint(0, len(empty_list_inside)-1)
            place = empty_list_inside[max_num]
            row = place[0]
            col = place[1]
            self.inside_board[row][col] = 1

        soldier = [board, row, col]
        return soldier

    def agent_turn_regular(self):
        #randomly makes a move for the agent's soldier in the regular part of the game
        agent_soldiers = self.list_of_players(self.outside_board, self.inside_board, 1)
        num_soldier = random.randint(0, len(agent_soldiers) - 1)
        soldier = agent_soldiers[num_soldier]
        valid_soldier = False
        while valid_soldier == False:
            if self.between_boards(soldier[1], soldier[2]) == True:
                if self.mid_can_move(self.outside_board, self.inside_board, soldier[0], soldier[1], soldier[2]) == False:
                    num_soldier = random.randint(0, len(agent_soldiers) - 1)
                    soldier = agent_soldiers[num_soldier]
                else:
                    valid_soldier = True
            else:
                if self.edge_can_move(self.outside_board, self.inside_board, soldier[0], soldier[1], soldier[2]) == False:
                    num_soldier = random.randint(0, len(agent_soldiers) - 1)
                    soldier = agent_soldiers[num_soldier]
                else:
                    valid_soldier = True
        if soldier[0] == 0:
            if self.between_boards(soldier[1], soldier[2]) == False:
                board = 0
                empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
                max_num = random.randint(0, len(empty_list_outside) - 1)
                place = empty_list_outside[max_num]
                row = place[0]
                col = place[1]
                while self.edge_is_valid(soldier[1], soldier[2], row, col) == False:
                    max_num = random.randint(0, len(empty_list_outside) - 1)
                    place = empty_list_outside[max_num]
                    row = place[0]
                    col = place[1]
                self.outside_board[row][col] = 1
                self.outside_board[soldier[1]][soldier[2]] = 0
            else:
                empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
                empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
                if len(empty_list_outside) == 0:
                    self.inside_board[soldier[1]][soldier[2]] = 1
                    self.outside_board[soldier[1]][soldier[2]] = 0
                if [soldier[1], soldier[2]] in empty_list_inside:
                    empty_list_outside.append([soldier[1], soldier[2]])
                max_num = random.randint(0, len(empty_list_outside) - 1)
                place = empty_list_outside[max_num]
                row = place[0]
                col = place[1]
                while self.mid_is_valid(soldier[1], soldier[2], row, col) == False:
                    max_num = random.randint(0, len(empty_list_outside) - 1)
                    place = empty_list_outside[max_num]
                    row = place[0]
                    col = place[1]
                if row == soldier[1] and col == soldier[2]:
                    board = 1
                    self.inside_board[soldier[1]][soldier[2]] = 1
                    self.outside_board[soldier[1]][soldier[2]] = 0
                else:
                    board = 0
                    self.outside_board[row][col] = 1
                    self.outside_board[soldier[1]][soldier[2]] = 0
        else:
            if self.between_boards(soldier[1], soldier[2]) == False:
                board = 1
                empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
                max_num = random.randint(0, len(empty_list_inside) - 1)
                place = empty_list_inside[max_num]
                row = place[0]
                col = place[1]
                while self.edge_is_valid(soldier[1], soldier[2], row, col) == False:
                    max_num = random.randint(0, len(empty_list_inside) - 1)
                    place = empty_list_inside[max_num]
                    row = place[0]
                    col = place[1]
                self.inside_board[row][col] = 1
                self.inside_board[soldier[1]][soldier[2]] = 0
            else:
                empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
                empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
                if len(empty_list_inside) == 0:
                    self.outside_board[soldier[1]][soldier[2]] = 1
                    self.inside_board[soldier[1]][soldier[2]] = 0
                if [soldier[1], soldier[2]] in empty_list_outside:
                    empty_list_inside.append([soldier[1], soldier[2]])
                max_num = random.randint(0, len(empty_list_inside) - 1)
                place = empty_list_inside[max_num]
                row = place[0]
                col = place[1]
                while self.mid_is_valid(soldier[1], soldier[2], row, col) == False:
                    max_num = random.randint(0, len(empty_list_inside) - 1)
                    place = empty_list_inside[max_num]
                    row = place[0]
                    col = place[1]
                if row == soldier[1] and col == soldier[2]:
                    board = 0
                    self.outside_board[soldier[1]][soldier[2]] = 1
                    self.inside_board[soldier[1]][soldier[2]] = 0
                else:
                    board = 1
                    self.inside_board[row][col] = 1
                    self.inside_board[soldier[1]][soldier[2]] = 0
        soldier = [board, row, col]
        return soldier



    def agent_turn_final_phase(self):
        #randomly makes a move for the agent's soldier in the special part of the game
        agent_soldiers = self.list_of_players(self.outside_board, self.inside_board, 1)
        num_soldier = random.randint(0, len(agent_soldiers) - 1)
        soldier = agent_soldiers[num_soldier]
        empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
        empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
        board = random.randint(0, 1)
        if (board == 0 and len(empty_list_outside) != 0) or len(empty_list_inside) == 0:
            max_num = random.randint(0, len(empty_list_outside) - 1)
            place = empty_list_outside[max_num]
            row = place[0]
            col = place[1]
            if soldier[0] == 0:
                self.outside_board[soldier[1], soldier[2]] = 0
            else:
                self.inside_board[soldier[1], soldier[2]] = 0
            self.outside_board[row][col] = 1
        else:
            max_num = random.randint(0, len(empty_list_inside) - 1)
            place = empty_list_inside[max_num]
            row = place[0]
            col = place[1]
            if soldier[0] == 0:
                self.outside_board[soldier[1], soldier[2]] = 0
            else:
                self.inside_board[soldier[1], soldier[2]] = 0
            self.inside_board[row][col] = 1
        soldier = [board, row, col]
        return soldier

    def player_turn_initialize(self):
        #randomly makes a move for the player's soldier in the initialization part of the game
        empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
        empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
        board = random.randint(0,1)
        if (board == 0 and len(empty_list_outside)!=0) or len(empty_list_inside)==0:
            max_num = random.randint(0,len(empty_list_outside)-1)
            place = empty_list_outside[max_num]
            row = place[0]
            col = place[1]
            self.outside_board[row][col] = -1
        else:
            max_num = random.randint(0, len(empty_list_inside)-1)
            place = empty_list_inside[max_num]
            row = place[0]
            col = place[1]
            self.inside_board[row][col] = -1
        soldier = [board, row, col]
        return soldier

    def player_turn_regular(self):
        #randomly makes a move for the player's soldier in the regular part of the game
        agent_soldiers = self.list_of_players(self.outside_board, self.inside_board, -1)
        num_soldier = random.randint(0, len(agent_soldiers) - 1)
        soldier = agent_soldiers[num_soldier]
        valid_soldier = False
        while valid_soldier == False:
            if self.between_boards(soldier[1], soldier[2]) == True:
                if self.mid_can_move(self.outside_board, self.inside_board, soldier[0], soldier[1], soldier[2]) == False:
                    num_soldier = random.randint(0, len(agent_soldiers) - 1)
                    soldier = agent_soldiers[num_soldier]
                else:
                    valid_soldier = True
            else:
                if self.edge_can_move(self.outside_board, self.inside_board, soldier[0], soldier[1], soldier[2]) == False:
                    num_soldier = random.randint(0, len(agent_soldiers) - 1)
                    soldier = agent_soldiers[num_soldier]
                else:
                    valid_soldier = True
        if soldier[0] == 0:
            if self.between_boards(soldier[1], soldier[2]) == False:
                board = 0
                empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
                max_num = random.randint(0, len(empty_list_outside) - 1)
                place = empty_list_outside[max_num]
                row = place[0]
                col = place[1]
                while self.edge_is_valid(soldier[1], soldier[2], row, col) == False:
                    max_num = random.randint(0, len(empty_list_outside) - 1)
                    place = empty_list_outside[max_num]
                    row = place[0]
                    col = place[1]
                self.outside_board[row][col] = -1
                self.outside_board[soldier[1]][soldier[2]] = 0
            else:
                empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
                empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
                if len(empty_list_outside) == 0:
                    self.inside_board[soldier[1]][soldier[2]] = -1
                    self.outside_board[soldier[1]][soldier[2]] = 0
                if [soldier[1], soldier[2]] in empty_list_inside:
                    empty_list_outside.append([soldier[1], soldier[2]])
                max_num = random.randint(0, len(empty_list_outside) - 1)
                place = empty_list_outside[max_num]
                row = place[0]
                col = place[1]
                while self.mid_is_valid(soldier[1], soldier[2], row, col) == False:
                    max_num = random.randint(0, len(empty_list_outside) - 1)
                    place = empty_list_outside[max_num]
                    row = place[0]
                    col = place[1]
                if row == soldier[1] and col == soldier[2]:
                    board = 1
                    self.inside_board[soldier[1]][soldier[2]] = -1
                    self.outside_board[soldier[1]][soldier[2]] = 0
                else:
                    board = 0
                    self.outside_board[row][col] = -1
                    self.outside_board[soldier[1]][soldier[2]] = 0
        else:
            if self.between_boards(soldier[1], soldier[2]) == False:
                board = 1
                empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
                max_num = random.randint(0, len(empty_list_inside) - 1)
                place = empty_list_inside[max_num]
                row = place[0]
                col = place[1]
                while self.edge_is_valid(soldier[1], soldier[2], row, col) == False:
                    max_num = random.randint(0, len(empty_list_inside) - 1)
                    place = empty_list_inside[max_num]
                    row = place[0]
                    col = place[1]
                self.inside_board[row][col] = -1
                self.inside_board[soldier[1]][soldier[2]] = 0
            else:
                empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
                empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
                if len(empty_list_inside) == 0:
                    self.outside_board[soldier[1]][soldier[2]] = -1
                    self.inside_board[soldier[1]][soldier[2]] = 0
                if [soldier[1], soldier[2]] in empty_list_outside:
                    empty_list_inside.append([soldier[1], soldier[2]])
                max_num = random.randint(0, len(empty_list_inside) - 1)
                place = empty_list_inside[max_num]
                row = place[0]
                col = place[1]
                while self.mid_is_valid(soldier[1], soldier[2], row, col) == False:
                    max_num = random.randint(0, len(empty_list_inside) - 1)
                    place = empty_list_inside[max_num]
                    row = place[0]
                    col = place[1]
                if row == soldier[1] and col == soldier[2]:
                    board = 0
                    self.outside_board[soldier[1]][soldier[2]] = -1
                    self.inside_board[soldier[1]][soldier[2]] = 0
                else:
                    board = 1
                    self.inside_board[row][col] = -1
                    self.inside_board[soldier[1]][soldier[2]] = 0
        soldier = [board, row, col]
        return soldier


    def player_turn_final_phase(self):
        #randomly makes a move for the player's soldier in the special part of the game
        player_soldiers = self.list_of_players(self.outside_board, self.inside_board, -1)
        num_soldier = random.randint(0, len(player_soldiers) - 1)
        soldier = player_soldiers[num_soldier]
        empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
        empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
        board = random.randint(0, 1)
        if (board == 0 and len(empty_list_outside) != 0) or len(empty_list_inside) == 0:
            max_num = random.randint(0, len(empty_list_outside) - 1)
            place = empty_list_outside[max_num]
            row = place[0]
            col = place[1]
            if soldier[0] == 0:
                self.outside_board[soldier[1], soldier[2]] = 0
            else:
                self.inside_board[soldier[1], soldier[2]] = 0
            self.outside_board[row][col] = -1
        else:
            max_num = random.randint(0, len(empty_list_inside) - 1)
            place = empty_list_inside[max_num]
            row = place[0]
            col = place[1]
            if soldier[0] == 0:
                self.outside_board[soldier[1], soldier[2]] = 0
            else:
                self.inside_board[soldier[1], soldier[2]] = 0
            self.inside_board[row][col] = -1
        soldier = [board, row, col]
        return soldier

    def three_creations_list_of_places(self):
        #returns a list of places where if we put a player's soldier there will be a three
        list_of_threes = list()
        empty_places_outside = self.empty_places_outside(self.outside_board, self.inside_board)
        empty_places_inside = self.empty_places_inside(self.outside_board, self.inside_board)
        for i in range(len(empty_places_outside)):
            outside_board_next = self.outside_board.copy()
            inside_board_next = self.inside_board.copy()
            row = empty_places_outside[i][0]
            col = empty_places_outside[i][1]
            outside_board_next[row][col] = -1
            board_str = self.change_to_string2(outside_board_next, inside_board_next)
            if self.check_three(outside_board_next, inside_board_next, -1, 0, row, col) == True:
                list_of_threes.append([0,row,col])
        for i in range(len(empty_places_inside)):
            outside_board_next = self.outside_board.copy()
            inside_board_next = self.inside_board.copy()
            row = empty_places_inside[i][0]
            col = empty_places_inside[i][1]
            inside_board_next[row][col] = -1
            board_str = self.change_to_string2(outside_board_next, inside_board_next)
            if self.check_three(outside_board_next, inside_board_next, -1, 1, row, col) == True:
                list_of_threes.append([1,row,col])

        return list_of_threes

    def still_creates_three(self, outside_board, inside_board, board1, row1, col1, board, row, col):
        #returns wether or not a certain move made will make a three
        if board1 == 0:
            outside_board[row1][col1] = 0
            if board == 0:
                outside_board[row][col] = -1
            else:
                inside_board[row][col] = -1
        else:
            inside_board[row1][col1] = 0
            if board == 0:
                outside_board[row][col] = -1
            else:
                inside_board[row][col] = -1

        return self.check_three(outside_board, inside_board, -1, board, row, col)

    def player_turn_initialize_smart(self):
        #places a player's soldier randomly unless there is an available three to create, in that case, it creates it
        list_of_threes = self.three_creations_list_of_places()
        if len(list_of_threes)>0:
            three = list_of_threes[0]
            if three[0] == 0:
                self.outside_board[three[1]][three[2]] = -1
            else:
                self.inside_board[three[1]][three[2]] = -1
            return three
        else:
            empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
            empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
            board = random.randint(0,1)
            if (board == 0 and len(empty_list_outside)!=0) or len(empty_list_inside)==0:
                max_num = random.randint(0,len(empty_list_outside)-1)
                place = empty_list_outside[max_num]
                row = place[0]
                col = place[1]
                self.outside_board[row][col] = -1
            else:
                max_num = random.randint(0, len(empty_list_inside)-1)
                place = empty_list_inside[max_num]
                row = place[0]
                col = place[1]
                self.inside_board[row][col] = -1
            soldier = [board, row, col]
            return soldier

    def player_turn_regular_smart(self):
        #moves a player's soldier randomly unless there is an available three to create, in that case, it creates it in the regular part of the game
        list_of_threes = self.three_creations_list_of_places()
        agent_soldiers = self.list_of_players(self.outside_board, self.inside_board, -1)
        found_three = False
        if len(list_of_threes) > 0:
            for i in range(len(list_of_threes)):
                three = list_of_threes[i]
                for j in range(len(agent_soldiers)):
                    soldier = agent_soldiers[j]
                    all_places_available = self.all_places_available(self.outside_board,self.inside_board, soldier[0], soldier[1], soldier[2])
                    for k in range(len(all_places_available)):
                        place = all_places_available[k]
                        if three[0] == place[0] and three[1] == place[1] and three[2] == place[2]:
                            outside_board = self.outside_board.copy()
                            inside_board = self.inside_board.copy()
                            if self.still_creates_three(outside_board, inside_board, soldier[0], soldier[1], soldier[2], three[0], three[1], three[2]):
                                if soldier[0] == 0:
                                    self.outside_board[soldier[1]][soldier[2]] = 0
                                else:
                                    self.inside_board[soldier[1]][soldier[2]] = 0
                                if three[0] == 0:
                                    self.outside_board[three[1]][three[2]] = -1
                                else:
                                    self.inside_board[three[1]][three[2]] = -1
                                return three
        num_soldier = random.randint(0, len(agent_soldiers) - 1)
        soldier = agent_soldiers[num_soldier]
        valid_soldier = False
        while valid_soldier == False:
            if self.between_boards(soldier[1], soldier[2]) == True:
                if self.mid_can_move(self.outside_board, self.inside_board, soldier[0], soldier[1], soldier[2]) == False:
                    num_soldier = random.randint(0, len(agent_soldiers) - 1)
                    soldier = agent_soldiers[num_soldier]
                else:
                    valid_soldier = True
            else:
                if self.edge_can_move(self.outside_board, self.inside_board, soldier[0], soldier[1], soldier[2]) == False:
                    num_soldier = random.randint(0, len(agent_soldiers) - 1)
                    soldier = agent_soldiers[num_soldier]
                else:
                    valid_soldier = True
        if soldier[0] == 0:
            if self.between_boards(soldier[1], soldier[2]) == False:
                board = 0
                empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
                max_num = random.randint(0, len(empty_list_outside) - 1)
                place = empty_list_outside[max_num]
                row = place[0]
                col = place[1]
                while self.edge_is_valid(soldier[1], soldier[2], row, col) == False:
                    max_num = random.randint(0, len(empty_list_outside) - 1)
                    place = empty_list_outside[max_num]
                    row = place[0]
                    col = place[1]
                self.outside_board[row][col] = -1
                self.outside_board[soldier[1]][soldier[2]] = 0
            else:
                empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
                empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
                if len(empty_list_outside) == 0:
                    self.inside_board[soldier[1]][soldier[2]] = -1
                    self.outside_board[soldier[1]][soldier[2]] = 0
                if [soldier[1], soldier[2]] in empty_list_inside:
                    empty_list_outside.append([soldier[1], soldier[2]])
                max_num = random.randint(0, len(empty_list_outside) - 1)
                place = empty_list_outside[max_num]
                row = place[0]
                col = place[1]
                while self.mid_is_valid(soldier[1], soldier[2], row, col) == False:
                    max_num = random.randint(0, len(empty_list_outside) - 1)
                    place = empty_list_outside[max_num]
                    row = place[0]
                    col = place[1]
                if row == soldier[1] and col == soldier[2]:
                    board = 1
                    self.inside_board[soldier[1]][soldier[2]] = -1
                    self.outside_board[soldier[1]][soldier[2]] = 0
                else:
                    board = 0
                    self.outside_board[row][col] = -1
                    self.outside_board[soldier[1]][soldier[2]] = 0
        else:
            if self.between_boards(soldier[1], soldier[2]) == False:
                board = 1
                empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
                max_num = random.randint(0, len(empty_list_inside) - 1)
                place = empty_list_inside[max_num]
                row = place[0]
                col = place[1]
                while self.edge_is_valid(soldier[1], soldier[2], row, col) == False:
                    max_num = random.randint(0, len(empty_list_inside) - 1)
                    place = empty_list_inside[max_num]
                    row = place[0]
                    col = place[1]
                self.inside_board[row][col] = -1
                self.inside_board[soldier[1]][soldier[2]] = 0
            else:
                empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
                empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
                if len(empty_list_inside) == 0:
                    self.outside_board[soldier[1]][soldier[2]] = -1
                    self.inside_board[soldier[1]][soldier[2]] = 0
                if [soldier[1], soldier[2]] in empty_list_outside:
                    empty_list_inside.append([soldier[1], soldier[2]])
                max_num = random.randint(0, len(empty_list_inside) - 1)
                place = empty_list_inside[max_num]
                row = place[0]
                col = place[1]
                while self.mid_is_valid(soldier[1], soldier[2], row, col) == False:
                    max_num = random.randint(0, len(empty_list_inside) - 1)
                    place = empty_list_inside[max_num]
                    row = place[0]
                    col = place[1]
                if row == soldier[1] and col == soldier[2]:
                    board = 0
                    self.outside_board[soldier[1]][soldier[2]] = -1
                    self.inside_board[soldier[1]][soldier[2]] = 0
                else:
                    board = 1
                    self.inside_board[row][col] = -1
                    self.inside_board[soldier[1]][soldier[2]] = 0
        soldier = [board, row, col]
        return soldier


    def player_turn_final_phase_smart(self):
        #moves a player's soldier randomly unless there is an available three to create, in that case, it creates it in the special part of the game
        list_of_threes = self.three_creations_list_of_places()
        player_soldiers = self.list_of_players(self.outside_board, self.inside_board, -1)
        empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
        empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
        found_three = False
        if len(list_of_threes) > 0:
            for i in range(len(empty_list_outside)):
                empty_place = empty_list_outside[i]
                place = [0, empty_place[0], empty_place[1]]
                for k in range(len(list_of_threes)):
                    three = list_of_threes[k]
                    for j in range(len(player_soldiers)):
                        soldier = player_soldiers[j]
                        if three[0] == place[0] and three[1] == place[1] and three[2] == place[2]:
                            outside_board = self.outside_board.copy()
                            inside_board = self.inside_board.copy()
                            if self.still_creates_three(outside_board, inside_board, soldier[0], soldier[1], soldier[2], three[0], three[1], three[2]):
                                if soldier[0] == 0:
                                    self.outside_board[soldier[1]][soldier[2]] = 0
                                else:
                                    self.inside_board[soldier[1]][soldier[2]] = 0
                                if three[0] == 0:
                                    self.outside_board[three[1]][three[2]] = -1
                                else:
                                    self.inside_board[three[1]][three[2]] = -1
                                return three
            for i in range(len(empty_list_inside)):
                empty_place = empty_list_inside[i]
                place = [1, empty_place[0], empty_place[1]]
                for k in range(len(list_of_threes)):
                    three = list_of_threes[k]
                    for j in range(len(player_soldiers)):
                        soldier = player_soldiers[j]
                        if three[0] == place[0] and three[1] == place[1] and three[2] == place[2]:
                            outside_board = self.outside_board.copy()
                            inside_board = self.inside_board.copy()
                            if self.still_creates_three(outside_board, inside_board, soldier[0], soldier[1], soldier[2], three[0], three[1], three[2]):
                                if soldier[0] == 0:
                                    self.outside_board[soldier[1]][soldier[2]] = 0
                                else:
                                    self.inside_board[soldier[1]][soldier[2]] = 0
                                if three[0] == 0:
                                    self.outside_board[three[1]][three[2]] = -1
                                else:
                                    self.inside_board[three[1]][three[2]] = -1
                                return three
        else:
            num_soldier = random.randint(0, len(player_soldiers) - 1)
            soldier = player_soldiers[num_soldier]
            board = random.randint(0, 1)
            if (board == 0 and len(empty_list_outside) != 0) or len(empty_list_inside) == 0:
                max_num = random.randint(0, len(empty_list_outside) - 1)
                place = empty_list_outside[max_num]
                row = place[0]
                col = place[1]
                if soldier[0] == 0:
                    self.outside_board[soldier[1], soldier[2]] = 0
                else:
                    self.inside_board[soldier[1], soldier[2]] = 0
                self.outside_board[row][col] = -1
            else:
                max_num = random.randint(0, len(empty_list_inside) - 1)
                place = empty_list_inside[max_num]
                row = place[0]
                col = place[1]
                if soldier[0] == 0:
                    self.outside_board[soldier[1], soldier[2]] = 0
                else:
                    self.inside_board[soldier[1], soldier[2]] = 0
                self.inside_board[row][col] = -1
            soldier = [board, row, col]
            return soldier

    def reset_boards(self):
        #resets the board to the initial state
        self.outside_board = np.zeros((3, 3), dtype=int)
        self.inside_board = np.zeros((3, 3), dtype=int)

    def play_one_game(self):
        #plays an entire game where both players play randomly
        board_str = "----------------"
        self.games.append(board_str)
        board_str = ""
        for i in range(5):
            soldier = self.agent_turn_initialize()
            if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == False:
                board_str = self.change_to_string()
                self.games.append(board_str)
            else:
                self.remove_enemy(-1)
                board_str = self.change_to_string()
                self.games.append(board_str)
            soldier = self.player_turn_initialize()
            if self.check_three(self.outside_board, self.inside_board, -1, soldier[0], soldier[1], soldier[2])==False:
                board_str = self.change_to_string()
                self.games.append(board_str)
            else:
                self.remove_enemy(1)
                board_str = self.change_to_string()
                self.games.append(board_str)

        while self.one_person_check_last_stage() == 0:
            if self.can_soldier_move(self.outside_board, self.inside_board, 1) == False:
                self.points()
                return -1
            soldier = self.agent_turn_regular()
            if self.check_three(self.outside_board, self.inside_board, 1, soldier[0], soldier[1], soldier[2]) == False:
                board_str = self.change_to_string()
                self.games.append(board_str)
            else:
                self.remove_enemy(-1)
                board_str = self.change_to_string()
                self.games.append(board_str)

            if self.one_person_check_last_stage() == 0:
                if self.can_soldier_move(self.outside_board, self.inside_board, -1) == False:
                    self.points()
                    return 1
                soldier = self.player_turn_regular()
                if self.check_three(self.outside_board, self.inside_board, -1, soldier[0], soldier[1], soldier[2]) == False:
                    board_str = self.change_to_string()
                    self.games.append(board_str)
                else:
                    self.remove_enemy(1)
                    board_str = self.change_to_string()
                    self.games.append(board_str)

        if self.one_person_check_last_stage() == 1:
            while self.check_last_stage() == False:
                if self.check_win() == 0:
                    soldier = self.agent_turn_final_phase()
                    if self.check_three(self.outside_board, self.inside_board, 1, soldier[0], soldier[1], soldier[2]) == False:
                        board_str = self.change_to_string()
                        self.games.append(board_str)
                    else:
                        self.remove_enemy(-1)
                        board_str = self.change_to_string()
                        self.games.append(board_str)

                    if self.check_win() == 0:
                        if self.can_soldier_move(self.outside_board, self.inside_board, -1) == False:
                            self.points()
                            return 1
                        soldier = self.player_turn_regular()
                        if self.check_three(self.outside_board, self.inside_board, -1, soldier[0], soldier[1], soldier[2]) == False:
                            board_str = self.change_to_string()
                            self.games.append(board_str)
                        else:
                            self.remove_enemy(1)
                            board_str = self.change_to_string()
                            self.games.append(board_str)
                    else:
                        self.points()
                        return self.check_win()
                else:
                    self.points()
                    return self.check_win()

            while self.check_win() == 0:
                soldier = self.agent_turn_final_phase()
                if self.check_three(self.outside_board, self.inside_board, 1, soldier[0], soldier[1], soldier[2]) == False:
                    board_str = self.change_to_string()
                    self.games.append(board_str)
                else:
                    self.remove_enemy(-1)
                    board_str = self.change_to_string()
                    self.games.append(board_str)

                if self.check_win() == 0:
                    soldier = self.player_turn_final_phase()
                    if self.check_three(self.outside_board, self.inside_board, -1, soldier[0], soldier[1], soldier[2]) == False:
                        board_str = self.change_to_string()
                        self.games.append(board_str)
                    else:
                        self.remove_enemy(1)
                        board_str = self.change_to_string()
                        self.games.append(board_str)
                else:
                    self.points()
                    return self.check_win()


        elif self.one_person_check_last_stage() == -1:
            while self.check_last_stage() == False:
                if self.check_win() == 0:
                    if self.can_soldier_move(self.outside_board, self.inside_board, 1) == False:
                        self.points()
                        return -1
                    soldier = self.agent_turn_regular()
                    if self.check_three(self.outside_board, self.inside_board, 1, soldier[0], soldier[1], soldier[2]) == False:
                        board_str = self.change_to_string()
                        self.games.append(board_str)
                    else:
                        self.remove_enemy(-1)
                        board_str = self.change_to_string()
                        self.games.append(board_str)

                    if self.check_win() == 0:
                        soldier = self.player_turn_final_phase()
                        if self.check_three(self.outside_board, self.inside_board, -1, soldier[0], soldier[1], soldier[2]) == False:
                            board_str = self.change_to_string()
                            self.games.append(board_str)
                        else:
                            self.remove_enemy(1)
                            board_str = self.change_to_string()
                            self.games.append(board_str)
                    else:
                        self.points()
                        return self.check_win()
                else:
                    self.points()
                    return self.check_win()

            while self.check_win() == 0:
                soldier = self.agent_turn_final_phase()
                if self.check_three(self.outside_board, self.inside_board, 1, soldier[0], soldier[1], soldier[2]) == False:
                    board_str = self.change_to_string()
                    self.games.append(board_str)
                else:
                    self.remove_enemy(-1)
                    board_str = self.change_to_string()
                    self.games.append(board_str)

                if self.check_win() == 0:
                    soldier = self.player_turn_final_phase()
                    if self.check_three(self.outside_board, self.inside_board, -1, soldier[0], soldier[1], soldier[2]) == False:
                        board_str = self.change_to_string()
                        self.games.append(board_str)
                    else:
                        self.remove_enemy(1)
                        board_str = self.change_to_string()
                        self.games.append(board_str)
                else:
                    self.points()
                    return self.check_win()

        self.points()
        return self.check_win()


    def play_one_game_smart_agent(self,dict_init, dict_reg, dict_player_special,dict_agent_special, dict_special, count_boards_found, count_boards_not_found):
        #plays an entire game where the player plays randomly and the agent plays using dictionaries
        board_str = "----------------"
        self.games.append(board_str)
        board_str = ""
        for i in range(5):
            soldier = self.smart_a_init(self.outside_board, self.inside_board, dict_init)
            if soldier[0] == -1:
                count_boards_not_found+=1
                soldier = self.agent_turn_initialize()
                if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                    self.remove_enemy(-1)
            else:
                count_boards_found += 1
            board_str = self.change_to_string()
            self.games.append(board_str)
            soldier = self.player_turn_initialize()
            if self.check_three(self.outside_board, self.inside_board, -1, soldier[0], soldier[1], soldier[2]) == True:
                self.remove_enemy(1)
            board_str = self.change_to_string()
            self.games.append(board_str)

        while self.one_person_check_last_stage() == 0:
            if self.can_soldier_move(self.outside_board, self.inside_board, 1) == False:
                self.points()
                return count_boards_found, count_boards_not_found
            soldier = self.smart_a_reg(self.outside_board, self.inside_board, dict_reg, dict_player_special)
            if soldier[0] == -1:
                count_boards_not_found += 1
                soldier = self.agent_turn_regular()
                if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                    self.remove_enemy(-1)
            else:
                count_boards_found += 1
            board_str = self.change_to_string()
            self.games.append(board_str)

            if self.one_person_check_last_stage() == 0:
                if self.can_soldier_move(self.outside_board, self.inside_board, -1) == False:
                    self.points()
                    return count_boards_found, count_boards_not_found
                soldier = self.player_turn_regular()
                if self.check_three(self.outside_board, self.inside_board, -1, soldier[0], soldier[1], soldier[2]) == True:
                    self.remove_enemy(1)
                board_str = self.change_to_string()
                self.games.append(board_str)

        if self.one_person_check_last_stage() == 1:
            while self.check_last_stage() == False:
                if self.check_win() == 0:
                    soldier = self.smart_a_special(self.outside_board, self.inside_board, dict_agent_special, dict_special)
                    if soldier[0] == -1:
                        count_boards_not_found += 1
                        soldier = self.agent_turn_final_phase()
                        if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                            self.remove_enemy(-1)
                    else:
                        count_boards_found += 1
                    board_str = self.change_to_string()
                    self.games.append(board_str)

                    if self.check_win() == 0:
                        if self.can_soldier_move(self.outside_board, self.inside_board,-1) == False:
                            self.points()
                            return count_boards_found, count_boards_not_found
                        soldier = self.player_turn_regular()
                        if self.check_three(self.outside_board, self.inside_board,-1, soldier[0], soldier[1], soldier[2]) == True:
                            self.remove_enemy(1)
                        board_str = self.change_to_string()
                        self.games.append(board_str)
                    else:
                        self.points()
                        return count_boards_found, count_boards_not_found
                else:
                    self.points()
                    return count_boards_found, count_boards_not_found

            while self.check_win() == 0:
                soldier = self.smart_a_special(self.outside_board, self.inside_board, dict_special, dict_special)
                if soldier[0] == -1:
                    count_boards_not_found += 1
                    soldier = self.agent_turn_final_phase()
                    if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                        self.remove_enemy(-1)
                else:
                    count_boards_found += 1
                board_str = self.change_to_string()
                self.games.append(board_str)

                if self.check_win() == 0:
                    soldier = self.player_turn_final_phase()
                    if self.check_three(self.outside_board, self.inside_board,-1, soldier[0], soldier[1], soldier[2]) == True:
                        self.remove_enemy(1)
                    board_str = self.change_to_string()
                    self.games.append(board_str)
                else:
                    self.points()
                    return count_boards_found, count_boards_not_found


        elif self.one_person_check_last_stage() == -1:
            while self.check_last_stage() == False:
                if self.check_win() == 0:
                    if self.can_soldier_move(self.outside_board, self.inside_board,1) == False:
                        self.points()
                        return count_boards_found, count_boards_not_found
                    soldier = self.smart_a_reg(self.outside_board, self.inside_board,dict_player_special, dict_special)
                    if soldier[0] == -1:
                        count_boards_not_found += 1
                        soldier = self.agent_turn_regular()
                        if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                            self.remove_enemy(-1)
                    else:
                        count_boards_found += 1
                    board_str = self.change_to_string()
                    self.games.append(board_str)

                    if self.check_win() == 0:
                        soldier = self.player_turn_final_phase()
                        if self.check_three(self.outside_board, self.inside_board,-1, soldier[0], soldier[1], soldier[2]) == True:
                            self.remove_enemy(1)
                        board_str = self.change_to_string()
                        self.games.append(board_str)
                    else:
                        self.points()
                        return count_boards_found, count_boards_not_found
                else:
                    self.points()
                    return count_boards_found, count_boards_not_found

            while self.check_win() == 0:
                soldier = self.smart_a_special(self.outside_board, self.inside_board,dict_special, dict_special)
                if soldier[0] == -1:
                    count_boards_not_found += 1
                    soldier = self.agent_turn_final_phase()
                    if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                        self.remove_enemy(-1)
                else:
                    count_boards_found += 1
                board_str = self.change_to_string()
                self.games.append(board_str)

                if self.check_win() == 0:
                    soldier = self.player_turn_final_phase()
                    if self.check_three(self.outside_board, self.inside_board,-1, soldier[0], soldier[1], soldier[2]) == True:
                        self.remove_enemy(1)
                    board_str = self.change_to_string()
                    self.games.append(board_str)
                else:
                    self.points()
                    return count_boards_found, count_boards_not_found

        self.points()
        return count_boards_found, count_boards_not_found


    def play_one_game_explore_explicit(self,dict_init, dict_reg, dict_player_special,dict_agent_special, dict_special, count_boards_found, count_boards_not_found, count_turns):
        #plays an entire game where the player plays randomly and the agent plays 80% using the dictionary and 20% randomly
        board_str = "----------------"
        self.games.append(board_str)
        soldier = [-1,-1,-1]
        board_str = ""
        for i in range(5):
            count_turns+=1
            if count_turns % 5 != 0:
                soldier = self.smart_a_init(self.outside_board, self.inside_board, dict_init)
            if soldier[0] == -1 or count_turns%5==0:
                count_boards_not_found+=1
                soldier = self.agent_turn_initialize()
                if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                    self.remove_enemy(-1)
            else:
                count_boards_found += 1
            board_str = self.change_to_string()
            self.games.append(board_str)
            soldier = self.player_turn_initialize()
            if self.check_three(self.outside_board, self.inside_board, -1, soldier[0], soldier[1], soldier[2]) == True:
                self.remove_enemy(1)
            board_str = self.change_to_string()
            self.games.append(board_str)

        while self.one_person_check_last_stage() == 0:
            count_turns+=1
            if self.can_soldier_move(self.outside_board, self.inside_board, 1) == False:
                self.points()
                return count_boards_found, count_boards_not_found, count_turns
            if count_turns % 5 != 0:
                soldier = self.smart_a_reg(self.outside_board, self.inside_board, dict_reg, dict_player_special)
            if soldier[0] == -1 or count_turns%5==0:
                count_boards_not_found += 1
                soldier = self.agent_turn_regular()
                if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                    self.remove_enemy(-1)
            else:
                count_boards_found += 1
            board_str = self.change_to_string()
            self.games.append(board_str)

            if self.one_person_check_last_stage() == 0:
                if self.can_soldier_move(self.outside_board, self.inside_board, -1) == False:
                    self.points()
                    return count_boards_found, count_boards_not_found, count_turns
                soldier = self.player_turn_regular()
                if self.check_three(self.outside_board, self.inside_board, -1, soldier[0], soldier[1], soldier[2]) == True:
                    self.remove_enemy(1)
                board_str = self.change_to_string()
                self.games.append(board_str)

        if self.one_person_check_last_stage() == 1:
            while self.check_last_stage() == False:
                count_turns += 1
                if self.check_win() == 0:
                    if count_turns % 5 != 0:
                        soldier = self.smart_a_special(self.outside_board, self.inside_board, dict_agent_special, dict_special)
                    if soldier[0] == -1 or count_turns%5==0:
                        count_boards_not_found += 1
                        soldier = self.agent_turn_final_phase()
                        if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                            self.remove_enemy(-1)
                    else:
                        count_boards_found += 1
                    board_str = self.change_to_string()
                    self.games.append(board_str)

                    if self.check_win() == 0:
                        if self.can_soldier_move(self.outside_board, self.inside_board,-1) == False:
                            self.points()
                            return count_boards_found, count_boards_not_found, count_turns
                        soldier = self.player_turn_regular()
                        if self.check_three(self.outside_board, self.inside_board,-1, soldier[0], soldier[1], soldier[2]) == True:
                            self.remove_enemy(1)
                        board_str = self.change_to_string()
                        self.games.append(board_str)
                    else:
                        self.points()
                        return count_boards_found, count_boards_not_found, count_turns
                else:
                    self.points()
                    return count_boards_found, count_boards_not_found, count_turns

            while self.check_win() == 0:
                count_turns += 1
                if count_turns % 5 != 0:
                    soldier = self.smart_a_special(self.outside_board, self.inside_board, dict_special, dict_special)
                if soldier[0] == -1 or count_turns%5==0:
                    count_boards_not_found += 1
                    soldier = self.agent_turn_final_phase()
                    if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                        self.remove_enemy(-1)
                else:
                    count_boards_found += 1
                board_str = self.change_to_string()
                self.games.append(board_str)

                if self.check_win() == 0:
                    soldier = self.player_turn_final_phase()
                    if self.check_three(self.outside_board, self.inside_board,-1, soldier[0], soldier[1], soldier[2]) == True:
                        self.remove_enemy(1)
                    board_str = self.change_to_string()
                    self.games.append(board_str)
                else:
                    self.points()
                    return count_boards_found, count_boards_not_found, count_turns


        elif self.one_person_check_last_stage() == -1:
            while self.check_last_stage() == False:
                count_turns += 1
                if self.check_win() == 0:
                    if self.can_soldier_move(self.outside_board, self.inside_board,1) == False:
                        self.points()
                        return count_boards_found, count_boards_not_found, count_turns
                    if count_turns % 5 != 0:
                        soldier = self.smart_a_reg(self.outside_board, self.inside_board,dict_player_special, dict_special)
                    if soldier[0] == -1 or count_turns%5==0:
                        count_boards_not_found += 1
                        soldier = self.agent_turn_regular()
                        if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                            self.remove_enemy(-1)
                    else:
                        count_boards_found += 1
                    board_str = self.change_to_string()
                    self.games.append(board_str)

                    if self.check_win() == 0:
                        soldier = self.player_turn_final_phase()
                        if self.check_three(self.outside_board, self.inside_board,-1, soldier[0], soldier[1], soldier[2]) == True:
                            self.remove_enemy(1)
                        board_str = self.change_to_string()
                        self.games.append(board_str)
                    else:
                        self.points()
                        return count_boards_found, count_boards_not_found, count_turns
                else:
                    self.points()
                    return count_boards_found, count_boards_not_found, count_turns

            while self.check_win() == 0:
                count_turns += 1
                if count_turns % 5 != 0:
                    soldier = self.smart_a_special(self.outside_board, self.inside_board,dict_special, dict_special)
                if soldier[0] == -1 or count_turns%5==0:
                    count_boards_not_found += 1
                    soldier = self.agent_turn_final_phase()
                    if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                        self.remove_enemy(-1)
                else:
                    count_boards_found += 1
                board_str = self.change_to_string()
                self.games.append(board_str)

                if self.check_win() == 0:
                    soldier = self.player_turn_final_phase()
                    if self.check_three(self.outside_board, self.inside_board,-1, soldier[0], soldier[1], soldier[2]) == True:
                        self.remove_enemy(1)
                    board_str = self.change_to_string()
                    self.games.append(board_str)
                else:
                    self.points()
                    return count_boards_found, count_boards_not_found, count_turns

        self.points()
        return count_boards_found, count_boards_not_found, count_turns

    def play_one_game_smartest(self,dict_init, dict_reg, dict_player_special,dict_agent_special, dict_special, count_boards_found, count_boards_not_found):
        #plays an entire game where the agent plays using the dictinary and the player plays cleverly
        board_str = "----------------"
        self.games.append(board_str)
        board_str = ""
        for i in range(5):
            soldier = self.smart_a_init(self.outside_board, self.inside_board, dict_init)
            if soldier[0] == -1:
                count_boards_not_found+=1
                soldier = self.agent_turn_initialize()
                if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                    self.remove_enemy(-1)
            else:
                count_boards_found += 1
            board_str = self.change_to_string()
            self.games.append(board_str)
            soldier = self.player_turn_initialize_smart()
            if self.check_three(self.outside_board, self.inside_board, -1, soldier[0], soldier[1], soldier[2]) == True:
                self.remove_enemy(1)
            board_str = self.change_to_string()
            self.games.append(board_str)

        while self.one_person_check_last_stage() == 0:
            if self.can_soldier_move(self.outside_board, self.inside_board, 1) == False:
                self.points()
                return count_boards_found, count_boards_not_found
            soldier = self.smart_a_reg(self.outside_board, self.inside_board, dict_reg, dict_player_special)
            if soldier[0] == -1:
                count_boards_not_found += 1
                soldier = self.agent_turn_regular()
                if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                    self.remove_enemy(-1)
            else:
                count_boards_found += 1
            board_str = self.change_to_string()
            self.games.append(board_str)

            if self.one_person_check_last_stage() == 0:
                if self.can_soldier_move(self.outside_board, self.inside_board, -1) == False:
                    self.points()
                    return count_boards_found, count_boards_not_found
                soldier = self.player_turn_regular_smart()
                if self.check_three(self.outside_board, self.inside_board, -1, soldier[0], soldier[1], soldier[2]) == True:
                    self.remove_enemy(1)
                board_str = self.change_to_string()
                self.games.append(board_str)

        if self.one_person_check_last_stage() == 1:
            while self.check_last_stage() == False:
                if self.check_win() == 0:
                    soldier = self.smart_a_special(self.outside_board, self.inside_board, dict_agent_special, dict_special)
                    if soldier[0] == -1:
                        count_boards_not_found += 1
                        soldier = self.agent_turn_final_phase()
                        if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                            self.remove_enemy(-1)
                    else:
                        count_boards_found += 1
                    board_str = self.change_to_string()
                    self.games.append(board_str)

                    if self.check_win() == 0:
                        if self.can_soldier_move(self.outside_board, self.inside_board,-1) == False:
                            self.points()
                            return count_boards_found, count_boards_not_found
                        soldier = self.player_turn_regular_smart()
                        if self.check_three(self.outside_board, self.inside_board,-1, soldier[0], soldier[1], soldier[2]) == True:
                            self.remove_enemy(1)
                        board_str = self.change_to_string()
                        self.games.append(board_str)
                    else:
                        self.points()
                        return count_boards_found, count_boards_not_found
                else:
                    self.points()
                    return count_boards_found, count_boards_not_found

            while self.check_win() == 0:
                soldier = self.smart_a_special(self.outside_board, self.inside_board, dict_special, dict_special)
                if soldier[0] == -1:
                    count_boards_not_found += 1
                    soldier = self.agent_turn_final_phase()
                    if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                        self.remove_enemy(-1)
                else:
                    count_boards_found += 1
                board_str = self.change_to_string()
                self.games.append(board_str)

                if self.check_win() == 0:
                    soldier = self.player_turn_final_phase_smart()
                    if self.check_three(self.outside_board, self.inside_board,-1, soldier[0], soldier[1], soldier[2]) == True:
                        self.remove_enemy(1)
                    board_str = self.change_to_string()
                    self.games.append(board_str)
                else:
                    self.points()
                    return count_boards_found, count_boards_not_found


        elif self.one_person_check_last_stage() == -1:
            while self.check_last_stage() == False:
                if self.check_win() == 0:
                    if self.can_soldier_move(self.outside_board, self.inside_board,1) == False:
                        self.points()
                        return count_boards_found, count_boards_not_found
                    soldier = self.smart_a_reg(self.outside_board, self.inside_board,dict_player_special, dict_special)
                    if soldier[0] == -1:
                        count_boards_not_found += 1
                        soldier = self.agent_turn_regular()
                        if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                            self.remove_enemy(-1)
                    else:
                        count_boards_found += 1
                    board_str = self.change_to_string()
                    self.games.append(board_str)

                    if self.check_win() == 0:
                        soldier = self.player_turn_final_phase_smart()
                        if self.check_three(self.outside_board, self.inside_board,-1, soldier[0], soldier[1], soldier[2]) == True:
                            self.remove_enemy(1)
                        board_str = self.change_to_string()
                        self.games.append(board_str)
                    else:
                        self.points()
                        return count_boards_found, count_boards_not_found
                else:
                    self.points()
                    return count_boards_found, count_boards_not_found

            while self.check_win() == 0:
                soldier = self.smart_a_special(self.outside_board, self.inside_board,dict_special, dict_special)
                if soldier[0] == -1:
                    count_boards_not_found += 1
                    soldier = self.agent_turn_final_phase()
                    if self.check_three(self.outside_board, self.inside_board,1, soldier[0], soldier[1], soldier[2]) == True:
                        self.remove_enemy(-1)
                else:
                    count_boards_found += 1
                board_str = self.change_to_string()
                self.games.append(board_str)

                if self.check_win() == 0:
                    soldier = self.player_turn_final_phase_smart()
                    if self.check_three(self.outside_board, self.inside_board,-1, soldier[0], soldier[1], soldier[2]) == True:
                        self.remove_enemy(1)
                    board_str = self.change_to_string()
                    self.games.append(board_str)
                else:
                    self.points()
                    return count_boards_found, count_boards_not_found

        self.points()
        return count_boards_found, count_boards_not_found

    def change_from_string(self,string):
        #gets a string and returns the board as 2, 2D arrays
        outside_board = np.zeros((3, 3), dtype=int)
        inside_board = np.zeros((3, 3), dtype=int)
        for i in range((len(string)//2)):
            if i < 4:
                row = i//3
                col = i%3
                if string[i] == 'x':
                    outside_board[row][col] = 1
                elif string[i] == 'o':
                    outside_board[row][col] = -1
                else:
                    outside_board[row][col] = 0
            else:
                row = (i+1)//3
                col = (i+1)%3
                if string[i] == 'x':
                    outside_board[row][col] = 1
                elif string[i] == 'o':
                    outside_board[row][col] = -1
                else:
                    outside_board[row][col] = 0
        for i in range((len(string)//2)):
            if i < 4:
                row = i//3
                col = i%3
                if string[i+8] == 'x':
                    inside_board[row][col] = 1
                elif string[i+8] == 'o':
                    inside_board[row][col] = -1
                else:
                    inside_board[row][col] = 0
            else:
                row = (i+1)//3
                col = (i+1)%3
                if string[i+8] == 'x':
                    inside_board[row][col] = 1
                elif string[i+8] == 'o':
                    inside_board[row][col] = -1
                else:
                    inside_board[row][col] = 0
        return outside_board, inside_board

    def change_to_string(self):
        #changes the boards from arrays to a string
        board_str = ""
        for i in range(3):
            for j in range(3):
                if i != 1 or j != 1:
                    if self.outside_board[i][j] == 0:
                        board_str += "-"
                    else:
                        if self.outside_board[i][j] == 1:
                            board_str += "x"
                        else:
                            board_str += "o"
        for i in range(3):
            for j in range(3):
                if i != 1 or j != 1:
                    if self.inside_board[i][j] == 0:
                        board_str += "-"
                    else:
                        if self.inside_board[i][j] == 1:
                            board_str += "x"
                        else:
                            board_str += "o"
        return board_str

    def change_to_string2(self,outside_board, inside_board):
        #changes the boards we get from arrays to a string
        board_str = ""
        for i in range(3):
            for j in range(3):
                if i != 1 or j != 1:
                    if outside_board[i][j] == 0:
                        board_str += "-"
                    else:
                        if outside_board[i][j] == 1:
                            board_str += "x"
                        else:
                            board_str += "o"
        for i in range(3):
            for j in range(3):
                if i != 1 or j != 1:
                    if inside_board[i][j] == 0:
                        board_str += "-"
                    else:
                        if inside_board[i][j] == 1:
                            board_str += "x"
                        else:
                            board_str += "o"
        return board_str

    def points(self):
        #grants points to each board in the game using the "Monte Carlo" method
        self.games.reverse()
        w = self.check_win()
        if w == 1:
            win_num = self.win
        else:
            if w == -1:
                win_num = self.loss
            else:
                win_num = self.draw
        for i in range(len(self.games)):
            self.gamesStr.append((self.games[i], win_num))
            win_num *= self.gamma
        self.gamesStr.reverse()

    def print_board_got(self,outside_board, inside_board):
        #gets a board and prints it
        for i in range(2):
            print(outside_board[0][i], end=" ------ ")
        print(outside_board[0][2], end="")
        print()
        print("|        |        |")
        print("|",end="   ")
        for i in range(2):
            print(inside_board[0][i], end=" -- ")
        print(inside_board[0][2], end="   |")
        print()
        print("|   |         |   |")
        print(outside_board[1][0],end=" - ")
        print(inside_board[1][0], end="         ")
        print(inside_board[1][2], end=" - ")
        print(outside_board[1][2], end="")
        print()
        print("|   |         |   |")
        print("|", end="   ")
        for i in range(2):
            print(inside_board[2][i], end=" -- ")
        print(inside_board[2][2], end="   |")
        print()
        print("|        |        |")
        for i in range(2):
            print(outside_board[2][i], end=" ------ ")
        print(outside_board[2][2], end="")
        print()

    def print_board(self):
        #prints the board
        for i in range(2):
            print(self.outside_board[0][i], end=" ------ ")
        print(self.outside_board[0][2], end="")
        print()
        print("|        |        |")
        print("|",end="   ")
        for i in range(2):
            print(self.inside_board[0][i], end=" -- ")
        print(self.inside_board[0][2], end="   |")
        print()
        print("|   |         |   |")
        print(self.outside_board[1][0],end=" - ")
        print(self.inside_board[1][0], end="         ")
        print(self.inside_board[1][2], end=" - ")
        print(self.outside_board[1][2], end="")
        print()
        print("|   |         |   |")
        print("|", end="   ")
        for i in range(2):
            print(self.inside_board[2][i], end=" -- ")
        print(self.inside_board[2][2], end="   |")
        print()
        print("|        |        |")
        for i in range(2):
            print(self.outside_board[2][i], end=" ------ ")
        print(self.outside_board[2][2], end="")
        print()


with open("dict_init_ANN.json", 'r') as json_file:
    loaded_data1 = json.load(json_file)
with open("dict_reg_ANN.json", 'r') as json_file:
    loaded_data2 = json.load(json_file)
with open("dict_player_special_ANN.json", 'r') as json_file:
    loaded_data3 = json.load(json_file)
with open("dict_agent_special_ANN.json", 'r') as json_file:
    loaded_data4 = json.load(json_file)
with open("dict_special_ANN.json", 'r') as json_file:
    loaded_data5 = json.load(json_file)

# my_games = Games()
# dict_init_ANN, dict_reg_ANN, dict_player_special_ANN, dict_agent_special_ANN, dict_special_ANN  = my_games.games_100000_dumb()
#
# filename1 = 'dict_init_ANN.json'
# with open(filename1, 'w') as json_file:
#     json.dump(dict_init_ANN, json_file, indent=4)
#
# filename2 = 'dict_reg_ANN.json'
# with open(filename2, 'w') as json_file:
#     json.dump(dict_reg_ANN, json_file, indent=4)
#
# filename3 = 'dict_player_special_ANN.json'
# with open(filename3, 'w') as json_file:
#     json.dump(dict_player_special_ANN, json_file, indent=4)
#
# filename4 = 'dict_agent_special_ANN.json'
# with open(filename4, 'w') as json_file:
#     json.dump(dict_agent_special_ANN, json_file, indent=4)
#
# filename5 = 'dict_special_ANN.json'
# with open(filename5, 'w') as json_file:
#     json.dump(dict_special_ANN, json_file, indent=4)
#
# # with open(filename1, 'r') as json_file:
# #     loaded_data1 = json.load(json_file)
# #     print('Loaded data from dict_init:', loaded_data1)
# #
# # with open(filename2, 'r') as json_file:
# #     loaded_data2 = json.load(json_file)
# #     print('Loaded data from dict_reg:', loaded_data2)
# #
# # with open(filename3, 'r') as json_file:
# #     loaded_data3 = json.load(json_file)
# #     print('Loaded data from dict_player_special:', loaded_data3)
# #
# # with open(filename4, 'r') as json_file:
# #     loaded_data4 = json.load(json_file)
# #     print('Loaded data from dict_agent_special:', loaded_data4)
# #
# # with open(filename5, 'r') as json_file:
# #     loaded_data5 = json.load(json_file)
# #     print('Loaded data from dict_special:', loaded_data5)
#
# count = 0
# for i in range(len(dict_init_ANN)):
#     count+=1
# print(count)
# count = 0
# for i in range(len(dict_reg_ANN)):
#     count+=1
# print(count)
# count = 0
# for i in range(len(dict_player_special_ANN)):
#     count+=1
# print(count)
# count = 0
# for i in range(len(dict_agent_special_ANN)):
#     count+=1
# print(count)
# count = 0
# for i in range(len(dict_special_ANN)):
#     count+=1
# print(count)