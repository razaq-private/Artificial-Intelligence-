import random
import copy
import math
############################################################
# CIS 521: Homework 2
############################################################

student_name = "Abudurazaq Aribidesi"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

############################################################
# Section 1: N-Queens
############################################################


def num_placements_all(n):
    return math.factorial(n*n) / (math.factorial(n*n - n)*math.factorial(n))


def num_placements_one_per_row(n):
    return n**n


def n_queens_valid(board):
    for i in range(len(board)):
        for j in range(i+1, len(board)):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                return False
    return True


def n_queens_solutions(n):
    board = []
    solutions = []
    for sol in n_queens_helper(n, board):
        solutions.append(sol)
    return solutions


def n_queens_helper(n, board):
    if len(board) == n:
        return [board[:]]

    solutions = []

    for i in range(n):
        board.append(i)
        if n_queens_valid(board):
            solutions.extend(n_queens_helper(n, board))
        board.pop()
    return solutions

############################################################
# Section 2: Lights Out
############################################################


class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.board_row = len(board)
        self.board_col = len(board[0])

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        if row >= 0 and row < self.board_row and col >= 0 and col < self.board_col:
            self.board[row][col] = not self.board[row][col]
            neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
            for r, c in neighbors:
                if r >= 0 and r < self.board_row and c >= 0 and c < self.board_col:
                    self.board[r][c] = not self.board[r][c]

    def scramble(self):
        for i in range(self.board_row):
            for j in range(self.board_col):
                if random.random() < 0.5:
                    self.perform_move(i, j)

    def is_solved(self):
        for row in self.board:
            for cell in row:
                if cell:
                    return False
        return True

    def copy(self):
        board_copy = copy.deepcopy(self.board)
        return LightsOutPuzzle(board_copy)

    def successors(self):
        for i in range(self.board_row):
            for j in range(self.board_col):
                test = self.copy()
                test.perform_move(i, j)
                yield ((i, j), test)

    def find_solution(self):
        queue = [([], self)]
        visited_nodes = set()

        if self.is_solved():
            return []

        while queue:
            move, node = queue.pop(0)
            visited_nodes.add(tuple(map(tuple, node.get_board())))
            for new_move, new_node in node.successors():
                if new_node.is_solved():
                    move.append((new_move))
                    return move
                elif tuple(map(tuple, new_node.get_board())) not in visited_nodes:
                    temp = move[:]
                    temp.append((new_move))
                    queue.append((temp, new_node))
        return None

def create_puzzle(rows, cols):
    board = [[False for i in range(cols)]for j in range(rows)]
    return LightsOutPuzzle(board)

############################################################
# Section 3: Linear Disk Movement
############################################################


class LinearDiskIdentical(object):
    def __init__(self, cells, n):
        self.cells = cells
        self.n = n
        self.length = len(cells)

    def get_cells(self):
        return self.cells

    def perform_move(self, prev, to):
        if prev >= 0 and prev < self.length and to >= 0 and to < self.length:
            temp = self.cells[prev]
            self.cells[prev] = self.cells[to]
            self.cells[to] = temp

    def is_solved(self):
        for i in range(self.n):
            if self.cells[self.length - i - 1] == 0: return False
        for i in range(self.length - self.n):
            if self.cells[i] != 0: return False
        return True

    def successors(self):
        for i in range(self.length):
  
            if self.cells[i] == 1:
                if self.cells[i+1] == 0 and i < self.length - 1:
                    test = self.copy()
                    test.perform_move(i, i+1)
                    yield ((i, i+1), test)
                     
                if i < self.length - 2 and self.cells[i+2] == 0 and self.cells[i+1] == 1:
                    test = self.copy()
                    test.perform_move(i, i+2)
                    yield ((i, i+2), test)
                    
                if i - 2 >= 0 and self.cells[i - 1] == 1 and self.cells[i - 2] == 0:
                    test = self.copy()
                    test.perform_move(i, i-2)
                    yield ((i, i-2), test)    
                    
                if i - 1 >= 0 and self.cells[i - 1] == 0:
                    test = self.copy()
                    test.perform_move(i, i-1)
                    yield ((i, i-1), test)
                    

    def copy(self):
        cell_copy = copy.deepcopy(self.cells)
        return LinearDiskIdentical(cell_copy, self.n)

def solve_identical_disks(length, n):
    disk_cell = [1 for i in range(n)]
    empty_cell = [0 for i in range(n, length)]
    cell = disk_cell + empty_cell
    disk_obj = LinearDiskIdentical(cell, n)

    queue = [([], disk_obj)]
    visited_nodes = set()

    if disk_obj.is_solved():
        return []

    while queue:
        move, node = queue.pop(0)
        test = tuple(j for j in disk_obj.get_cells())
        visited_nodes.add(tuple(j for j in disk_obj.get_cells()))
        for new_move, new_node in node.successors():
            if new_node.is_solved():
                move.append((new_move))
                return move
            elif tuple(j for j in disk_obj.get_cells()) not in visited_nodes:
                temp = move[:]
                temp.append((new_move))
                queue.append((temp, new_node))
    return []
      
class LinearDiskDistinct(object):
    def __init__(self, cells, n):
        self.cells = cells
        self.n = n
        self.length = len(cells)

    def get_cells(self):
        return self.cells

    def perform_move(self, prev, to):
        if prev >= 0 and prev < self.length and to >= 0 and to < self.length:
            temp = self.cells[prev]
            self.cells[prev] = self.cells[to]
            self.cells[to] = temp

    def is_solved(self):
        for j in range(self.n):
            if self.cells[self.length - 1 - j] != j: return False
        return True

    def successors(self):
        for i in range(self.length):
            if self.cells[i] != 0:
                if self.cells[i+1] < 0 and i < self.length - 1:
                    test = self.copy()
                    test.perform_move(i, i+1)
                    yield ((i, i+1), test)
  
                if i < self.length - 2 and self.cells[i+2] < 0 and self.cells[i+1] >= 1:
                    test = self.copy()
                    test.perform_move(i, i+2)
                    yield ((i, i+2), test)

                if i > 1 and self.cells[i - 1] < 0:
                    test = self.copy()
                    test.perform_move(i, i-1)
                    yield ((i, i-1), test)   
 
                if i >= 2 and self.cells[i - 1] >= 1 and self.cells[i - 2] < 0:
                    test = self.copy()
                    test.perform_move(i, i-2)
                    yield ((i, i-2), test)

    def copy(self):
        cell_copy = copy.deepcopy(self.cells)
        return LinearDiskDistinct(cell_copy, self.n)

def solve_distinct_disks(length, n):
    disk_cell = [i for i in range(n)]
    empty_cell = [-1 for i in range(n, length)]
    cell = disk_cell + empty_cell
    disk_obj = LinearDiskDistinct(cell, n)

    queue = [([], disk_obj)]
    visited_nodes = set()

    if disk_obj.is_solved():
        return []

    while queue:
        move, node = queue.pop(0)
        visited_nodes.add(tuple(j for j in disk_obj.get_cells()))
        for new_move, new_node in node.successors():
            if new_node.is_solved():
                move.append((new_move))
                return move
            elif tuple(j for j in disk_obj.get_cells()) not in visited_nodes:
                temp = move.copy()
                temp.append(move)
                queue.append((temp, new_node))
    return []


############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
Around 4 days
"""

feedback_question_2 = """
Q3 was the hardest but I am not sure on why\
    i thought the methods would be similar but 
    i had errors somewhere
"""

feedback_question_3 = """
I liked the way Q2 was broken up\ 
it helped me visualize.
"""
