from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
import json
import numpy as np
import copy
import tensorflow as tf
from kivy.graphics import Color, Line, Ellipse
import random
from kivy.uix.popup import Popup
from kivy.core.window import Window


class FirstScreen(FloatLayout):
    def __init__(self):
        FloatLayout.__init__(self)
        self.outside_board_graph = []
        self.inside_board_graph = []
        self.what_game_size = 1
        self.my_turn = 1
        self.part = 0
        self.which_touch = 1
        self.chosen_piece = []
        self.removing_piece = []
        self.removing = False
        self.difficulty = 1
        self.addPlayerTypeButton()
        self.game_rules()
        self.game_size()
        self.addButton()
        self.controller = Controller()
        self.addCellsToBoard()
        self.agent_turn_UI()
        self.agent_soldiers_UI()
        self.player_turn_UI()
        self.player_soldiers_UI()
        self.addResultLabel()
        self.tutorial()
        self.tutorial = False
        self.agent_turn(1)

    def tutorial(self):
        self.tutorial_button = Button()
        self.tutorial_button.background_color = (0, 1, 1)
        self.tutorial_button.text = "Tutorial"
        self.tutorial_button.pos_hint = {"center_x": .5, "center_y": .05}
        self.tutorial_button.size_hint = (1, .1)
        self.add_widget(self.tutorial_button)

    def agent_turn_UI(self):
        self.agent_turns_button = Button()
        self.agent_turns_button.background_color = (0.5, 0.5, 0.5, 1)
        self.agent_turns_button.text = "Agent"
        self.agent_turns_button.font_size = 30
        self.agent_turns_button.pos_hint = {"center_x": .85, "center_y": .9}
        self.agent_turns_button.size_hint = (.2, .1)
        self.add_widget(self.agent_turns_button)

    def agent_soldiers_UI(self):
        self.agent_soldiers_button = Button()
        self.agent_soldiers_button.background_color = (0.6, 0.6, 0.6, 1)
        self.agent_soldiers_button.text = "X X X X X "
        self.agent_soldiers_button.font_size = 36
        self.agent_soldiers_button.pos_hint = {"center_x": .85, "center_y": .75}
        self.agent_soldiers_button.size_hint = (.3, .15)
        self.add_widget(self.agent_soldiers_button)

    def player_turn_UI(self):
        self.player_turns_button = Button()
        self.player_turns_button.background_color = (0.2, 0.6, 0.3, 1)
        self.player_turns_button.text = "You <"
        self.player_turns_button.font_size = 30
        self.player_turns_button.pos_hint = {"center_x": .85, "center_y": .6}
        self.player_turns_button.size_hint = (.2, .1)
        self.add_widget(self.player_turns_button)

    def player_soldiers_UI(self):
        self.player_soldiers_button = Button()
        self.player_soldiers_button.background_color = (0.4, 0.7, 0.5, 1)
        self.player_soldiers_button.text = "O O O O O "
        self.player_soldiers_button.font_size = 36
        self.player_soldiers_button.pos_hint = {"center_x": .85, "center_y": .45}
        self.player_soldiers_button.size_hint = (.3, .15)
        self.add_widget(self.player_soldiers_button)

    def addButton(self):
        self.buttonRestart = Button()
        self.buttonRestart.background_color = (0.8, 0.3, 0.3, 1)
        self.buttonRestart.text = "refresh"
        self.buttonRestart.pos_hint = {"center_x": .1, "center_y": .2}
        self.buttonRestart.size_hint = (.2, .1)
        self.buttonRestart.bind(on_press = self.reset_game)
        self.add_widget(self.buttonRestart)

    def addResultLabel(self):
        self.result_label = Label()
        self.result_label.font_size = 5
        self.result_label.color = '#00FF00'
        self.result_label.text = ""
        self.result_label.size_hint = (.6, .1)
        self.result_label.pos_hint = {"center_x": .5, "center_y": .3}
        self.add_widget(self.result_label)

        animation = Animation(font_size=70, duration=5,t='out_bounce')
        animation.start(self.result_label)

    def reset_game(self, instance):
        self.clear_board()
        self.result_label.text = ""
        self.agent_soldiers_UI()
        self.player_soldiers_UI()

    def addCellsToBoard(self):

        with self.canvas.before:
            Color(1, 1, 1, 1)  # White color
            # Outer square
            Line(points=[80, 300, 400, 300, 400, 540, 80, 540, 80, 300], width=2)
            # Inner square
            Line(points=[160, 360, 320, 360, 320, 480, 160, 480, 160, 360], width=2)
            # Connecting lines
            Line(points=[80, 420, 160, 420], width=2)
            Line(points=[320, 420, 400, 420], width=2)
            Line(points=[240, 300, 240, 360], width=2)
            Line(points=[240, 540, 240, 480], width=2)


        self.temp_cell1 = Cell(0,0,0)
        self.temp_cell1.size_hint = (.02, .02)
        self.temp_cell1.pos_hint = {"center_x": .1, "center_y": .9}
        self.temp_cell1.text = ""
        self.add_widget(self.temp_cell1)
        self.outside_board_graph.append(self.temp_cell1)

        self.temp_cell2 = Cell(0,0,1)
        self.temp_cell2.size_hint = (.02, .02)
        self.temp_cell2.pos_hint = {"center_x": .3, "center_y": .9}
        self.temp_cell2.text = ""
        self.add_widget(self.temp_cell2)
        self.outside_board_graph.append(self.temp_cell2)

        self.temp_cell3 = Cell(0,0,2)
        self.temp_cell3.size_hint = (.02, .02)
        self.temp_cell3.pos_hint = {"center_x": .5, "center_y": .9}
        self.temp_cell3.text = ""
        self.add_widget(self.temp_cell3)
        self.outside_board_graph.append(self.temp_cell3)

        self.temp_cell4 = Cell(0,1,0)
        self.temp_cell4.size_hint = (.02, .02)
        self.temp_cell4.pos_hint = {"center_x": .1, "center_y": .7}
        self.temp_cell4.text = ""
        self.add_widget(self.temp_cell4)
        self.outside_board_graph.append(self.temp_cell4)

        self.temp_cell5 = Cell(0,1,2)
        self.temp_cell5.size_hint = (.02, .02)
        self.temp_cell5.pos_hint = {"center_x": .5, "center_y": .7}
        self.temp_cell5.text = ""
        self.add_widget(self.temp_cell5)
        self.outside_board_graph.append(self.temp_cell5)

        self.temp_cell6 = Cell(0,2,0)
        self.temp_cell6.size_hint = (.02, .02)
        self.temp_cell6.pos_hint = {"center_x": .1, "center_y": .5}
        self.temp_cell6.text = ""
        self.add_widget(self.temp_cell6)
        self.outside_board_graph.append(self.temp_cell6)

        self.temp_cell7 = Cell(0,2,1)
        self.temp_cell7.size_hint = (.02, .02)
        self.temp_cell7.pos_hint = {"center_x": .3, "center_y": .5}
        self.temp_cell7.text = ""
        self.add_widget(self.temp_cell7)
        self.outside_board_graph.append(self.temp_cell7)

        self.temp_cell8 = Cell(0,2,2)
        self.temp_cell8.size_hint = (.02, .02)
        self.temp_cell8.pos_hint = {"center_x": .5, "center_y": .5}
        self.temp_cell8.text = ""
        self.add_widget(self.temp_cell8)
        self.outside_board_graph.append(self.temp_cell8)

        self.temp_cell9 = Cell(1,0,0)
        self.temp_cell9.size_hint = (.02, .02)
        self.temp_cell9.pos_hint = {"center_x": .2, "center_y": .8}
        self.temp_cell9.text = ""
        self.add_widget(self.temp_cell9)
        self.inside_board_graph.append(self.temp_cell9)

        self.temp_cell10 = Cell(1,0,1)
        self.temp_cell10.size_hint = (.02, .02)
        self.temp_cell10.pos_hint = {"center_x": .3, "center_y": .8}
        self.temp_cell10.text = ""
        self.add_widget(self.temp_cell10)
        self.inside_board_graph.append(self.temp_cell10)

        self.temp_cell11 = Cell(1,0,2)
        self.temp_cell11.size_hint = (.02, .02)
        self.temp_cell11.pos_hint = {"center_x": .4, "center_y": .8}
        self.temp_cell11.text = ""
        self.add_widget(self.temp_cell11)
        self.inside_board_graph.append(self.temp_cell11)

        self.temp_cell12 = Cell(1,1,0)
        self.temp_cell12.size_hint = (.02, .02)
        self.temp_cell12.pos_hint = {"center_x": .2, "center_y": .7}
        self.temp_cell12.text = ""
        self.add_widget(self.temp_cell12)
        self.inside_board_graph.append(self.temp_cell12)

        self.temp_cell13 = Cell(1,1,2)
        self.temp_cell13.size_hint = (.02, .02)
        self.temp_cell13.pos_hint = {"center_x": .4, "center_y": .7}
        self.temp_cell13.text = ""
        self.add_widget(self.temp_cell13)
        self.inside_board_graph.append(self.temp_cell13)

        self.temp_cell14 = Cell(1,2,0)
        self.temp_cell14.size_hint = (.02, .02)
        self.temp_cell14.pos_hint = {"center_x": .2, "center_y": .6}
        self.temp_cell14.text = ""
        self.add_widget(self.temp_cell14)
        self.inside_board_graph.append(self.temp_cell14)

        self.temp_cell15 = Cell(1,2,1)
        self.temp_cell15.size_hint = (.02, .02)
        self.temp_cell15.pos_hint = {"center_x": .3, "center_y": .6}
        self.temp_cell15.text = ""
        self.add_widget(self.temp_cell15)
        self.inside_board_graph.append(self.temp_cell15)

        self.temp_cell16 = Cell(1,2,2)
        self.temp_cell16.size_hint = (.02, .02)
        self.temp_cell16.pos_hint = {"center_x": .4, "center_y": .6}
        self.temp_cell16.text = ""
        self.add_widget(self.temp_cell16)
        self.inside_board_graph.append(self.temp_cell16)

    def change_to_boards(self):
        outside_board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        inside_board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        for i in range(3):
            text = self.outside_board_graph[i].text
            if text == "X":
                outside_board[0][i] = 1
            elif text == "O":
                outside_board[0][i] = -1
            else:
                outside_board[0][i] = 0
        text = self.outside_board_graph[3].text
        if text == "X":
            outside_board[1][0] = 1
        elif text == "O":
            outside_board[1][0] = -1
        else:
            outside_board[1][0] = 0
        text = self.outside_board_graph[4].text
        if text == "X":
            outside_board[1][2] = 1
        elif text == "O":
            outside_board[1][2] = -1
        else:
            outside_board[1][2] = 0
        for i in range(3):
            text = self.outside_board_graph[i+5].text
            if text == "X":
                outside_board[2][i] = 1
            elif text == "O":
                outside_board[2][i] = -1
            else:
                outside_board[2][i] = 0


        for i in range(3):
            text = self.inside_board_graph[i].text
            if text == "X":
                inside_board[0][i] = 1
            elif text == "O":
                inside_board[0][i] = -1
            else:
                inside_board[0][i] = 0
        text = self.inside_board_graph[3].text
        if text == "X":
            inside_board[1][0] = 1
        elif text == "O":
            inside_board[1][0] = -1
        else:
            inside_board[1][0] = 0
        text = self.inside_board_graph[4].text
        if text == "X":
            inside_board[1][2] = 1
        elif text == "O":
            inside_board[1][2] = -1
        else:
            inside_board[1][2] = 0
        for i in range(3):
            text = self.inside_board_graph[i+5].text
            if text == "X":
                inside_board[2][i] = 1
            elif text == "O":
                inside_board[2][i] = -1
            else:
                inside_board[2][i] = 0

        return outside_board, inside_board

    def react(self, board, row, col):

        if (row == 1 and col == 2) or row == 2:
            place = row * 3 + col - 1
        else:
            place = row * 3 + col
        if self.removing == True:
            if (self.controller.check_three_self(1, board, row, col) == False and len(self.controller.list_of_players_self(1)) > 3) or (len(self.controller.list_of_players_self(1)) == 3):
                if board == 0:
                    if self.outside_board_graph[place].text == "X":
                        self.outside_board_graph[place].text = ""
                        outside_board, inside_board = self.change_to_boards()
                        self.controller.player_turn(outside_board, inside_board)
                        self.removing = False
                        self.agent_turn(self.my_turn)
                        self.my_turn += 1
                else:
                    if self.inside_board_graph[place].text == "X":
                        self.inside_board_graph[place].text = ""
                        outside_board, inside_board = self.change_to_boards()
                        self.controller.player_turn(outside_board, inside_board)
                        self.removing = False
                        self.agent_turn(self.my_turn)
                        self.my_turn += 1
        else:
            self.part = self.controller.which_part(self.my_turn)
            answer = self.check(board, row, col)
            if self.part == 1 and answer == True:
                if board == 0:
                    self.outside_board_graph[place].text = "O"
                else:
                    self.inside_board_graph[place].text = "O"
                outside_board, inside_board = self.change_to_boards()
                self.controller.player_turn(outside_board, inside_board)
                if self.controller.check_three_self(-1,board,row,col) == True:
                    self.removing_piece = [board, row, col]
                    self.removing = True
                else:
                    self.agent_turn(self.my_turn)
                    self.my_turn += 1
            elif self.part == 2 or self.part == 4:
                if self.which_touch == 2:
                    if (self.chosen_piece[1] == 1 and self.chosen_piece[2] == 2) or self.chosen_piece[1] == 2:
                        chosen_place = self.chosen_piece[1] * 3 + self.chosen_piece[2] - 1
                    else:
                        chosen_place = self.chosen_piece[1] * 3 + self.chosen_piece[2]
                    if answer == True:
                        can_move = False
                        if self.controller.between_boards(self.chosen_piece[1], self.chosen_piece[2]) == True:
                            is_edge = False
                            if self.controller.mid_is_valid(self.chosen_piece[1], self.chosen_piece[2], row, col) == True:
                                can_move = True
                        else:
                            is_edge = True
                            if self.controller.edge_is_valid(self.chosen_piece[1], self.chosen_piece[2], row, col) == True:
                                can_move = True
                        if can_move == True:
                            if self.chosen_piece[0] == 0:
                                self.outside_board_graph[chosen_place].text = ""
                                self.outside_board_graph[chosen_place].background_color = (0.7, 0.7, 0.7, 1)
                            else:
                                self.inside_board_graph[chosen_place].text = ""
                                self.inside_board_graph[chosen_place].background_color = (0.7, 0.7, 0.7, 1)
                            if board == 0:
                                self.outside_board_graph[place].text = "O"
                            else:
                                self.inside_board_graph[place].text = "O"
                            outside_board, inside_board = self.change_to_boards()
                            self.controller.player_turn(outside_board, inside_board)
                            self.which_touch = 1
                            if self.controller.check_three_self(-1, board, row, col) == True:
                                self.removing_piece = [board, row, col]
                                self.removing = True
                            else:
                                self.agent_turn(self.my_turn)
                                self.my_turn += 1
                        else:
                            self.which_touch = 1
                            if self.chosen_piece[0] == 0:
                                self.outside_board_graph[chosen_place].background_color = (0.7, 0.7, 0.7, 1)
                            else:
                                self.inside_board_graph[chosen_place].background_color = (0.7, 0.7, 0.7, 1)
                    else:
                        self.which_touch = 1
                        if self.chosen_piece[0] == 0:
                            self.outside_board_graph[chosen_place].background_color = (0.7, 0.7, 0.7, 1)
                        else:
                            self.inside_board_graph[chosen_place].background_color = (0.7, 0.7, 0.7, 1)

                else:
                    if answer != True:
                        self.chosen_piece = [board, row, col]
                    text = False
                    if board == 0:
                        if self.outside_board_graph[place].text == "O":
                            text = True
                    else:
                        if self.inside_board_graph[place].text == "O":
                            text = True
                    if text == True:
                        can_move = False
                        if self.controller.between_boards(row, col) == True:
                            is_edge = False
                            if self.controller.mid_can_move(board,row, col) == True:
                                can_move = True
                        else:
                            is_edge = True
                            if self.controller.edge_can_move(board,row, col) == True:
                                can_move = True
                        if can_move == True:
                            if board == 0:
                                self.outside_board_graph[place].background_color = (1, 0, 1, 1)
                            else:
                                self.inside_board_graph[place].background_color = (1, 0, 1, 1)
                            self.which_touch = 2
            else:
                if self.which_touch == 2:
                    if (self.chosen_piece[1] == 1 and self.chosen_piece[2] == 2) or self.chosen_piece[1] == 2:
                        chosen_place = self.chosen_piece[1] * 3 + self.chosen_piece[2] - 1
                    else:
                        chosen_place = self.chosen_piece[1] * 3 + self.chosen_piece[2]
                    if answer == True:
                        if self.chosen_piece[0] == 0:
                            self.outside_board_graph[chosen_place].text = ""
                            self.outside_board_graph[chosen_place].background_color = (0.7, 0.7, 0.7, 1)
                        else:
                            self.inside_board_graph[chosen_place].text = ""
                            self.inside_board_graph[chosen_place].background_color = (0.7, 0.7, 0.7, 1)
                        if board == 0:
                            self.outside_board_graph[place].text = "O"
                        else:
                            self.inside_board_graph[place].text = "O"
                        outside_board, inside_board = self.change_to_boards()
                        self.controller.player_turn(outside_board, inside_board)
                        self.which_touch = 1
                        if self.controller.check_three_self(-1, board, row, col) == True:
                            self.removing_piece = [board, row, col]
                            self.removing = True
                        else:
                            self.agent_turn(self.my_turn)
                            self.my_turn += 1
                    else:
                        self.which_touch = 1
                        if self.chosen_piece[0] == 0:
                            self.outside_board_graph[chosen_place].background_color = (0.7, 0.7, 0.7, 1)
                        else:
                            self.inside_board_graph[chosen_place].background_color = (0.7, 0.7, 0.7, 1)

                else:
                    if answer != True:
                        self.chosen_piece = [board, row, col]
                    text = False
                    if board == 0:
                        if self.outside_board_graph[place].text == "O":
                            text = True
                    else:
                        if self.inside_board_graph[place].text == "O":
                            text = True
                    if text == True:
                        if board == 0:
                            self.outside_board_graph[place].background_color = (1, 0, 1, 1)
                        else:
                            self.inside_board_graph[place].background_color = (1, 0, 1, 1)
                        self.which_touch = 2
            self.player_soldiers_button.text = self.player_soldiers_button.text[:-2]
            return self.part

    def game_rules(self):
        self.rules_button = Button(text="Game Rules",
                                    size_hint=(.2, .1),
                                    pos_hint={"center_x": .375, "center_y": .2})
        self.rules_button.background_color = (0.8, 0.6, 0.2, 1)
        self.rules_button.color = (0, 0, 0, 1)
        self.rules_button.bind(on_press=self.show_rules_popup)
        self.add_widget(self.rules_button)

    def show_rules_popup(self, instance):
        rules_text = """
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
        """

        popup = Popup(title='Game Rules',
                      content=Label(text=rules_text, text_size=(None, None), halign='left', valign='top'),
                      size_hint=(0.8, 0.8))
        popup.open()


    def game_size(self):
        self.game_size_button = Button(text="Game Size",
                                    size_hint=(.2, .1),
                                    pos_hint={"center_x": .625, "center_y": .2})
        self.game_size_button.background_color = (0.8, 0.6, 0.2, 1)
        self.game_size_button.color = (0, 0, 0, 1)
        self.game_size_button.bind(on_press=self.switch_game_size)
        self.add_widget(self.game_size_button)

    def switch_game_size(self, instance):
        with self.canvas.before:
            if self.what_game_size == 1:
                Color(0,0,0)
                # Outer square
                Line(points=[80, 300, 400, 300, 400, 540, 80, 540, 80, 300], width=2)
                # Inner square
                Line(points=[160, 360, 320, 360, 320, 480, 160, 480, 160, 360], width=2)
                # Connecting lines
                Line(points=[80, 420, 160, 420], width=2)
                Line(points=[320, 420, 400, 420], width=2)
                Line(points=[240, 300, 240, 360], width=2)
                Line(points=[240, 540, 240, 480], width=2)

                Color(1, 1, 1, 1)  # White color
                # Outer square
                Line(points=[255, 685, 255, 1235, 1280, 1235, 1280, 685, 255, 685], width=2)
                # Inner square
                Line(points=[510, 820, 510, 1095, 1025, 1095, 1025, 820, 510, 820], width=2)
                # Connecting lines
                Line(points=[255, 960, 510, 960], width=2)
                Line(points=[1025, 960, 1280, 960], width=2)
                Line(points=[770, 685, 770, 820], width=2)
                Line(points=[770, 1095, 770, 1235], width=2)
                self.what_game_size = 2
            else:
                Color(0,0,0)  # White color
                # Outer square
                Line(points=[255, 685, 255, 1235, 1280, 1235, 1280, 685, 255, 685], width=2)
                # Inner square
                Line(points=[510, 820, 510, 1095, 1025, 1095, 1025, 820, 510, 820], width=2)
                # Connecting lines
                Line(points=[255, 960, 510, 960], width=2)
                Line(points=[1025, 960, 1280, 960], width=2)
                Line(points=[770, 685, 770, 820], width=2)
                Line(points=[770, 1095, 770, 1235], width=2)


                Color(1, 1, 1, 1)  # White color
                # Outer square
                Line(points=[80, 300, 400, 300, 400, 540, 80, 540, 80, 300], width=2)
                # Inner square
                Line(points=[160, 360, 320, 360, 320, 480, 160, 480, 160, 360], width=2)
                # Connecting lines
                Line(points=[80, 420, 160, 420], width=2)
                Line(points=[320, 420, 400, 420], width=2)
                Line(points=[240, 300, 240, 360], width=2)
                Line(points=[240, 540, 240, 480], width=2)
                self.what_game_size = 1


    def addPlayerTypeButton(self):
        self.difficulty_button = Button()
        self.update_difficulty_button_text()
        self.difficulty_button.background_color = (0.5, 0.4, 0.7, 1)
        self.difficulty_button.pos_hint = {"center_x": .9, "center_y": .2}
        self.difficulty_button.size_hint = (.2, .1)
        self.difficulty_button.bind(on_press=self.switch_difficulty)
        self.add_widget(self.difficulty_button)


    def switch_difficulty(self, instance):
        self.clear_board()
        self.difficulty += 1
        if self.difficulty > 3:
            self.difficulty = 1
        self.update_difficulty_button_text()


    def update_difficulty_button_text(self):
        if self.difficulty == 1:
            self.difficulty_button.text = "Agent: Dumb"
        elif self.difficulty == 2:
            self.difficulty_button.text = "Agent: ANN"
        elif self.difficulty == 3:
            self.difficulty_button.text = "Agent: Dictionary"

    def agent_turn(self, turn):
        if self.difficulty == 1:
            soldier = self.controller.agent_turn_dumb(turn)
        elif self.difficulty == 2:
            soldier = self.controller.agent_turn_ANN(turn)
        elif self.difficulty == 3:
            soldier = self.controller.agent_turn(turn)
        outside_board, inside_board = self.controller.return_boards()
        for i in range(3):
            if outside_board[0][i] == 1:
                text = "X"
            elif outside_board[0][i] == -1:
                text = "O"
            else:
                text = ""
            self.outside_board_graph[i].text = text
        if outside_board[1][0] == 1:
            text = "X"
        elif outside_board[1][0] == -1:
            text = "O"
        else:
            text = ""
        self.outside_board_graph[3].text = text
        if outside_board[1][2] == 1:
            text = "X"
        elif outside_board[1][2] == -1:
            text = "O"
        else:
            text = ""
        self.outside_board_graph[4].text = text
        for i in range(3):
            if outside_board[2][i] == 1:
                text = "X"
            elif outside_board[2][i] == -1:
                text = "O"
            else:
                text = ""
            self.outside_board_graph[i+5].text = text

        for i in range(3):
            if inside_board[0][i] == 1:
                text = "X"
            elif inside_board[0][i] == -1:
                text = "O"
            else:
                text = ""
            self.inside_board_graph[i].text = text
        if inside_board[1][0] == 1:
            text = "X"
        elif inside_board[1][0] == -1:
            text = "O"
        else:
            text = ""
        self.inside_board_graph[3].text = text
        if inside_board[1][2] == 1:
            text = "X"
        elif inside_board[1][2] == -1:
            text = "O"
        else:
            text = ""
        self.inside_board_graph[4].text = text
        for i in range(3):
            if inside_board[2][i] == 1:
                text = "X"
            elif inside_board[2][i] == -1:
                text = "O"
            else:
                text = ""
            self.inside_board_graph[i+5].text = text
        self.agent_soldiers_button.text = self.agent_soldiers_button.text[:-2]

    def the_turn(self):
        return self.my_turn

    def clear_board(self):
        for cell in self.outside_board_graph:
            cell.text = ""
            cell.background_color = (0.7, 0.7, 0.7, 1) 
        for cell in self.inside_board_graph:
            cell.text = ""
            cell.background_color = (0.7, 0.7, 0.7, 1)
        self.controller.reset_board()
        self.my_turn = 1
        self.part = 0
        self.which_touch = 1
        self.chosen_piece = []
        self.removing_piece = []
        self.removing = False
        self.agent_soldiers_button.text = "X X X X X "
        self.player_soldiers_button.text = "O O O O O "
        self.agent_turn(1)
        self.result_label.text = ""




    def check(self, board, row, col):
        return self.controller.check(board, row, col)


class Cell(Button):
    def __init__(self, board, row, col):
        Button.__init__(self)
        self.text = ""
        self.board = board
        self.row = row
        self.col = col
        self.background_color = (0.7, 0.7, 0.7, 1)

    def on_press(self):
        part = self.parent.react(self.board, self.row, self.col)
        my_turn = self.parent.the_turn()
        if my_turn > 5:
            isWin = self.parent.controller.check_win_board()
            if isWin == 1:
                self.parent.addResultLabel()
                self.parent.result_label.text = "The agent won!!"

            elif isWin == -1:
                self.parent.addResultLabel()
                self.parent.result_label.text = "The player won!!"

class Controller:
    def __init__(self):
        self.logic = Logic()

    def check(self, board, row, col):
        return self.logic.check(board, row, col)

    def check_three_self(self, player, board, row, col):
        return self.logic.check_three_self(player, board, row, col)

    def list_of_players_self(self, player):
        return self.logic.list_of_players_self(player)

    def check_win_board(self):
        return self.logic.check_win_board()

    def agent_turn(self, turn):
        return self.logic.agent_turn(turn)

    def agent_turn_ANN(self, turn):
        return self.logic.agent_turn_ANN(turn)

    def agent_turn_dumb(self, turn):
        return self.logic.agent_turn_dumb(turn)

    def player_turn(self, outside_board, inside_board):
        return self.logic.player_turn(outside_board, inside_board)

    def reset_board(self):
        self.logic.reset_board()

    def which_part(self, turn):
        return self.logic.which_part(turn)

    def between_boards(self, row, col):
        return self.logic.between_boards(row, col)

    def edge_is_valid(self, curr_row, curr_col, row, col):
        return self.logic.edge_is_valid(curr_row, curr_col, row, col)

    def edge_can_move(self, board, row, col):
        return self.logic.edge_can_move(board, row, col)

    def mid_is_valid(self, curr_row, curr_col, row, col):
        return self.logic.mid_is_valid(curr_row, curr_col, row, col)

    def mid_can_move(self, board, row, col):
        return self.logic.mid_can_move(board, row, col)

    def return_boards(self):
        return self.logic.return_boards()

    def print_board(self):
        self.logic.print_board()

class Logic:
    def __init__(self):
        # 0 = empty, 1 = X = agent, -1 = O = player
        self.outside_board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.inside_board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.model_init = tf.keras.models.load_model('initial_model1.keras')
        self.model_reg = tf.keras.models.load_model('reg_model1.keras')
        self.model_player_special = tf.keras.models.load_model('player_special_model1.keras')
        self.model_agent_special = tf.keras.models.load_model('agent_special_model1.keras')
        self.model_special = tf.keras.models.load_model('special_model1.keras')
        filename = 'dict_init.json'
        with open(filename, 'r') as json_file:
            self.dict1 = json.load(json_file)

        filename = 'dict_reg.json'
        with open(filename, 'r') as json_file:
            self.dict2 = json.load(json_file)

        filename = 'dict_player_special.json'
        with open(filename, 'r') as json_file:
            self.dict3 = json.load(json_file)

        filename = 'dict_agent_special.json'
        with open(filename, 'r') as json_file:
            self.dict4 = json.load(json_file)

        filename = 'dict_special.json'
        with open(filename, 'r') as json_file:
            self.dict5 = json.load(json_file)

    def return_boards(self):
        return self.outside_board, self.inside_board


    def check(self, board, row, col):
        if board == 0:
            if self.outside_board[row][col] == 0:
                return True
        elif board == 1:
            if self.inside_board[row][col] == 0:
                return True
        return False

    def empty_places_outside(self, outside_board, inside_board):
        empty_list = list()
        for n in range(3):
            for j in range(3):
                if n!=1 or j!=1:
                    if outside_board[n][j] == 0:
                        empty_list.append([n,j])
        return empty_list

    def empty_places_inside(self, outside_board, inside_board):
        empty_list = list()
        for n in range(3):
            for j in range(3):
                if n!=1 or j!=1:
                    if inside_board[n][j] == 0:
                        empty_list.append([n,j])
        return empty_list


    def list_of_players_self(self, player):
        players_list = list()
        for n in range(3):
            for j in range(3):
                if n != 1 or j != 1:
                    if self.outside_board[n][j] == player:
                        players_list.append([0, n, j])
        for n in range(3):
            for j in range(3):
                if n!=1 or j!=1:
                    if self.inside_board[n][j] == player:
                        players_list.append([1, n, j])
        return players_list


    def list_of_players(self, outside_board, inside_board, player):
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


    def change_to_string2(self, outside_board, inside_board):
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

    def check_three_self(self, player, board, row, col):
        if board == 0:
            if self.between_boards(row,col) == True:
                if row == 1:
                    if self.outside_board[row][col] == player and self.outside_board[row+1][col] == player and self.outside_board[row-1][col] == player:
                        return True
                elif row == 2 or row == 0:
                    if self.outside_board[row][col] == player and self.outside_board[row][col+1] == player and self.outside_board[row][col-1] == player:
                        return True
            else:
                if row == 0 and col == 0:
                    if self.outside_board[0][0] == player and self.outside_board[1][0] == player and self.outside_board[2][0] == player:
                        return True
                    elif self.outside_board[0][0] == player and self.outside_board[0][1] == player and self.outside_board[0][2] == player:
                        return True
                elif row == 0 and col == 2:
                    if self.outside_board[0][2] == player and self.outside_board[1][2] == player and self.outside_board[2][2] == player:
                        return True
                    elif self.outside_board[0][2] == player and self.outside_board[0][1] == player and self.outside_board[0][0] == player:
                        return True
                elif row == 2 and col == 2:
                    if self.outside_board[2][2] == player and self.outside_board[1][2] == player and self.outside_board[0][2] == player:
                        return True
                    elif self.outside_board[2][2] == player and self.outside_board[2][1] == player and self.outside_board[2][0] == player:
                        return True
                else:
                    if self.outside_board[2][0] == player and self.outside_board[1][0] == player and self.outside_board[0][0] == player:
                        return True
                    elif self.outside_board[2][0] == player and self.outside_board[2][1] == player and self.outside_board[2][2] == player:
                        return True
        else:
            if self.between_boards(row,col) == True:
                if row == 1:
                    if self.inside_board[row][col] == player and self.inside_board[row+1][col] == player and self.inside_board[row-1][col] == player:
                        return True
                elif row == 2 or row == 0:
                    if self.inside_board[row][col] == player and self.inside_board[row][col+1] == player and self.inside_board[row][col-1] == player:
                        return True
            else:
                if row == 0 and col == 0:
                    if self.inside_board[0][0] == player and self.inside_board[1][0] == player and self.inside_board[2][0] == player:
                        return True
                    elif self.inside_board[0][0] == player and self.inside_board[0][1] == player and self.inside_board[0][2] == player:
                        return True
                elif row == 0 and col == 2:
                    if self.inside_board[0][2] == player and self.inside_board[1][2] == player and self.inside_board[2][2] == player:
                        return True
                    elif self.inside_board[0][2] == player and self.inside_board[0][1] == player and self.inside_board[0][0] == player:
                        return True
                elif row == 2 and col == 2:
                    if self.inside_board[2][2] == player and self.inside_board[1][2] == player and self.inside_board[0][2] == player:
                        return True
                    elif self.inside_board[2][2] == player and self.inside_board[2][1] == player and self.inside_board[2][0] == player:
                        return True
                else:
                    if self.inside_board[2][0] == player and self.inside_board[1][0] == player and self.inside_board[0][0] == player:
                        return True
                    elif self.inside_board[2][0] == player and self.inside_board[2][1] == player and self.inside_board[2][2] == player:
                        return True

        return False

    def check_three(self, outside_board, inside_board, player, board, row, col):
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

    def smart_a_remove(self, dict1, dict2, str1):
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

    def change_from_string(self,string):
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

    def between_boards(self, row,col):
        if row == 0 and col == 1:
            return True
        if row == 1 and col == 0:
            return True
        if row == 1 and col == 2:
            return True
        if row == 2 and col == 1:
            return True
        return False

    def all_places_available(self,outside_board, inside_board, board,row,col):
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

    def one_person_check_last_stage(self):
        if len(self.list_of_players(self.outside_board, self.inside_board, 1)) == 3:
            return 1
        elif len(self.list_of_players(self.outside_board, self.inside_board, -1)) == 3:
            return -1

        return 0

    def check_last_stage(self):
        if len(self.list_of_players(self.outside_board, self.inside_board,1)) == 3 and len(self.list_of_players(self.outside_board, self.inside_board,-1)) == 3:
            return True

        return False


    def which_part(self, turn):
        if turn<=5:
            return 1
        elif self.check_last_stage() == True:
            return 5
        elif self.one_person_check_last_stage() == 0:
            return 2
        elif self.one_person_check_last_stage() == 1:
            return 4
        elif self.one_person_check_last_stage() == -1:
            return 3


    def edge_is_valid(self, curr_row, curr_col, row, col):
        if row == 1 and curr_col == col:
            return True

        if col == 1 and curr_row == row:
            return True

        return False

    def edge_can_move(self, board, row, col):
        empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
        empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
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

    def mid_can_move(self, board, row, col):
        empty_list_outside = self.empty_places_outside(self.outside_board, self.inside_board)
        empty_list_inside = self.empty_places_inside(self.outside_board, self.inside_board)
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

    def player_turn(self, outside_board1, inside_board1):
        self.outside_board = outside_board1
        self.inside_board = inside_board1

    def agent_turn(self, turn):
        if turn<5:
            return self.agent_turn_init(self.outside_board, self.inside_board, self.dict1)
        elif self.check_last_stage() == True:
            return self.agent_turn_special(self.outside_board, self.inside_board, self.dict5, self.dict5)
        elif self.one_person_check_last_stage() == 0:
            return self.agent_turn_reg(self.outside_board, self.inside_board, self.dict2, self.dict3)
        elif self.one_person_check_last_stage() == 1:
            return self.agent_turn_special(self.outside_board, self.inside_board, self.dict4, self.dict5)
        elif self.one_person_check_last_stage() == -1:
            return self.agent_turn_reg(self.outside_board, self.inside_board,self.dict3, self.dict5)

    def agent_turn_init(self,outside_board, inside_board, dict_init):
        player_list = self.list_of_players(outside_board, inside_board, 1)
        best_score = -1
        best_board = '----------------'
        current_score = -1
        board = -1
        best_row = -1
        best_col = -1
        empty_places_outside = self.empty_places_outside(outside_board, inside_board)
        empty_places_inside = self.empty_places_inside(outside_board, inside_board)
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

    def agent_turn_reg(self,outside_board, inside_board, dict_reg, dict1):
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


    def agent_turn_special(self,outside_board, inside_board,  dict_special, dict1):
        player_list = self.list_of_players(outside_board, inside_board, 1)
        empty_places_outside = self.empty_places_outside(outside_board, inside_board)
        empty_places_inside = self.empty_places_inside(outside_board, inside_board)
        best_score = -1
        best_board = '----------------'
        current_score = -1
        this_board = -1
        best_row = -1
        best_col = -1
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

    def turn_to_array(self, str1):
        row = np.zeros(16, dtype=int)
        for i in range(16):
            char = str1[i]
            if char == 'x':
                row[i] = 1
            elif char == 'o':
                row[i] = -1
            elif char == '-':
                row[i] = 0
            else:
                row[i] = 0
        return row

    def part(self, str1, is_init):
        count_player = -1
        for i in range(len(str1)):
            if str1[i] == 'o':
                count_player+=1
        count_agent = 0
        for i in range(len(str1)):
            if str1[i] == 'x':
                count_agent+=1
        if is_init == True:
            return 1
        elif (count_player>3) and (count_agent>3):
            return 2
        elif count_player == 3 and count_agent>3:
            return 3
        elif count_player>3 and count_agent == 3:
            return 4
        elif count_player == 3 and count_agent == 3:
            return 5

    def smart_a_remove_ANN(self, model1, model2, str1, is_init, part1):
        part2 = self.part(str1, is_init)
        best_take = str1
        current_score = -1
        best_score = -1
        take = list(str1)

        for i in range(len(take)):
            if take[i] == 'o':
                take[i] = '-'
                new_take = ''.join(take)

                if part1 == part2:
                    this_take = self.turn_to_array(new_take)
                    this_take = this_take.reshape(1,-1)
                    current_score = model1.predict(this_take)
                else:
                    this_take = self.turn_to_array(new_take)
                    this_take = this_take.reshape(1,-1)
                    current_score = model2.predict(this_take)

                if current_score > best_score:
                    best_score = current_score
                    best_take = new_take

                take[i] = 'o'

        return best_take

    def agent_turn_ANN(self, turn):
        if turn<5:
            return self.agent_turn_init_ANN(self.outside_board, self.inside_board, self.model_init)
        elif self.check_last_stage() == True:
            return self.agent_turn_special_ANN(self.outside_board, self.inside_board, self.model_special, self.model_special, 5)
        elif self.one_person_check_last_stage() == 0:
            return self.agent_turn_reg_ANN(self.outside_board, self.inside_board, self.model_reg, self.model_reg, 2)
        elif self.one_person_check_last_stage() == 1:
            return self.agent_turn_special_ANN(self.outside_board, self.inside_board, self.model_agent_special, self.model_special, 4)
        elif self.one_person_check_last_stage() == -1:
            return self.agent_turn_reg_ANN(self.outside_board, self.inside_board,self.model_player_special, self.model_special , 3)

    def agent_turn_init_ANN(self,outside_board, inside_board, model):
        player_list = self.list_of_players(outside_board, inside_board, 1)
        best_score = -1
        best_board = '----------------'
        current_score = -1
        board = -1
        best_row = -1
        best_col = -1
        empty_places_outside = self.empty_places_outside(outside_board, inside_board)
        empty_places_inside = self.empty_places_inside(outside_board, inside_board)
        for i in range(len(empty_places_outside)):
            outside_board_next = outside_board.copy()
            inside_board_next = inside_board.copy()
            row = empty_places_outside[i][0]
            col = empty_places_outside[i][1]
            outside_board_next[row][col] = 1
            board_str = self.change_to_string2(outside_board_next, inside_board_next)
            if self.check_three(outside_board_next, inside_board_next,1, 0, row, col) == True:
                str_after_take = self.smart_a_remove_ANN(model, model,  board_str, True, 1)
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
            current_board = self.turn_to_array(board_str)
            current_board = current_board.reshape(1, -1)
            current_score = model.predict(current_board)
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
                str_after_take = self.smart_a_remove_ANN(model, model, board_str, True, 1)
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
            current_board = self.turn_to_array(board_str)
            current_board = current_board.reshape(1, -1)
            current_score = model.predict(current_board)
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

    def agent_turn_reg_ANN(self,outside_board, inside_board, model1, model2, part):
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
                    str_after_take = self.smart_a_remove_ANN(model1, model2, board_str, False, part)
                    board_str = str_after_take
                    best_board = board_str
                    outside_board_best, inside_board_best = self.change_from_string(best_board)
                    self.outside_board = outside_board_best.copy()
                    self.inside_board = inside_board_best.copy()
                    soldier = [board_next, row_next, col_next]
                    return soldier
                current_board = self.turn_to_array(board_str)
                current_board = current_board.reshape(1, -1)
                current_score = model1.predict(current_board)
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


    def agent_turn_special_ANN(self,outside_board, inside_board,  model1, model2, part):
        player_list = self.list_of_players(outside_board, inside_board, 1)
        empty_places_outside = self.empty_places_outside(outside_board, inside_board)
        empty_places_inside = self.empty_places_inside(outside_board, inside_board)
        best_score = -1
        best_board = '----------------'
        current_score = -1
        this_board = -1
        best_row = -1
        best_col = -1
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
                    str_after_take = self.smart_a_remove_ANN(model1, model2, board_str, False, part)
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

                current_board = self.turn_to_array(board_str)
                current_board = current_board.reshape(1, -1)
                current_score = model1.predict(current_board)
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
                    str_after_take = self.smart_a_remove_ANN(model1, model2, board_str, False, part)
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

                current_board = self.turn_to_array(board_str)
                current_board = current_board.reshape(1, -1)
                current_score = model1.predict(current_board)
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

    def agent_turn_dumb(self, turn):
        if turn<5:
            return self.agent_turn_init_dumb()
        elif self.check_last_stage() == True:
            return self.agent_turn_special_dumb()
        elif self.one_person_check_last_stage() == 0:
            return self.agent_turn_reg_dumb()
        elif self.one_person_check_last_stage() == 1:
            return self.agent_turn_special_dumb()
        elif self.one_person_check_last_stage() == -1:
            return self.agent_turn_reg_dumb()

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


    def remove_enemy_dumb(self, player):
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


    def agent_turn_init_dumb(self):
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
        if self.check_three_self(1, board, row, col) == True:
            self.remove_enemy_dumb(-1)

        soldier = [board, row, col]
        return soldier

    def agent_turn_reg_dumb(self):
        #randomly makes a move for the agent's soldier in the regular part of the game
        agent_soldiers = self.list_of_players(self.outside_board, self.inside_board, 1)
        num_soldier = random.randint(0, len(agent_soldiers) - 1)
        soldier = agent_soldiers[num_soldier]
        valid_soldier = False
        while valid_soldier == False:
            if self.between_boards(soldier[1], soldier[2]) == True:
                if self.mid_can_move(soldier[0], soldier[1], soldier[2]) == False:
                    num_soldier = random.randint(0, len(agent_soldiers) - 1)
                    soldier = agent_soldiers[num_soldier]
                else:
                    valid_soldier = True
            else:
                if self.edge_can_move(soldier[0], soldier[1], soldier[2]) == False:
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
        if self.check_three_self(1, board, row, col) == True:
            self.remove_enemy_dumb(-1)
        soldier = [board, row, col]
        return soldier



    def agent_turn_special_dumb(self):
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

        if self.check_three_self(1, board, row, col) == True:
            self.remove_enemy_dumb(-1)
        soldier = [board, row, col]
        return soldier

    def check_win_board(self):
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

    def reset_board(self):
        self.outside_board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.inside_board = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

    def change(self):
        pass

    def restart(self):
        pass

    def checkWin(self):

        pass

    def checkDraw(self):
        pass

    def changeTurn(self):
        pass

    def checkWin(self):
        pass

    def agent(self):
        pass

    def print_board(self):
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


class MyPaintApp(App):
    def build(self):
        return FirstScreen()

MyPaintApp().run()
