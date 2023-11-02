import collections
import copy
import itertools
import random
import math

############################################################
# CIS 521: Homework 5
############################################################

student_name = "Abudurazaq Aribidesi"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.


# ############################################################
# # Sudoku Solver
# ############################################################
# game will be mapped out as {(i, j), (possible moves)}

def sudoku_cells():
    cells = []
    for i in range(9):
        for j in range(9):
            cells.append((i, j))
    return cells


def sudoku_arcs():
    arcs = []
    for row, col in sudoku_cells():
        for index in range(9):
            if index != row:
                arcs.append(((row, col), (index, col)))
            if index != col:
                arcs.append(((row, col), (row, index)))

        grid_i = (row // 3) * 3
        grid_j = (col // 3) * 3
        for r in range(grid_i, grid_i + 3):
            for c in range(grid_j, grid_j + 3):
                if r != row and c != col:
                    arcs.append(((row, col), (r, c)))
    return arcs


def read_board(path):
    board = {}
    with open(path) as file:
        lines = file.readlines()
        for row, line in enumerate(lines):
            for col, char in enumerate(line.strip()):
                cell = (row, col)
                if char == '*':
                    board[cell] = set(range(1, 10))
                else:
                    board[cell] = {int(char)}
    return board


class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board
        self.board_map = {}
        # for i in range(9):
        #     for j in range(9):
        #         cell = (i, j)
        #         if self.board[i][j] == 0:
        #             self.board_map[cell] = set(range(1,10))
        #         else:
        #             self.board[cell] = self.board[i][j]

    def get_values(self, cell):
        vals = set(self.board[cell])
        return vals

    def remove_inconsistent_values(self, cell1, cell2):
        c2_vals = list(self.get_values(cell2))
        c1_vals = self.get_values(cell1)
        if len(c2_vals) != 1:
            return False

        val = int(c2_vals[0])
        if val in c1_vals:
            c1_vals.remove(val)
            self.board[cell1] = list(c1_vals)
            return True
        return False

    # find a way to get neighboring cells
    def get_neighbors(self, cell):
        neighbors = set()
        row, col = cell
        # get neighboring rows
        for i in range(9):
            if i != cell[0]:
                neighbors.add((i, col))

        # get neighboring cols
        for j in range(9):
            if j != cell[1]:
                neighbors.add((row, j))

        # check in the 3x3 grid
        grid_row = (row // 3) * 3
        grid_col = (col // 3) * 3

        for i in range(3):
            for j in range(3):
                grid_i = grid_row + i
                grid_j = grid_col + j
                if (grid_i != row or grid_j != col):
                    neighbors.add((grid_i, grid_j))
        return list(neighbors)

    def infer_ac3(self):
        queue = list(self.ARCS)
        while queue:
            cell1, cell2 = queue.pop(0)
            if self.remove_inconsistent_values(cell1, cell2):
                for neighbor in self.get_neighbors(cell1):
                    if neighbor != cell2:
                        queue.append((neighbor, cell1))

    def infer_improved(self):
        extra_inference = True
        while extra_inference:
            self.infer_ac3()
            extra_inference = False
            for cell in self.CELLS:
                vals = self.board[cell]
                # cell has not been assigned a val
                if len(self.board[cell]) > 1:
                    # each possible val in the cell
                    for value in self.board[cell]:
                        unique = True

                        for row in range(9):
                            if (row != cell[0]
                                    and value in self.board[row, cell[1]]):
                                unique = False
                                break
                        if unique:
                            self.board[cell] = [value]
                            extra_inference = True
                            break

                        for col in range(9):
                            if (col != cell[1]
                                    and value in self.board[cell[0], col]):
                                unique = False
                                break
                        if unique:
                            self.board[cell] = [value]
                            extra_inference = True
                            break

                        grid_row = (cell[0] // 3) * 3
                        grid_col = (cell[1] // 3) * 3
                        for i in range(grid_row, grid_row + 3):
                            for j in range(grid_col, grid_col + 3):
                                if ((i, j) != cell
                                        and value in self.board[i, j]):
                                    unique = False
                                    break
                        if unique:
                            self.board[cell] = [value]
                            extra_inference = True
                            break

                    if extra_inference:
                        break

    def create_copy(self):
        return copy.deepcopy(self.board)

    def infer_with_guessing(self):
        self.infer_improved()
        for cell in self.CELLS:
            vals = self.board[cell]
            if len(vals) >= 2:  # cell does not have one value ea
                # for each possible value in the cell
                for possible in self.board[cell]:
                    copy_sudoku = self.create_copy()
                    self.board[cell] = [possible]
                    # recursive call infer_with_guessing
                    self.infer_with_guessing()
                    # is this board solved
                    if all(len(possible_val) == 1
                           for possible_val in self.board.values()):
                        break  # we could keep board as is
                    else:
                        # otherwise get back copy
                        self.board = copy_sudoku
                return


############################################################
# Feedback
############################################################

# Just an approximation is fine.

feedback_question_1 = 25

feedback_question_2 = """
the improved_infer was complicated
"""

feedback_question_3 = """
playing the games
and seeing if the solver
could get it right
"""
