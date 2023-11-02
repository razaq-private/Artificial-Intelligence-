import collections
import copy
import itertools
import random
import math
import numpy as np

############################################################
# CIS 521: Homework 4
############################################################

student_name = "Abudurazaq Aribidesi"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

############################################################
# Section 1: Dominoes Game
############################################################


def create_dominoes_game(rows, cols):
    board = [[False for i in range(cols)] for j in range(rows)]
    return DominoesGame(board)


class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.board_rows = len(board)
        self.board_cols = len(board[0])

    def get_board(self):
        return self.board

    def reset(self):
        for i in range(self.board_rows):
            for j in range(self.board_cols):
                self.board[i][j] = False

    def is_legal_move(self, row, col, vertical):
        # check if outside boundary
        if (row < 0 or row >= self.board_rows or
                col < 0 or col >= self.board_cols):
            return False

        if vertical:
            if row + 1 >= self.board_rows:
                return False
            if self.board[row][col] or self.board[row + 1][col]:
                return False
        else:
            if col + 1 >= self.board_cols:
                return False
            if self.board[row][col] or self.board[row][col + 1]:
                return False
        return True

    def legal_moves(self, vertical):
        for i in range(self.board_rows):
            for j in range(self.board_cols):
                if self.is_legal_move(i, j, vertical):
                    yield (i, j)

    def perform_move(self, row, col, vertical):
        self.board[row][col] = True
        if vertical:
            self.board[row + 1][col] = True
        else:
            self.board[row][col + 1] = True

    def game_over(self, vertical):
        for i in range(self.board_rows):
            for j in range(self.board_cols):
                if self.is_legal_move(i, j, vertical):
                    return False
        return True

    def copy(self):
        copy_board = copy.deepcopy(self.board)
        return DominoesGame(copy_board)

    def successors(self, vertical):
        legal_moves = self.legal_moves(vertical)
        for move in legal_moves:
            copy = self.copy()
            copy.perform_move(move[0], move[1], vertical)
            yield move, copy

    def get_random_move(self, vertical):
        legal_moves = self.legal_moves(vertical)
        return random.choice(legal_moves)

    # Required
    def get_best_move(self, vertical, limit):
        if vertical:
            move, value, total_leaves = self.alpha_beta_max(0, limit,
                                                            -np.inf, np.inf)
        else:
            # if horizontal
            move, value, total_leaves = self.alpha_beta_max(0, limit,
                                                            -np.inf, np.inf)
            value = value * -1
        return ((move[0], move[1]), value, total_leaves)

    # Create two methods for max and min
    def alpha_beta_max(self, vertical, limit, alpha, beta):
        # check termination condition
        if self.game_over(True) or limit == vertical:
            # calculate best value as num_player_moves(original vertical)
            # - num_opp_moves(~original_vertical)
            best_value = (len(list(self.legal_moves(True)))
                          - len(list(self.legal_moves(False))))
            # return best_move, best_val, total_leaves
            return None, best_value, 1

        # initialze return variables
        best_move = None
        value = -np.inf
        total_leaves = 0

        # try to find max of self's successors
        for move, new_game in self.successors(True):
            new_move, new_value, new_leaves = new_game.alpha_beta_min(
                vertical+1, limit, alpha, beta)
            # update total_leaves
            total_leaves += new_leaves
            # update variabels if new max found
            if new_value > value:
                value = new_value
                best_move = move
            if new_value >= beta:
                # break if the prining check is true
                break
            if new_value > alpha:
                # update alpha
                alpha = new_value
        return best_move, value, total_leaves

    def alpha_beta_min(self, vertical, limit, alpha, beta):
        # similar to alpha_beta_max
        # check termination condition
        if self.game_over(False) or limit == vertical:
            # calculate best value as num_player_moves(original vertical)
            # - num_opp_moves(~original_vertical)
            best_value = (len(list(self.legal_moves(True)))
                          - len(list(self.legal_moves(False))))
            # return best_move, best_val, total_leaves
            return None, best_value, 1

        # initialze return variables
        best_move = None
        value = np.inf
        total_leaves = 0

        # try to find max of self's successors
        for move, new_game in self.successors(False):
            new_move, new_value, new_leaves = new_game.alpha_beta_max(
                vertical + 1, limit, alpha, beta)
            # update total_leaves
            total_leaves += new_leaves
            # update variabels if new max found
            if new_value < value:
                value = new_value
                best_move = move
            if new_value <= alpha:
                # break if the prining check is true
                break
            if new_value < beta:
                # update beta
                beta = new_value
        return best_move, value, total_leaves


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
5
"""

feedback_question_2 = """
Just the debugging of the
max and min
"""

feedback_question_3 = """
liked the written
explanation of how
to do alpha beta
"""
