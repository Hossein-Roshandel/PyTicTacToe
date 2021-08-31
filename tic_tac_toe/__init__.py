import os
import math
import random
import pyinputplus
import bcolors
import gc
from itertools import cycle
from tic_tac_toe.arts import logo, x_wins, o_wins

SQUARE_WIDTH = 12
PLAYER_X = f"{bcolors.WARN}{'X':^{SQUARE_WIDTH}}{bcolors.END}"
PLAYER_O = f"{bcolors.FAIL}{'O':^{SQUARE_WIDTH}}{bcolors.END}"
PLAYERS_LIST = [(1, PLAYER_X, x_wins), (-1, PLAYER_O, o_wins)]
PLAYER_POOL = cycle(PLAYERS_LIST)

COMPUTER_PLAYER = random.choice(PLAYERS_LIST)


class Square:

    def __init__(self, row=0, col=0, choice_number=0):
        self.value = 0
        self.row = row
        self.col = col
        self.choice_number = choice_number
        self.neighbors = []

    def get_value(self):
        return self.value

    def update_value(self, new_value):
        """ updates the square value and returns its maximum score"""
        self.value = new_value
        return self.max_move_sum()

    def max_move_sum(self):
        """ returns the maximum score obtained by the current square"""
        scores = []
        for line in self.neighbors:
            line_sum = sum(square.get_value() for square in line) * self.value
            scores.append(line_sum)
        return dict(max=max(scores), sum=sum(scores))

    def __str__(self):
        if self.value == PLAYERS_LIST[0][0]:
            return PLAYERS_LIST[0][1]
        elif self.value == PLAYERS_LIST[1][0]:
            return PLAYERS_LIST[1][1]
        else:
            return f"{self.choice_number:^{SQUARE_WIDTH}}"


class GameTable:
    def __init__(self):

        self.table = [[Square(row=i, col=j) for j in range(3)] for i in range(3)]
        self.update_neighbors()
        self.options = []
        self.update_options()
        self.winner_state = None

    def get_best_move(self, value):
        best_score = -math.inf
        best_move = None
        move_score_pairs = []
        for move in self.options:
            score = self.toggle_score(move, value)
            if score >= best_score:
                best_score = score
                move_score_pairs.append((move, score))
            # print(f"Score: {score:>4}\t\tBest Score: {best_score:>4}\t\t Move: {move}")

        best_move = random.choice([m[0] for m in move_score_pairs if m[1] == best_score])
        return best_move

    def toggle_score(self, move, value):
        """ Toggles the value of a square and returns its best score"""
        self.update_table(square=move[1], value=value)
        score = self.minimax(-value, is_maximizer=not (value == 1))
        self.update_table(square=move[1], value=0)  # return the table to previous state
        return score * value

    def minimax(self, value, depth=4, alpha=-math.inf, beta=math.inf, is_maximizer=False):
        if depth == 0 or self.is_game_finished():
            return self.winner_state if self.winner_state else 0

        if is_maximizer:
            for move in self.options:
                self.update_table(square=move[1], value=value)
                score = self.minimax(-value, depth - 1, alpha, beta, is_maximizer=False)
                self.update_table(square=move[1], value=0)  # return the table to previous state
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return alpha + depth
        else:

            for move in self.options:
                self.update_table(square=move[1], value=value)
                score = self.minimax(-value, depth - 1, alpha, beta, is_maximizer=True)
                self.update_table(square=move[1], value=0)  # return the table to previous state
                beta = min(beta, score)
                if beta < alpha:
                    break
            return beta - depth

    def update_options(self):
        choice_number = 1
        options = []
        for i in range(3):
            for j in range(3):
                if self.table[i][j].value == 0:
                    self.table[i][j].choice_number = choice_number
                    options.append((choice_number, (i, j)))
                    choice_number += 1
        self.options = options

    def update_neighbors(self):
        # set references for vertical and horizontal neighbors
        for i in range(3):
            for j in range(3):
                self.table[i][j].neighbors.append(self.table[i][:])
                self.table[i][j].neighbors.append([self.table[k][j] for k in range(3)])

        # set references for diagonal members
        for i in range(3):
            self.table[i][i].neighbors.append([self.table[j][j] for j in range(3)])
            self.table[2 - i][i].neighbors.append([self.table[2 - j][j] for j in range(3)])

    def update_table(self, square, value):
        """ updates the value of the square and returns its score for game finish criteria"""
        row = square[0]
        col = square[1]
        if value == 0:
            self.table[row][col].update_value(value)
            self.winner_state = None
            self.update_options()
        else:
            square_score = self.table[row][col].update_value(value)
            if square_score['max'] == 3:
                self.winner_state = value * square_score['sum']  # 1 or -1 depending on who wins
            else:
                self.update_options()
                if len(self.options) == 0:
                    self.winner_state = 0  # 0 indicates a tie
            return square_score['max']

    def get_input_options(self):
        return self.options

    def get_display_table(self):
        display_table = [[str(self.table[i][j]) for j in range(3)] for i in range(3)]
        return display_table

    def is_game_finished(self):
        return isinstance(self.winner_state, int)

    def show_table(self):
        TicTacToeGame.clear_console()
        array = self.get_display_table()

        table_str = f"""     
                {"":12}|{"":12}|{"":12}
                {array[0][0]:^{SQUARE_WIDTH}}|{array[0][1]:^{SQUARE_WIDTH}}|{array[0][2]:^{SQUARE_WIDTH}}
                {"":12}|{"":12}|{"":12}
                {'-' * 36}
                {"":12}|{"":12}|{"":12}
                {array[1][0]:^{SQUARE_WIDTH}}|{array[1][1]:^{SQUARE_WIDTH}}|{array[1][2]:^{SQUARE_WIDTH}}
                {"":12}|{"":12}|{"":12}
                {'-' * 36}
                {"":12}|{"":12}|{"":12}
                {array[2][0]:^{SQUARE_WIDTH}}|{array[2][1]:^{SQUARE_WIDTH}}|{array[2][2]:^{SQUARE_WIDTH}}
                {"":12}|{"":12}|{"":12}
    """
        TicTacToeGame.show_logo()
        print(table_str)
        del array
        gc.collect()


class TicTacToeGame:
    def __init__(self):
        self.table = GameTable()

    def play_game(self):
        for i in range(9):
            player = next(PLAYER_POOL)

            if player[0] == COMPUTER_PLAYER[0]:
                best_move = self.table.get_best_move(player[0])
                choice = best_move[1]

            else:
                choice = self.get_user_choice(player)

            score = self.table.update_table(square=choice, value=player[0])
            if score == 3:
                self.table.show_table()
                print(player[2])

                return player[0]
        self.table.show_table()
        print("It's A Tie!")
        return 0

    def get_user_choice(self, player):
        options = self.table.get_input_options()
        self.table.show_table()

        print("You Are Player: ", player[1])
        choice_num = int(
            pyinputplus.inputInt("Please choose a square number> ", min=options[0][0], max=options[-1][0]))
        choice = options[choice_num - 1][1]
        return choice

    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')
        pass

    @staticmethod
    def show_logo():
        TicTacToeGame.clear_console()
        print(logo)
