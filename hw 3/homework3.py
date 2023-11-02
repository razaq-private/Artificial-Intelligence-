############################################################
# CIS 521: Homework 3
############################################################
import random
import copy
import queue
import math

student_name = "Abudurazaq Aribidesi"

############################################################
# Section 1: Tile Puzzle
############################################################


def create_tile_puzzle(rows, cols):
    board = [[0 for i in range(cols)]for j in range(rows)]

    counter = 1
    for i in range(rows):
        for j in range(cols):
            board[i][j] = counter
            counter += 1
    board[rows - 1][cols - 1] = 0
    return TilePuzzle(board)


class TilePuzzle(object):
    # Required
    def __init__(self, board):
        self.board = board
        self.board_rows = len(board)
        self.board_cols = len(board[0])
        # keep track of blank tile
        for i in range(self.board_rows):
            for j in range(self.board_cols):
                if self.board[i][j] == 0:
                    self.blank = (i, j)
        return

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        # move based on the directions
        board = self.get_board()
        (blank_r, blank_c) = self.blank

        direction_dict = {"up": (-1, 0),
                          "down": (1, 0),
                          "left": (0, -1),
                          "right": (0, 1)}

        if direction in direction_dict:
            row_dir, col_dir = direction_dict[direction]
            new_blank_r = blank_r + row_dir
            new_blank_c = blank_c + col_dir

        if (0 <= new_blank_r < self.board_rows and
                0 <= new_blank_c < self.board_cols):
            self.board[blank_r][blank_c] = self.board[new_blank_r][new_blank_c]
            self.board[new_blank_r][new_blank_c] = 0
            self.blank = (new_blank_r, new_blank_c)
            return True

        return False

    def scramble(self, num_moves):
        moves = ["up", "down", "left", "right"]
        for n in range(num_moves):
            self.perform_move(random.choice(moves))

    def is_solved(self):
        # can have a solution and check if it matches
        for i in range(self.board_rows):
            for j in range(self.board_cols):
                # last cell = 0
                if i == self.board_rows - 1 and j == self.board_cols - 1:
                    if self.board[i][j] != 0:
                        return False
                elif self.board[i][j] != i * self.board_cols + 1 + j:
                    return False
        return True

    def copy(self):
        return TilePuzzle(copy.deepcopy(self.board))

    def successors(self):
        solutions = []
        for move in ["up", "down", "left", "right"]:
            copy = self.copy()
            if copy.perform_move(move):
                yield move, copy
                # Try to append instead of yield
        #         solutions.append((move, copy))
        # return solutions

    # Required
    def iddfs_helper(self, limit, moves):
        success = []
        if limit == 0:
            return success
        for successor in self.successors():
            new_move, board = successor
            move_list = moves + [new_move]
            if board.is_solved():
                success.append(move_list)
            success.extend(board.iddfs_helper(limit - 1, move_list))
        return success

    def find_solutions_iddfs(self):
        if self.is_solved():
            yield []
        step = 1
        while True:
            solutions = self.iddfs_helper(step, [])
            if solutions:
                for moves in solutions:
                    yield moves
                break
            step += 1

    def heuristic_mdd(self):
        # |x1 - x2| + |y1 - y2|
        board = self.get_board()
        dis = 0

        for i in range(self.board_rows):
            for j in range(self.board_cols):
                tile = board[i][j]
                if tile != 0:
                    row = (tile - 1) // self.board_cols
                    col = (tile - 1) % self.board_cols
                    dis += abs(i - row) + abs(j - col)
        return dis

    def find_solution_a_star(self):
        def generateTuple(input):
            return tuple(map(tuple, input))

        q = queue.PriorityQueue()
        visited = {}
        initial_board = self.get_board()
        visited[generateTuple(initial_board)] = []
        step = 0
        q.put((self.heuristic_mdd(), step, self))

        while not q.empty():
            (curr_cost, curr_counter, current_board) = q.get()
            current_moves = visited[generateTuple(current_board.get_board())]

            if current_board.heuristic_mdd() == 0:
                return current_moves

            for successor in current_board.successors():
                new_move, board = successor
                move_list = current_moves + [new_move]
                total_cost = board.heuristic_mdd() + len(move_list)

                if (generateTuple(board.get_board()) not in visited.keys()):
                    visited[generateTuple(board.get_board())] = move_list
                    q.put((total_cost, step, board))
                    step += 1

############################################################
# Section 2: Grid Navigation
############################################################


def heuristic_euclidean(curr, goal):
    return math.sqrt((curr[0] - goal[0]) ** 2 + (curr[1] - goal[1]) ** 2)


def getNeighbors(node, scene):
    x, y = node
    neighbors = []
    rows = len(scene)
    cols = len(scene[0])
    for change_x in range(-1, 2):
        for change_y in range(-1, 2):
            if change_x == 0 and change_y == 0:
                continue
            new_x, new_y = x + change_x, y + change_y
            if (0 <= new_x < rows and 0 <= new_y < cols and not
                    scene[new_x][new_y]):
                neighbors.append((new_x, new_y))
    return neighbors


def find_path(start, goal, scene):
    # define how to get the neighboring blocks
    # initialize everything
    q = queue.PriorityQueue()
    visited_paths = {}
    visited_paths[start] = ([start], 0)
    (x, y) = start
    (goal_x, goal_y) = goal

    if scene[x][y] or scene[goal_x][goal_y]:
        return None

    start_dist = heuristic_euclidean(start, goal) + 1
    q.put((start_dist, start))

    while not q.empty():
        (dist, curr_node) = q.get()
        (move, dist) = visited_paths[curr_node]
        if curr_node == goal:
            return move

        neighbors = getNeighbors(curr_node, scene)

        for successor in neighbors:
            (next_x, next_y) = successor
            if not scene[next_x][next_y]:
                move_list = list(move)
                move_list.append((next_x, next_y))
                new_distance = (heuristic_euclidean(curr_node,
                                                    (next_x, next_y)) + dist)
                if (next_x, next_y) not in visited_paths.keys():
                    total_dist = (heuristic_euclidean((next_x, next_y), goal)
                                  + new_distance)
                    q.put((total_dist, (next_x, next_y)))
                    visited_paths[(next_x, next_y)] = (move_list, new_distance)
                else:
                    past_move, past_dist = visited_paths[(next_x, next_y)]
                    if new_distance < past_dist:
                        estimated_dist = (new_distance
                                          + heuristic_euclidean((next_x,
                                                                next_y), goal))
                        q.put((estimated_dist, (next_x, next_y)))
                        visited_paths[(next_x, next_y)] = (move_list,
                                                           new_distance)


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

def heuristic_disk(board, target):
    distance = 0
    solutions = {value: i for i, value in enumerate(target)}
    for i in range(len(board)):
        if board[i] > -1:
            solution_index = solutions.get(board[i])
            if solution_index is not None:
                distance += abs(i - solution_index) / 2
    return distance


def makeBoards(length, n):
    board = list(range(n)) + [-1] * (length - n)
    target = [-1] * (length - n) + list(range(n - 1, -1, -1))
    return board, target


def diskMovement(board):
    movements = []
    # conditions to move forward
    for adv in range(len(board) - 1):
        if board[adv] > -1:
            if board[adv + 1] < 0:
                movements.append((adv, adv + 1))
            elif adv < len(board) - 2 and board[adv+2] < 0:
                movements.append((adv, adv+2))

        # conditions to move backwards
        back = len(board) - 1 - adv
        if board[back] > -1:
            if board[back - 1] < 0:
                movements.append((back, back - 1))
            elif back > 1 and board[back - 2] < 0:
                movements.append((back, back - 2))
    return movements


def solve_distinct_disks(length, n):
    start_board, target = makeBoards(length, n)
    q = queue.PriorityQueue()
    visited_boards = {}
    board = []
    visited_boards[tuple(start_board)] = []
    print(visited_boards)
    cost = heuristic_disk(start_board, target)
    q.put((cost, board))

    while not q.empty():
        dist, board = q.get()
        board_tuple = tuple(board)
        move = visited_boards[board_tuple]
        if board == target:
            return move
    print(move)
    movements = diskMovement(board)
    print(movements)
    for successor in movements:
        past, new = successor
        new_board = [board]
        move_list = [move]
        new_board[new] = board[past]
        new_board[past] = -1
        move_list.append((past, new))
        new_board_tuple = tuple(new_board)

        if new_board_tuple not in visited_boards.keys():
            cost = heuristic_disk(new_board, target) + len(move_list)
            q.put((cost, new_board))
            visited_boards[new_board_tuple] = move_list
    return None


############################################################
# Section 4: Feedback
############################################################

# Just an approximation is fine.
feedback_question_1 = 27

feedback_question_2 = """
The concept of A* was tough for me
because I wasn't sure on how
to implement it
"""

feedback_question_3 = """
the visualization aspect that came
with the first problem
"""
